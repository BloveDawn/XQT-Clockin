#!/bin/zsh

# Author: Blovedawn
# Release Date: 2021.6

# Clone from github

git clone https://github.com/BloveDawn/XQT-Clockin.git

# go to XQT-AutoClockin folder

cd $(pwd)/XQT-Clockin

# Setup
echo '[!] XQT-AutoClockin Setup...'
echo '[!] Section1: Setup Python Env...)'

python3_path=$(where python3)
pip3_path=$(where pip3)

if [ "$python3_path" -o "$pip3_path" ]
then
    echo "[+] python3 path is set to" $python3_path"."
    echo "[+] pip3 path is set to" $pip3_path"."
else
    echo "[-] python3 or pip3 path is null, setup abort."
    exit
fi

pip3 install requests
pip3 install fake_useragent

echo '[!] Section2: Setup crontab...'

current_path=$(pwd)

mkdir $current_path/ShellOutput # create shell output folder
mkdir $current_path/ShellOutput/DO_NOT_DELETE_THIS_FOLDER # warning...info?

crontab -l | { cat; echo "\n# XQT-AutoClockin Works"; } | crontab -
crontab -l | { cat; echo "10 8 * * * $python3_path $current_path/Clockin.py >> \"$current_path/ShellOutput/\$(date +\"\\%Y-\\%m-\\%d_\\%H\").log\" 2>&1"; } | crontab -
crontab -l | { cat; echo "5 12 * * * $python3_path $current_path/Clockin.py >> \"$current_path/ShellOutput/\$(date +\"\\%Y-\\%m-\\%d_\\%H\").log\" 2>&1"; } | crontab -
crontab -l | { cat; echo "15 18 * * * $python3_path $current_path/Clockin.py >> \"$current_path/ShellOutput/\$(date +\"\\%Y-\\%m-\\%d_\\%H\").log\" 2>&1"; } | crontab -

service cron reload

echo '[!] setup end.'