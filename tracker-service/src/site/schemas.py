from pydantic import BaseModel, ConfigDict, HttpUrl


class SSiteCreate(BaseModel):
    """
    Schema for creating a new site.

    Attributes:
        url: Site URL (validated HttpUrl).
        hash: Content hash of the site.
    """

    url: HttpUrl
    hash: str


class SSiteDTO(BaseModel):
    """
    Data Transfer Object for site entity.

    Attributes:
        id: Unique identifier of the site.
        url: Site URL.
        hash: Current content hash of the site.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    hash: str
