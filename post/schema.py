from pydantic import BaseModel


class CreatePost(BaseModel):
    post_name : str
    image : bytes
    description : str