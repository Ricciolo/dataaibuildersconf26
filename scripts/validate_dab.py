"""Validate DAB without printing the local connection string."""
import os,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
values=dict(line.split('=',1) for line in (root/'.env').read_text().splitlines() if '=' in line)
env=os.environ.copy();env['DOTNET_ROOT']=str(root/'.local/dotnet')
env['DAB_CONNECTION_STRING']='Host=127.0.0.1;Port=55432;Database=orders_demo;Username=quality_reader;Password='+values['QUALITY_PASSWORD']
result=subprocess.run([str(root/'.local/tools/dab'),'validate','--config',str(root/'config/dab-config.json')],env=env,capture_output=True,text=True)
output=result.stdout+result.stderr
for secret in values.values():output=output.replace(secret,'[REDACTED]')
print(output);raise SystemExit(result.returncode)
