import requests
import pytz
import datetime
from datetime import datetime
from pytz import timezone

def load_attempts():
    request_data = requests.get("http://devman.org/api/challenges/solution_attempts/").json()
    pages = request_data["number_of_pages"]
    for page in range(pages):
        get_params = {"page": page+1}
        users_data = requests.get("http://devman.org/api/challenges/solution_attempts/",
                                                 params=get_params).json()
        for user in users_data["records"]:
            yield {
                'username': user["username"],
                'timestamp': user["timestamp"],
                'timezone': user["timezone"],
            }


def get_midnighters():
    hours_for_owls = [0,1,2,3,4,5]
    arr = []
    for user in load_attempts():
        if user["timestamp"] is None:
            continue
        user_timezone =  user["timezone"]
        date = datetime.utcfromtimestamp(user["timestamp"])
        hour = timezone(user_timezone).fromutc(date).hour
        if hour in hours_for_owls:
            arr.append(user["username"])
    return set(arr)


def output_users(users_list):
    print("Список сов на дэвмане:")
    for user in users_list:
        print(user)


if __name__ == '__main__':
    users_list = get_midnighters()
    output_users(users_list)
