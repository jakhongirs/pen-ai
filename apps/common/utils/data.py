from json import JSONDecodeError
from urllib.error import HTTPError

import requests

from apps.common.utils.login import get_token

post_headers = {
    "authority": "api.rytr.me",
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "origin": "https://app.rytr.me",
    "referer": "https://app.rytr.me/",
    "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/109.0.0.0 Safari/537.36",
}


# Language list
def language_list():
    try:
        headers = post_headers.update({"authentication": "Bearer " + get_token()})
        json_data = {
            "operation": "languageList",
        }

        response = requests.post("https://api.rytr.me/", headers=headers, json=json_data)

        return response.json()
    except (HTTPError, JSONDecodeError):
        print("Error: language_list()")

    return None


# Tone list
def tone_list():
    try:
        headers = post_headers.update({"authentication": "Bearer " + get_token()})
        json_data = {
            "operation": "toneList",
        }

        response = requests.post("https://api.rytr.me/", headers=headers, json=json_data)

        return response.json()
    except (HTTPError, JSONDecodeError):
        print("Error: tone_list()")

    return None


# Use case list
def use_case_list():
    try:
        headers = post_headers.update({"authentication": "Bearer " + get_token()})
        json_data = {
            "operation": "typeList",
        }

        response = requests.post("https://api.rytr.me/", headers=headers, json=json_data)

        return response.json()
    except (HTTPError, JSONDecodeError):
        print("Error: use_case_list()")

    return None
