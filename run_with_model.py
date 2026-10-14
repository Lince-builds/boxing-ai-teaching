#!/usr/bin/env python3
"""macOS-tested hidden input; credentials remain in this process only."""
import getpass,os,runpy,sys
from pathlib import Path
if not os.environ.get('DEEPSEEK_API_KEY'):
    if not sys.stdin.isatty():
        raise SystemExit('请在交互终端运行，以便隐藏输入；不从命令参数或文件读取密钥。')
    secret=getpass.getpass('输入自己的 DeepSeek API Key（隐藏输入，不保存）：').strip()
    if not secret or any(c.isspace() for c in secret):raise SystemExit('密钥为空或含空格，未启动。')
    os.environ['DEEPSEEK_API_KEY']=secret
    del secret
print('凭证仅供本次进程使用；Ctrl+C 停止。输入环节请勿录屏。',flush=True)
sys.argv[0]=str(Path(__file__).with_name('app.py'))
runpy.run_path(sys.argv[0],run_name='__main__')
