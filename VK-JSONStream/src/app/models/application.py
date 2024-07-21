from pydantic import BaseModel, Field

class Application(BaseModel): 
    kind: str = Field(..., title='kind', max_length=32)
    name: str = Field(..., title='name', max_length=128)
    description: str = Field(..., title='description', max_length=4096)
    version: str = Field(..., title='version', regex='^(0|[1-9]\\\\d*)\\\\.(0|[1-9]\\\\d*)\\\\.(0|[1-9]\\\\d*)(?:-((?:0|[1-9]\\\\d*|\\\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\\\.(?:0|[1-9]\\\\d*|\\\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\\\+([0-9a-zA-Z-]+(?:\\\\.[0-9a-zA-Z-]+)*))?$')
    configuration: dict = Field(..., title='configuration')
