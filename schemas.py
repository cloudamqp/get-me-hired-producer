from pydantic import BaseModel


class JobsQueryModel(BaseModel):
    """ Defines the allowed format of job queries """
    search_term: str
    location: str
    email: str

    class Config:
        schema_extra = {
            "example": {
                "search_term": "Junior Python Engineer", 
                "location": "Nigeria",
                "email": "spongebob@gmail.com"
            }
        }