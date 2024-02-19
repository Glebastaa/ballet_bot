import pytest


@pytest.fixture
def student_name():
    return 'sasuke'


@pytest.fixture
def studio_names():
    return {
        'studio_one': 'strana ognya',
        'studio_two': 'strana wodi'
    }


@pytest.fixture
def group_name():
    return 'konoha'