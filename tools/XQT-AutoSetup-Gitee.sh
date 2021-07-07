#!/bin/zsh

# Author: Blovedawn
# Release Date: 2021.6

# Clone from gitee

git clone https://gitee.com/blovedawn/XQT-Clockin.git

# go to XQT-AutoClockin folder

cd $(pwd)/XQT-Clockin
echo "[!] working directory:" $(pwd)"/XQT-Clockin"

# mv id_save_sample.txt to id_save.txt

mv id_save_sample.txt id_save.txt

# Setup
echo '[+] XQT-AutoClockin Setup...'

echo '[1] Section1: Setup Python Env...)'
echo '[1] Run command:'$(pwd)'/InstallPython.sh'
source $(pwd)/InstallPython.sh

echo '[2] Section2: Setup crontab...'
echo '[2] Run command:'$(pwd)'/AddCron.sh'
source $(pwd)/AddCron.sh

echo '[!] setup end.'