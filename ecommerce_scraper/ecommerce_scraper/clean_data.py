def format_price(s, *subs):
    for sub in subs:
        s = s.rstrip(sub)
    return float(s.replace(' ', '').replace(',', '.'))