from json import JSONDecodeError
from urllib.error import HTTPError

import requests

simple_headers = {
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


# Login
def login(email, password):
    try:
        fingerprint_json_data = {
            "operation": "userAuthEmail",
            "params": {
                "email": email,
                "otp": "",
                "password": password,
                "name": "",
            },
        }

        # Fingerprint
        fingerprint = requests.post("https://api.rytr.me/", headers=simple_headers, json=fingerprint_json_data).json()[
            "data"
        ]["fingerprint"]

        # Token
        token_json_data = {
            "operation": "userAuthLogin",
            "params": {
                "email": email,
                "otp": "",
                "password": password,
                "name": "",
                "fp": fingerprint,
            },
        }

        response = requests.post("https://api.rytr.me/", headers=simple_headers, json=token_json_data).json()["data"][
            "token"
        ]

        return response
    except (HTTPError, JSONDecodeError):
        print("An exception occurred")

    return None


def check_is_available(email, password):
    headers = {
        "authority": "api.rytr.me",
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authentication": f"Bearer {login(email, password)}",
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

    json_data = {
        "operation": "usageSummary",
    }

    response = requests.post("https://api.rytr.me/", headers=headers, json=json_data)

    # check for usage percentage, if it's 100% - return False
    if response.json()["data"]["usage"]["percentage"] == 100:
        return False
    else:
        return True


def get_token():
    from apps.users.models import User

    for user in User.objects.filter(is_staff=False):
        if check_is_available(user.email, user.password):
            return login(user.email, user.password)
        else:
            continue
    return None
