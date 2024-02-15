import requests
import time

def get_refresh_token():
    url = 'https://openapi.alipan.com/oauth/authorize/qrcode'

    data = {
        "client_id": "d1af8f792c15469b9c3b35cba10dad3b",
        "client_secret": "cfc7beea544c463997e169e80a74b837",
        "scopes": ["user:base", "file:all:read"],
        "width": 430,
        "height": 430
    }

    response = requests.post(url, json=data)

    qr_code_url = response.json()['qrCodeUrl']
    sid = response.json()['sid']

    print(f'请扫描二维码进行登录：{qr_code_url}')

    while True:
        status_check_url = f'https://openapi.alipan.com/oauth/qrcode/{sid}/status'
        status_response = requests.get(status_check_url)

        status = status_response.json()['status']

        if status == 'QRCodeExpired':
            print('二维码已过期，请重新扫描')
            get_refresh_token()
        elif status == 'LoginSuccess':
            auth_code = status_response.json()['authCode']
            break
        else:
            time.sleep(1)

    token_url = 'https://openapi.alipan.com/oauth/access_token'

    token_data = {
        "client_id": "d1af8f792c15469b9c3b35cba10dad3b",
        "client_secret": "cfc7beea544c463997e169e80a74b837",
        "grant_type": "authorization_code",   
        "code": auth_code
    }

    token_response = requests.post(token_url, json=token_data)
    print(token_response.json())  # Add this line
    access_token = token_response.json()['accessToken']
    refresh_token = token_response.json()['refreshToken']

    print(f'Access Token: {access_token}\nRefresh Token: {refresh_token}')

get_refresh_token()