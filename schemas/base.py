from typing import Annotated

from pydantic import StringConstraints

from schemas.constant import NAME_MAX_LENGTH, NAME_MIN_LENGTH


NameStr = Annotated[
    str,
    StringConstraints(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH)
    ]

NotesStr = Annotated[
    str,
    StringConstraints(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH)
]
