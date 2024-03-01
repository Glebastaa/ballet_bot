class DoesNotExist(Exception):
    """Raised when an entity does not exist."""

    def __init__(self, id):
        message = f'Entity with id: {id} does not exist.'
        super().__init__(message)


class EntityAlreadyExists(Exception):
    """Raised when an entity already exists."""

    def __init__(self, entity_type: str, entity_data: dict):
        message = f'{entity_type} with data {entity_data} already exists.'
        super().__init__(message)


class IndivIsFull(Exception):
    """Raised when try to add > 2 students to indiv."""

    def __init__(self, entity_data: dict):
        message = f'Indiv {entity_data} is full (max 2 students).'
        super().__init__(message)


class InvalidIsIndividual(Exception):
    """Exception indicating an invalid value
    for the 'is_individual' attribute."""

    def __init__(self):
        message = 'Invalid value for "is_individual" attribute'
        super().__init__(message)


class ScheduleTimeInsertionError(Exception):
    """raised when attempting to insert
    a time into the schedule with insufficient
    gap between existing times."""

    def __init__(self):
        message = 'Unable to insert the new time at schedule. Time is busy.'
        super().__init__(message)
