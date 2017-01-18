#!/usr/bin/python2

# This script opens a dmenu and lets you type a new name for the
# current workspace. The naming is done like "x: name", where x is
# the workspace number.
#
# Author: Jan Oliver Oelerich

import i3
import subprocess
from os.path import expanduser
def get_workspace():
    workspaces = i3.get_workspaces()
    for workspace in workspaces:
        if workspace['focused']:
            return workspace
    return None

def dmenu_prompt(num):
    script = expanduser('~/.config/i3/bin/make-menu')
    dmenu = subprocess.Popen([
        script, '-P',
        '-f', 'Ubuntu Mono 24',
        '-p', 'Rename workspace {0}'.format(num), # prompt
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    name = dmenu.communicate("")[0].decode().rstrip()
    return name

if __name__ == '__main__':
    ws = get_workspace()

    name = dmenu_prompt(ws['num'])
    if not len(name):
        exit(0)
    print(ws['name'])
    i3.command("rename workspace \"{0}\" to \"{1}: {2}\"".format(
        ws['name'],
        ws['num'],
        name
    ))
