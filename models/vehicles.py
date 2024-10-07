from pydantic import BaseModel, Field


class Vehicle(BaseModel):
    vehicle_model : str
    vehicle_company : str
    vehicle_number : int
    rented : bool = Field(False)
    price : float