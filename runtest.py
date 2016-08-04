#!/usr/bin/env python

LINEWIDTH = 80
COLORIZED = True

import os
import shlex
import subprocess
import sys

def cmd_quote(string):
    import sys
    if sys.version_info < (3,3):
        import pipes
        return pipes.quote(string)
    else:
        import shlex
        return shlex.quote(string)

def main():
    # Store arguments
    testname = sys.argv[1]
    logfile = sys.argv[2]
    cmds = sys.argv[3:]

    # Run test and save results
    with open(logfile, 'w') as f:
        cmd = ' '.join(map(cmd_quote, cmds))
        f.write("# Command executed: ")
        f.write(cmd)
        f.write('\n')
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True, shell=True)
        out, _ = p.communicate()
        f.write(out)
        returncode = p.returncode

    # Check returncode to set status
    if returncode == 0:
        status = True
        statustext = 'PASS'
    else:
        status = False
        statustext = 'FAIL'

    # Add coloring if desired
    use_colors = COLORIZED
    if 'COLORIZED' in os.environ:
        use_colors = True if os.environ['COLORIZED'] == '1' else False
    if use_colors and sys.stdout.isatty():
        if status:
            statustext = '\033[32m' + statustext + '\033[0m'
        else:
            statustext = '\033[31m' + statustext + '\033[0m'

    # Print status
    print("{t} {d} {s}".format(t=testname,
                               d=(LINEWIDTH-len(testname)-4-2)*'.',
                               s=statustext))

if __name__ == '__main__':
    sys.exit(main())
