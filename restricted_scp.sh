#!/bin/bash
# Made with ChatGPT
ALLOWED_DIR="/flash/LuscombeU/"$(whoami)"/cache/last-flask"
if [[ "$SSH_ORIGINAL_COMMAND" =~ ^scp\ -[ftr]\ .*$ ]]; then
    if [[ "$SSH_ORIGINAL_COMMAND" =~ .*$ALLOWED_DIR.* ]]; then
        $SHELL -c $SSH_ORIGINAL_COMMAND
    else
        echo "This SSH key is restricted to operations within the $ALLOWED_DIR directory."
        exit 1
    fi
else
    echo "This SSH key is only allowed to use SCP."
    exit 1
fi
