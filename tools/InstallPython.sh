
python3_path=$(where python3 | grep /usr)
pip3_path=$(where pip3 | grep /usr)

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
