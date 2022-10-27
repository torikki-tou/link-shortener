from typing import Optional

from pydantic import BaseModel, AnyUrl


class LinkBase(BaseModel):
    uri: Optional[AnyUrl] = None


class LinkCreate(LinkBase):
    uri: AnyUrl


class LinkUpdate(LinkBase):
    uri: Optional[AnyUrl] = None


class LinkInDBBase(LinkBase):
    id: str
    owner_id: str
    short_urn: str


class Link(LinkInDBBase):
    pass


class LinkInDB(LinkInDBBase):
    pass
