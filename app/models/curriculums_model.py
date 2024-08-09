from pydantic import BaseModel, EmailStr #basemodel
from typing import Union #indica que el atributopuede ser de más de un tipo

class CVUserCreate(BaseModel):
    id:Union[int,None] = None
    user_id: int
    cv_id: int
    template_name: str
    color: str

class UserInformationCreate(BaseModel):
    cvid_user_template: int
    id_user: int
    name: str
    surname: str
    city: str
    municipality: str
    address: str
    colony: str
    postalCode: int
    phone: str
    email: str
    photo: Union[str, None] = None  # Agregamos el campo `photo`