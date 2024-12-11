import pydantic


class User(pydantic.BaseModel):
    id: int = pydantic.Field(default=0)
    name: str = pydantic.Field(default="")
    password: str = pydantic.Field(default="")
    email: str = pydantic.Field(default="")
    sweethearts_id: int = pydantic.Field(default=0)