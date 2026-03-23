#!/usr/bin/env python3
import subprocess
import sys
import os
import tty
import termios
import select

def run_ssh_with_password(host, user, password, command):
    """Run SSH with password via PTY"""
    import pty
    import time
    
    pid, master = pty.fork()
    
    if pid == 0:
        # Child - exec ssh
        os.execvp('ssh', ['ssh', '-o', 'StrictHostKeyChecking=no', 
                          '-o', 'UserKnownHostsFile=/dev/null',
                          f'{user}@{host}'] + command.split())
    else:
        # Parent - interact with PTY
        import os
        import time
        
        def write_fd(fd, data):
            while data:
                n = os.write(fd, data.encode())
                if n <= 0:
                    break
                data = data[n:]
        
        time.sleep(0.5)
        
        # Send password when prompted
        while True:
            r, w, e = select.select([master, sys.stdin], [], [], 1.0)
            if master in r:
                try:
                    data = os.read(master, 1024)
                    if not data:
                        break
                    sys.stdout.write(data.decode('utf-8', errors='replace'))
                    sys.stdout.flush()
                    
                    # Detect password prompt and send password
                    if b'password:' in data.lower() or b'password:' in data:
                        time.sleep(0.2)
                        write_fd(master, password + '\n')
                except OSError:
                    break
            if sys.stdin in r:
                data = os.read(sys.stdin.fileno(), 1024)
                if data:
                    write_fd(master, data.decode())
        
        os.waitpid(pid, 0)

if __name__ == '__main__':
    host = '134.175.217.108'
    user = 'root'
    password = 'HAOyan123.'
    command = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'echo connected'
    
    run_ssh_with_password(host, user, password, command)
