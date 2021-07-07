#!/bin/zsh

# Author: Blovedawn
# Release Date: 2021.6

# Clone from github

git clone https://github.com/BloveDawn/XQT-Clockin.git

# go to XQT-AutoClockin folder

cd $(pwd)/XQT-Clockin
echo "[!] working directory:" $(pwd)

# mv id_save_sample.txt to id_save.txt

mv id_save_sample.txt id_save.txt

# Setup
echo '[+] XQT-AutoClockin Setup...'
cd tools
echo "[!] working directory:" $(pwd)

echo '[1] Section1: Setup Python Env...)'
echo '[1] Run command:'$(pwd)'/InstallPython.sh'
source $(pwd)/InstallPython.sh

echo '[2] Section2: Setup crontab...'
echo '[2] Run command:'$(pwd)'/AddCron.sh'
source $(pwd)/AddCron.sh

echo '[!] setup end.'