import requests
import pytz
import datetime
from datetime import datetime
from pytz import timezone


def load_attempts():
    page = 1
    get_params = {"page": page}
    users_data = requests.get("http://devman.org/api/challenges/solution_attempts/",
                              params=get_params).json()
    pages = users_data["number_of_pages"]
    first_page = 1
    for page in range(first_page, pages):
        for user in users_data["records"]:
            yield {
                'username': user["username"],
                'timestamp': user["timestamp"],
                'timezone': user["timezone"],
            }
        get_params = {"page": page+1}
        users_data = requests.get("http://devman.org/api/challenges/solution_attempts/",
                                  params=get_params).json()


def get_midnighters():
    owls_list = []
    for user in load_attempts():
        if user["timestamp"] is None:
            continue
        user_timezone =  user["timezone"]
        date = datetime.utcfromtimestamp(user["timestamp"])
        hour = timezone(user_timezone).fromutc(date).hour
        midnight, six_hours = 0, 6
        if hour >= midnight and hour < six_hours:
            owls_list.append(user["username"])
    return set(owls_list)


def output_users(users_list):
    print("Список сов на дэвмане:")
    for user in users_list:
        print(user)


if __name__ == '__main__':
    users_list = get_midnighters()
    output_users(users_list)
