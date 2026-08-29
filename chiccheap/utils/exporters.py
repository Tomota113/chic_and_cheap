from pathlib import Path
from typing import List, Tuple


def export_ticket_txt(path: Path, lignes: List[Tuple[str, int, float]], total: float) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        f.write('Chic and Cheap
')
        f.write('-----------
')
        for nom, qte, prix in lignes:
            f.write(f"{nom} x{qte} @ {prix:.2f}
")
        f.write('-----------
')
        f.write(f'Total: {total:.2f}
')
