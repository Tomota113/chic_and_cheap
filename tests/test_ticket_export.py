from pathlib import Path

from chiccheap.utils.exporters import export_ticket_txt


def test_ticket_export(tmp_path):
    path = tmp_path / 'ticket.txt'
    export_ticket_txt(path, [('Test', 2, 10.0)], 20.0)
    assert path.exists()
    content = path.read_text(encoding='utf-8')
    assert 'Test' in content and '20.00' in content
