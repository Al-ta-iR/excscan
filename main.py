# b = a[:8] + '-' + a[8:12] + '-' + a[12:16] + '-' + a[16:20] + '-' + a[20:]

from dotenv import load_dotenv  # ◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄ local
import os
import datetime as dt
import requests
import smtplib
import time
import re


# EMAIL_SENDER = os.environ.get('EMAIL_SENDER')  # ◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄ online ▼
# PASSWORD_EMAIL_SENDER = os.environ.get('PASSWORD_EMAIL_SENDER')
# EMAIL_RECIEVER = os.environ.get('EMAIL_RECIEVER')
# SITE_DATA = os.environ.get('SITE_DATA')
# PAGE_ID_SITE_DATA = os.environ.get('PAGE_ID_SITE_DATA')  # ◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄ ▲


env_path = os.path.join('secrets.env')  # ◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄ local ▼
load_dotenv(env_path)
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
PASSWORD_EMAIL_SENDER = os.getenv('PASSWORD_EMAIL_SENDER')
EMAIL_RECIEVER = os.getenv('EMAIL_RECIEVER')
SITE_DATA = os.getenv('SITE_DATA')
PAGE_ID_SITE_DATA = os.getenv('PAGE_ID_SITE_DATA')  # ◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄ ▲
PAGE_ID_SITE_DATA_HUB_MANUAL = os.getenv('PAGE_ID_SITE_DATA_HUB_MANUAL')  # ◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄ ▲


def finder_text(content, flag, board):
    left_id_position = content.find(flag) + len(flag)
    right_id_position = content[left_id_position : ].find(board) + left_id_position
    text = content[left_id_position : right_id_position]
    return text, right_id_position


def get_data_from_hub(all_data):
    needs_data = (  # порядок не менять, так приходит из Notion и так понятнее работать поэтому)!
        'email_flag', 'mailto:',
        'server_flag', 'h@tm":[["',
        'password_flag', 'udad":[["',
        'url_flag', '{>sO":[["',
    )
    find_id_position_email = all_data.find('>w[J":[["') + len(needs_data[1])
    all_data = all_data[find_id_position_email:]
    all_urls_data = []
    while needs_data[1] in all_data:
        for i in range(1, len(needs_data), 2):
            value, end_position = finder_text(all_data, needs_data[i], '"')
            all_urls_data.append(value.strip())
            all_data = all_data[end_position + 1:]
    return all_urls_data


def get_hub_data(SITE_DATA, hub_url):
    json_data = {
        'page': {
            'id': PAGE_ID_SITE_DATA,
        },
        'limit': 100,
        'chunkNumber': 0,
        'verticalColumns': False,
    }
    try:
        response = requests.post(SITE_DATA, json=json_data, allow_redirects=True)
    except Exception as e:
        print(e)
        x = input('Нажмите Enter, чтобы закрыть программу: ')
        os._exit(0)
    data = str(response.text)
    return data


def check_version(current_version, data):
    new_version, right_position = finder_text(data, '• Version: [', ']')
    if new_version != current_version:
        flag = input(f"Есть обновление tool, version=[{new_version}]. Скачать можно отсюда: https://drive.google.com/drive/\nЛибо нажми Enter для продолжения в этой версии: \n")


if __name__ == "__main__":
    start_time = time.time()
    while 1:  # manual ▼
        try:
            data = get_hub_data(PAGE_ID_SITE_DATA_HUB_MANUAL)
            current_version = check_version(version, data)
            email_flag_enter = input(f"▓▓▓ Данные для проверок находятся здесь: http\nНажми Enter для продолжения: ")
            check_data = get_data_from_hub(data)
            print(check_cross_servers_login(check_data))
        except Exception as e:
            print(e)
        print("\n--- %s seconds ---\n" % round((time.time() - start_time), 2))
        start_time = time.time()
