IP_AGENT_ENABLED = False
EMAIL_ENABLED = False

EMAIL_RECEIVERS = ['example1@example.com', 'example2@example.com']
EMAIL_CC = [] # 抄送
EMAIL_BCC = [] # 密送

EMAIL_SENDER = {
    'SMTP_HOST': 'smtp.example.com',
    'SMTP_PORT': 465,
    'EMAIL_ADDRESS': 'example@example.com',
    'EMAIL_PASSWORD': 'example_password',
}