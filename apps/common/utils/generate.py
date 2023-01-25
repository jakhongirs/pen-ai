from json import JSONDecodeError
from urllib.error import HTTPError

import requests

from apps.common.utils.login import get_token


def generate_content(language, text):
    try:
        headers = {
            "authority": "api.rytr.me",
            "accept": "application/json, text/plain, */*",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "authentication": "Bearer " + get_token(),
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
            "operation": "generateExecute",
            "params": {
                "driveIdFolder": None,
                "driveIdFile": "",
                "typeId": "6062d819be972a000c6a05a3",
                "toneId": "60572a639bdd4272b8fe358b",
                "languageId": language,
                "contextInputs": {
                    "POST_TOPIC_LABEL": text,
                },
                "variations": 3,
                "creativityLevel": "default",
            },
        }

        response = requests.post("https://api.rytr.me/", headers=headers, json=json_data)

        return response.json()
    except (HTTPError, JSONDecodeError):
        print("Error: generate_content()")
