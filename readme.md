# XQT-Auto-Clockin

> I am sorry that I cannot provide the Chinese version of the documentation because it is dangerous.

## Introduction

This is an automatic check-in script of Shanxi Xiao Qi Tong, which can realize multi-user automatic check-in.

## Use

### Note

This script can run on any operating system, but I recommend using a cloud server for deployment, which will save you the trouble of starting this script every day.

You can use `XQT-AutoSetup.sh` to **AUTO** init env and setup.

`curl -fsSL "https://raw.githubusercontent.com/BloveDawn/XQT-Clockin/main/XQT-AutoSetup.sh" | zsh`

> **Note: You need `zsh` to run this shell script.**  
> Install zsh: `apt install zsh`

### 1.You need a VPS server

You can purchase student plan cloud servers from cloud service providers such as Baidu Cloud, Huawei Cloud, Alibaba Cloud, and Tencent Cloud.

It will be quite cheap. (About $14 a year)

Good luck.

### 2.Deploy the script on the server

- Install python environment
- Install dependencies
  - `pip install requests`
  - `pip install fake_useragent`

### 3.Enter information

Write the personal information of the person who needs to sign in to the file 'id_save.txt' in the following format

> id_save.txt

```text
140501199801010000:山西省某市某区某学校地址
140501199801010001:山西省某市某区某学校地址
140501199801010002:山西省某市某区某学校地址
```

> Note: **The two characters "市" and "省" are important classification basis, PLEASE DO NOT OMIT !**
>
> Warning: **Submitting with non-existent data will cause the server to report an error !!!**

### 4.Test run this script

- `python3 Clockin.py`

### 5.Run this script regularly on the cloud server

- You can use `XQT-AutoSetup.sh` to init env and setup.
  - Run with command `./XQT-AutoSetup.sh`
  - **Note: You need `zsh` to run this shell script.**
  - Install zsh:`apt install zsh`

> Take ubuntu as an example below.

- Edit crontab
  - `crontab -e`
- Add 3 timed clocks in the morning, noon and evening respectively
  - `15 8 * * * /usr/bin/python3.6 /path/to/XQTClockin/Clockin.py`
  - `15 12 * * * /usr/bin/python3.6 /path/to/XQTClockin/Clockin.py`
  - `15 18 * * * /usr/bin/python3.6 /path/to/XQTClockin/Clockin.py`
- Reload cron
  - `service cron reload`

### 6.Success

So far everything is perfect, you can have a cup of coffee and wait for the cloud server to automatically clock in for you

## Logging

This script will record all check-in logs in the folder 'ClockinLogArchive' under the current running directory.

The format of the file name written is 'UnixTimestamp_IDNumber.log'.

If a major error that cannot be checked in occurs, an'imp_error.log' file will be generated in the running directory. If such an error occurs in the future, the content will be appended to this file.

## Uninstall

- Remove folder XQT-Clockin
- Remove added cron table (Use `crontab -e`)
- Remove python package
  - requests
  - fake_useragent

## Q-A

If you have any other questions, please open an issue to ask, I will answer as soon as possible.
