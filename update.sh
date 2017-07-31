#!/bin/sh

python3.6 setup_dirs.py

git add .
git commit -m "updated plugins"
git push origin master
