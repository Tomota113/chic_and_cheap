from dataclasses import dataclass
from typing import Optional


@dataclass
class Vente:
    id: Optional[int]
    client_id: Optional[int]
    total_ht: float
    taxe: float
    remise_pct: float
    total_ttc: float
