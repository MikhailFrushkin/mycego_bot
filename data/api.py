import json

import requests

from data.config import domain


def check_user_api(username, password):
    url = f'{domain}/api-auth/login/'
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()
    return None


def create_or_get_apport(date, start_time, end_time, user_id_site):
    url = f'{domain}/api-auth/appointment/'
    data = {'date': date, 'start_time': start_time, 'end_time': end_time, 'user': user_id_site}
    response = requests.post(url, data=data)
    return response.status_code


def get_appointments(user_id_site):
    url = f'{domain}/api-auth/appointment/'
    data = {'user': user_id_site}
    response = requests.get(url, data=data)
    if response.status_code == 200:
        return response.json()
    return None


def delete_appointments(user_id_site, id_row):
    url = f'{domain}/api-auth/appointment_delete/'
    data = {'user': user_id_site, 'id': id_row}
    response = requests.post(url, data=data)
    return response.status_code


def get_works():
    url = f'{domain}/api-auth/get_works/'
    response = requests.get(url)
    return response.json()


def post_works(date, user_id_site, works):
    url = f'{domain}/api-auth/add_works/'
    data = {'date': date, 'user': user_id_site, 'works': works}
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    return response.status_code


if __name__ == '__main__':
    check_user_api('admin', 'fma160392')
