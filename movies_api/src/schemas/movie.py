from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import date

class MovieBase(BaseModel):
    title: str | None = Field(default=None, min_length = 2, max_length = 200)
    genre: str | None = Field(default=None, min_length = 2, max_length = 100)
    rating: float | None = Field(default=None, ge=0, le=10)
    year: int | None = None
    
    @field_validator("year")
    @classmethod
    def year_in_range(cls, year:int) -> int:
        if year is None:
            return year
        if not(1998 <= year <= date.today().year):
            raise ValueError(f"Год должен быть между 1998 и {date.today().year}")
        return year

class MovieCreate(MovieBase):
    title: str  = Field(...,  min_length=2, max_length=200)
    genre: str = Field(..., min_length=2, max_length=100)
    rating: float  = Field(..., ge=0, le=10)
    year: int = Field(..., ge=1998, le=date.today().year)

class MovieUpdate(MovieBase):
    pass

class MovieOut(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
    