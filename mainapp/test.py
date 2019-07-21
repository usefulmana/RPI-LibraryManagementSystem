import re

def gmail_check(user_email):
    regex = '^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$'
    return re.search(regex, user_email)


print(gmail_check("sdafdasf@gmail.com"))