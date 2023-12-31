import json
from pprint import pprint

import requests
from loguru import logger

from data.config import domain
from data.db import Works


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


def post_works(date, user_id_site, works, delivery=None, comment=None):
    url = f'{domain}/api-auth/add_works/'
    data = {'date': date, 'user': user_id_site, 'works': works, 'delivery': delivery, 'comment': comment}
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    return response.status_code


def get_works_lists(user_id_site):
    url = f'{domain}/api-auth/view_works/'
    data = {'user': user_id_site}
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, data=json_data, headers=headers)
    return response.json()


def get_details_works_lists(work_id):
    url = f'{domain}/api-auth/view_detail_work/'
    data = {'work_id': work_id}
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, data=json_data, headers=headers)
    return response.json()


def del_works_lists(work_id, user_id):
    url = f'{domain}/api-auth/view_detail_work/'
    data = {'work_id': work_id, 'user_id': user_id}
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    return response.status_code


def get_delivery():
    url = f'{domain}/api-auth/get_delivery/'
    response = requests.get(url)
    return response.json().get('data', None)


def get_data_delivery(user_id):
    url = f'{domain}/api-auth/get_list_delivery/'
    data = {'user_id': user_id}
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, data=json_data, headers=headers)
    return response.json()


def generate_works_base():
    data = get_works().get('data')
    if data:
        Works.delete().execute()
        for i in data:
            Works.create(id=i[0], name=i[1], delivery=i[2], standard=i[3])


def get_statistic(user_id):
    url = f'{domain}/api-auth/statistic/'
    data = {'user_id': user_id}
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, data=json_data, headers=headers)
    return response


def get_request(user_id):
    url = f'{domain}/api-auth/request/'
    data = {'user_id': user_id}
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, data=json_data, headers=headers)
    return response.json()


def post_request(user_id, type_r, comment):
    url = f'{domain}/api-auth/request/'
    data = {'user_id': user_id, 'type_r': type_r, 'comment': comment}
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    return response.status_code


if __name__ == '__main__':
    # check_user_api('admin', 'fma160392')
    get_statistic(1)