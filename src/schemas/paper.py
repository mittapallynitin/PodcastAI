from pydantic import BaseModel, Field


class PaperBase(BaseModel):
    link: str = Field(..., description="The link to the paper to be processed")
