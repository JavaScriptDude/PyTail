import asyncio
import os
import subprocess
import sys
from asyncio.subprocess import PIPE

async def main(fname:str, enc:str):

    def h_out(s):
        print(f"[O] {s}")

    def h_err(s): 
        print(f"[E] {s}")

    async def _rs(stream, cb, enc):  
        while True:
            line = await stream.readline()
            if line:
                line = line.decode(enc)
                cb(line.rstrip())
            else:
                break

    cmd = ['tail', '-f', fname]
    p = await asyncio.create_subprocess_exec(*cmd
                            , stdout=PIPE, stderr=PIPE)

    await asyncio.wait([_rs(p.stdout, h_out, enc)
                       ,_rs(p.stderr, h_err, enc)])
    
    await p.wait()


def exit_cli(msg=None, code:int=1):
    msg = f'\n{msg}' if msg else ''
    print(f"tail.py logfile [encoding]\n. encoding default: utf-8{msg}\n"); 
    sys.exit(code)


if __name__ == '__main__':
    if (os.name == 'nt'):
        def _nc():
            exit_cli(f'cygwin tail not found. For instructions see: https://github.com/JavaScriptDude/cygtail')
        try:
            s = subprocess.check_output(['tail', '--version'])
        except FileNotFoundError as ex:
            _nc()
        if s.decode().find("Packaged by Cygwin") == -1: _nc()
            

        loop = asyncio.ProactorEventLoop() # for subprocess' pipes on Windows
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()
    
    args = sys.argv[1:]
    if len(args) == 1: 
        fname = args[0]
        enc = 'utf-8'
    elif len(args) == 2:
        (fname, enc) = args   
    else:
        exit_cli('Please provide file to tail')    

    if os.path.isdir(fname): exit_cli(f"Log file '{fname}' is a directory")
    if not os.path.isfile(fname): exit_cli(f"Log file '{fname}' does not exist")
    if not os.access(fname, os.R_OK): exit_cli(f"Log file '{fname}' is not readable")

    try:
        loop.run_until_complete(main(fname, enc))
    except KeyboardInterrupt as ex:
        # Does not fire with cygtail
        print(f"\n{ex.__doc__}")

    sys.exit(0)