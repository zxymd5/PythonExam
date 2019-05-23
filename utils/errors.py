class UserError(object):
    UserNotFound = (300001, 'User Not Found')
    PasswordError = (300002, 'Password Error')
    VeriCodeError = (300003, 'Vericode Error')
    UserHasExists = (300004, 'User Has Exists')
    UserHasSentEmail = (300005, 'User Has Sent Email')
    UserSendEmailFailed = (300006, 'User Send Email Failed')
