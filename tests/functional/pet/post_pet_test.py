from pytest import mark

from tests.test_data_const import NEW_PET_ID
from utils import api
from utils.const_error import INV_RESP_CODE
from utils.data_utils import is_json_valid_by_scheme, response_values, is_json_the_same


@mark.positive
@mark.parametrize(
    "name, photo_urls",
    [
        (
            "king kong",
            [
                "https://commons.wikimedia.org/wiki/File:King_Kong_1933_Promotional_Image.png#/media/File:King_Kong_1933_Promotional_Image.png"
            ],
        )
    ],
)
# todo: здесь НЕ происходит удаление созданного pet
def test_post_pet_positive_short(name, photo_urls):
    """Проверка работы POST /pet с минимальным количеством параметров"""
    response = api.post_pet(name, photo_urls)

    assert response.status_code == 200, INV_RESP_CODE
    assert is_json_valid_by_scheme(response.text, "post_pet")
    # todo проверяем не все тело, а только одно поле?
    assert response_values(response.text, {"name": "king kong"})


@mark.positive
@mark.parametrize(
    #todo довольно сомнительная параметризация, почему просто не передать тело в качестве параметра? тогда предыдущий тест можно объединить с этим
    "name, photo_urls, id, category, tags, status",
    [
        (
            "Peregrine falcon",
            [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Falco_peregrinus_-_01.jpg/2880px-Falco_peregrinus_-_01.jpg"
            ],
            NEW_PET_ID,
            {"id": 28259559, "name": "deserunt ea ullamco"},
            [
                {"id": 99781532, "name": "adipisicing ullamco laborum quis"},
                {"id": -7620059, "name": "elit"},
            ],
            "perfect",
        )
    ],
)
def test_post_pet_positive_full(
    name, photo_urls, id, category, tags, status, delete_pet
):
    """Проверка работы POST /pet со всеми параметрами"""
    response = api.post_pet(name, photo_urls, id, category, tags, status)

    assert response.status_code == 200, INV_RESP_CODE
    # todo зачем проверять схемы/конкретное поле если дальше ты польностью проверяешь все тело?
    assert is_json_valid_by_scheme(response.text, "post_pet")
    assert response_values(response.text, {"name": "Peregrine falcon"})
    assert is_json_the_same(response.text, response.request.body)


@mark.negative
def test_post_pet_without_required_field():
    """Проверка работы POST /pet без минимальным количеством параметров

    Обязательные параметры "name" и "photo_urls"
    """
    response = api.post_pet(name=None, photo_urls=None)

    assert response.status_code == 405, INV_RESP_CODE
