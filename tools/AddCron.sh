current_path=$(pwd)
python3_path=$(where python3 | grep /usr)

echo "[!] cronadd current path:" $current_path

mkdir $current_path/ShellOutput # create shell output folder
mkdir $current_path/ShellOutput/DO_NOT_DELETE_THIS_FOLDER # warning...info?

crontab -l | { cat; echo "\n# XQT-AutoClockin Works"; } | crontab -
crontab -l | { cat; echo "10 8 * * * $python3_path $current_path/Clockin.py >> \"$current_path/ShellOutput/\$(date +\"\\%Y-\\%m-\\%d_\\%H\").log\" 2>&1"; } | crontab -
crontab -l | { cat; echo "5 12 * * * $python3_path $current_path/Clockin.py >> \"$current_path/ShellOutput/\$(date +\"\\%Y-\\%m-\\%d_\\%H\").log\" 2>&1"; } | crontab -
crontab -l | { cat; echo "15 18 * * * $python3_path $current_path/Clockin.py >> \"$current_path/ShellOutput/\$(date +\"\\%Y-\\%m-\\%d_\\%H\").log\" 2>&1"; } | crontab -

service cron reload