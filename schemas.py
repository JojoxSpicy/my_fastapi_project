from pydantic import BaseModel, EmailStr, Field, validator
from pydantic.networks import EmailStr

class UserCreate(BaseModel):
    name: str  # Usamos 'str' y aplicamos la validación manualmente
    
    email: EmailStr  # Email validado con la clase EmailStr
    
    age: int = Field(..., ge=0, description="La edad debe ser un número positivo.")  # ge=0 para garantizar que sea >= 0
    
    @validator('name')
    def validate_name(cls, v):
        # Asegurarse de que solo tenga letras y espacios
        if not v.isalpha() and not all(c.isspace() for c in v):
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v

    class Config:
        # Esto asegura que los datos sean correctamente validados y convertidos a sus tipos correspondientes
        orm_mode = True


