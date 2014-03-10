import i3
import json
import os
import datetime
import random

def get_config(file=None):
    if file is None:
        file=os.environ['HOME'] + "/.config/i3/workspaces.json"
    configfile = open(file, 'r')
    configjson = configfile.read()
    config = json.loads(configjson)
    configfile.close()
    return config

def get_workspace(number):
    """gets a workspace by number, as opposed to name"""
    config = get_config()
    if str(number) in config:
        space = config[str(number)]
    else:
        space = None

    existing = [wks for wks in i3.get_workspaces() if wks['num'] is int(number)]
    print(config)
    if len(existing):
        return existing[0]['name']
    else:
        if space is None:
            default_rfile = '/usr/share/dict/american-english'
            if "random" in config:
                rfile = os.path.expanduser(config['random']['file'])
            else:
                rfile = default_rfile
            try:
                words = open(rfile)
            except:
                words = open(default_rfile)
            total_chars = words.seek(0, 2)
            position = random.randint(0, total_chars)
            words.seek(position)
            rname = words.readline()
            rname = words.readline().replace("\n", "")
            space = {"name": rname}
        wksname = str(number) + ": " + space['name']
        return wksname


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description = "Change to a workspace based on number, not name. Uses JSON config file")
    parser.add_argument("--move", help="move to workspace", action="store_true")
    parser.add_argument("workspace", help="workspace number", metavar="<workspace number>", type = int)
    args = parser.parse_args()
    name = get_workspace(args.workspace)
    print(name)
    if (args.move):
        i3.movetoworkspace(name)
    else:
        i3.workspace(name)
