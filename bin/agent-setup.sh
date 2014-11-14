#!/usr/bin/env bash

gnupginf="/tmp/gpg-agent-info-${USER}"
sshinf="/tmp/ssh-agent-info-${USER}"

if pgrep -x -u "${USER}" gpg-agent >/dev/null 2>&1; then
    eval $(cat $gnupginf)
    eval $(cut -d= -f1 $gnupginf | xargs echo export)
else
    eval $(gpg-agent -s --daemon --write-env-file "$gnupginf")
fi

if ! pgrep -x -u "${USER}" ssh-agent >/dev/null 2>&1; then
    ssh-agent > $sshinf
fi
eval $(cat $sshinf)
eval $(cut -d= -f1 $sshinf | xargs echo export)
