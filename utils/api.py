import os

from requests import post, get, delete

from config import PETSTORE_URLS
from utils.logger import logged_request_response

PETSTORE_ENV = os.environ.get("ENV", "test")
URL = PETSTORE_URLS[PETSTORE_ENV]

# todo: это плохая идея, есть еще PATCH, PUT и прочее? Возможно стоит как-то лучше продумать этот клиент
@logged_request_response
def _request_post(url, data=None, json=None):
    response = post(url, data, json, timeout=15)
    return response


@logged_request_response
def _request_get(url, params=None):
    response = get(url, params)
    return response

@logged_request_response
def _request_delete(url, params=None):
    response = delete(url)
    return response


#todo это плохая идея передавать поля тела как параметры в этот метод
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


def get_pet(pet_id: int):
    response = _request_get(URL + "/pet" + f"/{pet_id}")
    return response


def delete_pet(pet_id: int):
    response = _request_delete(URL + "/pet" + f"/{pet_id}")
    return response
