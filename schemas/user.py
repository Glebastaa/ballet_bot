from pydantic import BaseModel

from database.models import UserRoles


class UserSchemaBase(BaseModel):
    id: int
    username: str
    role: UserRoles


class UserSchema(UserSchemaBase):
    pass


class UserSchemaAdd(UserSchemaBase):
    pass


class UserSchemaUpdateRole(BaseModel):
    role: UserRoles
