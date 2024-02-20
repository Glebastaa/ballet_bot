from datetime import datetime
import pytest

from database.models import WeekDays


# Studio.

@pytest.fixture
def student_name():
    return 'Саске'


@pytest.fixture
def first_studio():
    return 'Страна огня'


@pytest.fixture
def second_studio():
    return 'Страна воды'


@pytest.fixture
def new_studio_data():
    return {
            'id': 1,
            'new_name': 'Страна земли'
        }


# Group.

@pytest.fixture
def first_group():
    return {
        'name': 'Коноха',
        'studio_id': 2,
        'time': datetime.strptime('10:23', "%H:%M").time(),
        'date': WeekDays.monday
    }


@pytest.fixture
def second_group():
    return {
        'name': 'Киригакурэ',
        'studio_id': 2,
        'time': datetime.strptime('16:43', "%H:%M").time(),
        'date': WeekDays.friday
    }
