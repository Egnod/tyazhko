from typing import List

from tyazhko.components.links.api import router
from tyazhko.components.links.crud import CRUDS

COLLECTIONS: List[str] = [crud.collection for crud in CRUDS]
