import requests

url = 'https://kyfw.12306.cn/passport/captcha/captcha-image'
params = {
    'login_site': 'E',
    'module': 'login',
    'rand': 'sjrand'
}

session = requests.session()
resp = session.get(url, params=params)
f = open('code.png', 'wb')
f.write(resp.content)
f.flush()
f.close()

point_map = {
    '1': '40,45',
    '2': '116,53',
    '3': '185,52',
    '4': '257,50',
    '5': '40,121',
    '6': '116,133',
    '7': '185,132',
    '8': '257,130'
}


def get_point(index):
    indexs = index.split(',')
    tmp = []
    for i in indexs:
        tmp.append(point_map[i])
    return ','.join(tmp)


code = get_point(input("请输入验证码:"))
print(code)

check_params = {
    'answer': code,
    'rand': 'sjrand',
    'login_site': 'E'
}

check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
code_result = session.get(check_url, params=check_params)
code_result.encoding = code_result.apparent_encoding
print(code_result.text)
