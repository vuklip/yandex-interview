import os

from requests import post, get, delete

from config import PETSTORE_URLS

PETSTORE_ENV = os.environ.get("ENV", "test")
URL = PETSTORE_URLS[PETSTORE_ENV]


def _request_post(url, data=None, json=None):
    response = post(url, data, json, timeout=15)
    return response


def _request_get(url, params):
    response = get(url, params)
    return response


def _request_delete(url, params):
    response = delete(url, params)
    return response


def post_pet(
    name: str,
    photo_urls: list,
    id: int = None,
    category: dict = None,
    tags: list = None,
    status: str = None,
):
    body = {
        "id": id,
        "category": category,
        "name": name,
        "photoUrls": photo_urls,
        "tags": tags,
        "status": status,
    }

    response = _request_post(URL + "/pet", json=body)
    return response


def get_pet(pet_id: str):
    pass


def delete_pet(pet_id: str):
    pass
