from pydantic import BaseModel


class Weather(BaseModel):
    city: str
    output_format: str
