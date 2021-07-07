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
python3 FakeUACacheCopy.py

echo '[!] Section2: Setup crontab...'

echo '[!] Run command:'$(pwd)'/AddCron.sh'
source $(pwd)/AddCron.sh

echo '[!] setup end.'