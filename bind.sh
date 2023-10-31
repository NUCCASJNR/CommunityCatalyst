#!/usr/bin/bash

tmux new-session -d 'gunicorn --bind 0.0.0.0:5000 app:app'