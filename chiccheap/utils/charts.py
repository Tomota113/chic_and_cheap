def simple_bar_data(rows):
    return [(r['date'], r['total_ttc']) for r in rows]
