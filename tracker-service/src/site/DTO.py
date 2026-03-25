from dataclasses import dataclass
from datetime import datetime


@dataclass
class SiteDTO:
    id: int
    url: str
    hash: str
    created_at: datetime
    updated_at: datetime
