import requests
import pytz
import datetime
from datetime import datetime
from pytz import timezone


def create_generator(users_data):
        for user in users_data["records"]:
            yield {
                'username': user["username"],
                'timestamp': user["timestamp"],
                'timezone': user["timezone"],
            }


def load_attempts():
    first_page = 1
    get_params = {"page": first_page}
    users_data = requests.get("http://devman.org/api/challenges/solution_attempts/",
                              params=get_params).json()
    pages = users_data["number_of_pages"]
    for user in create_generator(users_data):
        yield user
    for page in range(first_page, pages):
        get_params = {"page": page+1}
        users_data = requests.get("http://devman.org/api/challenges/solution_attempts/",
                                  params=get_params).json()
        for user in create_generator(users_data):
            yield user


def get_midnighters():
    owls_list = []
    for user in load_attempts():
        if user["timestamp"] is None:
            continue
        user_timezone =  user["timezone"]
        date = datetime.utcfromtimestamp(user["timestamp"])
        hour = timezone(user_timezone).fromutc(date).hour
        midnight, six_hours = 0, 6
        owls_list.append(user["username"])
    return set(owls_list)


def output_users(users_list):
    print("Список сов на дэвмане:")
    for user in users_list:
        print(user)


if __name__ == '__main__':
    users_list = get_midnighters()
    output_users(users_list)
