import pytest

from tests.test_data_const import NEW_PET_ID
from utils import api


@pytest.fixture
def delete_pet():
    yield
    api.delete_pet(NEW_PET_ID)
