import json
import os

import jsonschema

from config import ROOT


def get_schema(json_schema_name):
    """Вычитать из файла описание схемы

    Args:
        json_schema_name: Название файла схемы

    Returns:
        str: Описание json схемы

    """
    path = os.path.join(ROOT, "tests", "json_schemas", json_schema_name + ".json")

    with open(path, "r") as file:
        schema = file.read()

    return schema


def get_dict(json_data):
    """Конвертировать строку в dict

    Args:
        json_data (str): строка с содержанием json

    Returns:
        False - входная строка не валидна, dict - если данные валидны

    """
    try:
        json_data_dict = json.loads(json_data)
    except ValueError:
        return False
    return json_data_dict


def is_json_valid_by_scheme(json_data, json_schema_name):
    """Проверка валидации json по схеме

    Args:
        json_data (str): данные для валидации
        json_schema_name (str): название схемы валидации

    Returns:
        bool:
            True - валидация прошла успешно
            False - валидация с ошибкой

    """
    json_data_dict = get_dict(json_data)

    json_schema_data = get_schema(json_schema_name)
    json_schema_dict = get_dict(json_schema_data)

    try:
        jsonschema.validate(instance=json_data_dict, schema=json_schema_dict)
    except jsonschema.exceptions.ValidationError:
        return False
    return True


def ordered(obj):
    """Сортировка вложенных объектов

    Args:
        obj: объект для сортировки

    Returns:
        Отсортированный obj

    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

#todo очень плохая проверка для больших json- она возвращает только true/false, а в чем отличия нет
def is_json_the_same(json_one: str | bytes, json_two: str | bytes):
    """Проверка json на схожесть

    Args:
        json_one: первый json для сравнения
        json_two: второй json для сравнения

    Returns:
        bool:
            True: если одинаковы
            False: если различаются

    """

    if isinstance(json_one, bytes):
        json_one = json.loads(json_one.decode("utf-8"))
        json_one = ordered(json_one)
    else:
        json_one = json.loads(json_one)
        json_one = ordered(json_one)

    if isinstance(json_two, bytes):
        json_two = json.loads(json_two.decode("utf-8"))
        json_two = ordered(json_two)
    else:
        json_two = json.loads(json_two)
        json_two = ordered(json_two)

    return json_one == json_two


def get_value_by_key(str_or_dict, key_with_value):
    """Получить значения по ключу

    Args:
        str_or_dict: str или dict откуда взять значение по ключу
        key_with_value: ключ, значение которого нужно найти

    Returns:
        value: значение из ключа key_with_value
        None: если ключ не был найден
    """
    result = None

    if isinstance(str_or_dict, str):
        str_or_dict = get_dict(str_or_dict)

    if key_with_value in str_or_dict.keys():
        return str_or_dict[key_with_value]

    for key, value in str_or_dict.items():

        if isinstance(value, list):
            for item in value:
                result = get_value_by_key(item, key_with_value)
                if result is not None:
                    break

        elif type(value) is dict:
            result = get_value_by_key(value, key_with_value)

        if result is not None:
            return result

# todo возможно стоит работать не со сторокой в качестве ответа
def response_values(response_text: str, check_params: dict, partly=False):
    """Проверка значения(-ий) в поле(-ях) тела ответа

    Args:
        response_text: тело ответа
        check_params: параметры для проверки
        partly: флаг частичного сопоставления строк

    Returns:
        bool:
         False: если значение для проверки не найдено или не равно значению
         True: все остальные случаи

    """
    response_dict = get_dict(response_text)

    for key, value in check_params.items():
        value_from_response = get_value_by_key(response_dict, key)

        if partly:
            return value_from_response is not None and value in value_from_response
        else:
            return value_from_response is not None and value_from_response == value
