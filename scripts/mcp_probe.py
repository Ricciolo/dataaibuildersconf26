"""Small stdio JSON-RPC probe, no additional dependencies. Logs only synthetic results."""
import argparse,json,os,queue,subprocess,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('server',choices=['dbhub','dab','filesystem']);p.add_argument('--call');p.add_argument('--arguments',default='{}');a=p.parse_args()
if a.server=='filesystem':
 config=json.loads((ROOT/'.local/claude_desktop_config.json').read_text())['mcpServers']['orders-evidence'];cmd=[config['command']]+config['args']
else:cmd=[str(ROOT/'.local'/a.server)]
process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
q=queue.Queue()
def read():
 for line in process.stdout:q.put(line)
threading.Thread(target=read,daemon=True).start()
# Drain stderr without printing DSNs or other accidental sensitive diagnostics.
threading.Thread(target=lambda: list(process.stderr),daemon=True).start()
seq=0
def send(method,params=None,notify=False):
 global seq
 seq+=1;msg={'jsonrpc':'2.0','method':method}
 if params is not None:msg['params']=params
 if not notify:msg['id']=seq
 process.stdin.write(json.dumps(msg)+'\n');process.stdin.flush()
 if notify:return
 deadline=time.monotonic()+120
 while time.monotonic()<deadline:
  try:line=q.get(timeout=1)
  except queue.Empty:
   if process.poll() is not None:raise RuntimeError('Server exited: '+str(process.returncode))
   continue
  try:result=json.loads(line)
  except ValueError:continue
  if result.get('id')==seq:return result
 raise TimeoutError(method)
try:
 init=send('initialize',{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'conference-probe','version':'1'}})
 print(json.dumps(init));assert 'result' in init
 send('notifications/initialized',notify=True)
 listed=send('tools/list',{});assert 'result' in listed;print(json.dumps({'tools':[{'name':t['name'],'inputSchema':t['inputSchema']} for t in listed['result']['tools']]}))
 if a.call: print(json.dumps(send('tools/call',{'name':a.call,'arguments':json.loads(a.arguments)})))
finally:
 process.terminate()
 try:process.wait(timeout=5)
 except subprocess.TimeoutExpired:process.kill()
