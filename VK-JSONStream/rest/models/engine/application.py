from pydantic import BaseModel, Field

class Application(BaseModel):
    kind: str = Field(..., default=Ellipsis, title='kind', max_length=32)
    name: str = Field(..., default=Ellipsis, title='name', max_length=128)
    description: str = Field(..., default=Ellipsis, title='description', max_length=4096)
    version: str = Field(..., default=Ellipsis, title='version', regex='^(\\d+\\.)?(\\d+\\.)?(\\*|\\d+)$')
    configuration: dict = Field(..., default=Ellipsis, title='configuration')
