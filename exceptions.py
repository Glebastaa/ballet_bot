class DoesNotExist(Exception):
    """Raised when an entity does not exist."""

    def __init__(self, message="Entity does not exist."):
        self.message = message
        super().__init__(self.message)


class EntityAlreadyExists(Exception):
    """Raised when an entity already exists."""

    def __init__(self, message="Entity already exists."):
        self.message = message
        super().__init__(self.message)
