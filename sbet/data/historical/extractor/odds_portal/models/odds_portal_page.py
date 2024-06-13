from dataclasses import dataclass
from typing import FrozenSet

from sbet.data.historical.extractor.odds_portal.models.odds_portal_row import OddsPortalRow


@dataclass(frozen=True)
class OddsPortalPage:
    page: int
    pageCount: int
    rows: FrozenSet[OddsPortalRow]
