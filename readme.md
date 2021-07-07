# XQT-Auto-Clockin

> I am sorry that I cannot provide the Chinese version of the documentation because it is dangerous.

## Introduction

This is an automatic check-in script of Shanxi Xiao Qi Tong, which can realize multi-user automatic check-in.

## Deploy

### Note

This script can run on any operating system, but I recommend using a cloud server for deployment, which will save you the trouble of starting this script every day.

### You need a VPS server

You can purchase student plan cloud servers from cloud service providers such as Baidu Cloud, Huawei Cloud, Alibaba Cloud, and Tencent Cloud.

It will be quite cheap. (About $14 a year)

Good luck.

### Automatic deploy and start

> **It's tested on Ubuntu(Arm64) Server.**
>
> **If you set it up through this automatic installation script, you don’t need to refer to the following steps**

You can use `XQT-AutoSetup.sh`(International) or `XQT-AutoSetup-Gitee.sh`(mainland China) to **AUTOMATIC** initialize environment and setup.

> **Note: You need `zsh`&`git`&`python3`&`pip` to run this shell script.**  
> first, install: `sudo apt install zsh git python3 python3-pip`
>
> If you are from **mainland China**, using the **Gitee** link below will speed up deployment.

1. download and automatic deploy
   - from Gitee(China): `curl -fsSL "https://gitee.com/blovedawn/XQT-Clockin/raw/main/XQT-AutoSetup-Gitee.sh" | zsh`
   - from GitHub: `curl -fsSL "https://raw.githubusercontent.com/BloveDawn/XQT-Clockin/main/XQT-AutoSetup.sh" | zsh`
2. enter information
   - Write the personal information of the person who needs to sign in to the file (default file name is 'id_save.txt') in the following format
   - > id_save.txt

     ```text
     140501199801010000:山西省某市某区某学校地址:remarks1
     140501199801010001:山西省某市某区某学校地址:remarks2
     140501199801010002:山西省某市某区某学校地址:remarks3
     ```

   - > Note: **The two characters "市" and "省" are important classification basis, PLEASE DO NOT OMIT !**
     >
     > Warning: **Submitting with non-existent data will cause the server to report an error !!!**
3. all done! enjoy it!

> Warning: **DO NOT DELETE FOLDER** `/path/to/XQT-Clockin/ShellOutput`

### Manually deploy the script on the server

1. install git by `apt install git`
2. clone repositories
   1. `git clone https://github.com/BloveDawn/XQT-Clockin.git`(International)
   2. `git clone https://gitee.com/blovedawn/XQT-Clockin.git`(mainland China)
3. install python environment by `apt install python3`
4. install pip by `apt install pip3`
5. install dependencies
   - `pip install requests`
   - `pip install fake_useragent`

#### Enter information

Write the personal information of the person who needs to sign in to the file (default file name is 'id_save.txt') in the following format.

- rename **id_save_sample.txt** to **id_save.txt**

> id_save.txt

```text
140501199801010000:山西省某市某区某学校地址:remarks1
140501199801010001:山西省某市某区某学校地址:remarks3
140501199801010002:山西省某市某区某学校地址:remarks4
```

> Note: **The two characters "市" and "省" are important classification basis, PLEASE DO NOT OMIT !**
>
> Warning: **Submitting with non-existent data will cause the server to report an error !!!**

#### Test run this script

- `python3 Clockin.py`

#### Run this script regularly on the cloud server

> take ubuntu as an example below.

- edit crontab
  - `crontab -e`
- add 3 timed clocks in the morning, noon and evening respectively
  - `15 8 * * * /usr/bin/python3.6 /path/to/XQTClockin/Clockin.py`
  - `15 12 * * * /usr/bin/python3.6 /path/to/XQTClockin/Clockin.py`
  - `15 18 * * * /usr/bin/python3.6 /path/to/XQTClockin/Clockin.py`
- reload cron
  - `service cron reload`

#### Success

So far everything is perfect, you can have a cup of coffee and wait for the cloud server to automatically clock in for you.

## Update

- `git pull`

## Logging

1. This script will record all check-in logs in the folder 'ClockinLogArchive' under the current running directory.
   - The format of the file name written is 'time_remarks.log'.
2. The console output is in folder `ShellOutput`.

## Uninstall

- remove folder XQT-Clockin
- remove added cron table (Use `crontab -e`)
- remove python package
  - requests
  - fake_useragent

## Q-A

If you have any other questions, please open an issue to ask, I will answer as soon as possible.
