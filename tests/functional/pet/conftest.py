import pytest

from tests.test_data_const import NEW_PET_ID
from utils import api

#todo довольно неуниверсальная фикстура которая удаляет всегда только NEW_PET_ID
@pytest.fixture
def delete_pet():
    yield
    api.delete_pet(NEW_PET_ID)
