"""Generate ignored local secrets and Claude configuration. Does not modify Claude Desktop."""
import json, os, secrets, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
local=ROOT/'.local'; local.mkdir(exist_ok=True)
envfile=ROOT/'.env'
if not envfile.exists():
 envfile.write_text(''.join(k+'='+secrets.token_hex(20)+'\n' for k in ['POSTGRES_PASSWORD','READER_PASSWORD','QUALITY_PASSWORD'])); envfile.chmod(0o600)
env=dict(line.split('=',1) for line in envfile.read_text().splitlines() if '=' in line)
npx=shutil.which('npx') or '/opt/homebrew/bin/npx'
def wrapper(name,body):
 p=local/name; p.write_text('#!/bin/sh\nset -eu\n'+body+'\n'); p.chmod(0o700); return str(p)
dbhub=wrapper('dbhub',"export DSN='postgres://demo_reader:"+env['READER_PASSWORD']+"@127.0.0.1:55432/orders_demo'\nexec '"+npx+"' -y @bytebase/dbhub@1.5.1 --transport stdio --config '"+str(ROOT/'config/dbhub.toml')+"'")
dab=wrapper('dab',"export DOTNET_ROOT='"+str(ROOT/'.local/dotnet')+"'\nexport DAB_CONNECTION_STRING='Host=127.0.0.1;Port=55432;Database=orders_demo;Username=quality_reader;Password="+env['QUALITY_PASSWORD']+"'\nexec '"+str(ROOT/'.local/tools/dab')+"' start --mcp-stdio role:anonymous --config '"+str(ROOT/'config/dab-config.json')+"' --LogLevel Error")
config={'mcpServers':{'orders-dbhub':{'command':dbhub},'orders-evidence':{'command':npx,'args':['-y','@modelcontextprotocol/server-filesystem@2.1.0',str(ROOT/'public/evidence')]}}}
(local/'claude_desktop_config.json').write_text(json.dumps(config,indent=2))
(local/'claude-dab-fragment.json').write_text(json.dumps({'mcpServers':{'orders-quality':{'command':dab}}},indent=2))
print('Generated .env and .local configs. Merge into Claude Desktop manually; never upload these files.')
