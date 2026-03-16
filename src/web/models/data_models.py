from dataclasses import dataclass
from enum import Enum


class ViewType(Enum):
    """View display type"""

    GRID = "grid"
    TABLE = "table"


class ProjectType(Enum):
    """Project classification"""

    CLASSICAL = "Classical"
    BDD = "BDD"


@dataclass
class ProjectData:
    """Project information data model"""

    title: str
    url: str
    tests_count: int
    members_count: str
    project_type: str
