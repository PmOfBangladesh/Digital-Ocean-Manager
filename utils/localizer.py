REGIONS = {
    'nyc1': '🇺🇸 New York 1',
    'nyc2': '🇺🇸 New York 2',
    'nyc3': '🇺🇸 New York 3',
    'sfo1': '🇺🇸 San Francisco 1',
    'sfo2': '🇺🇸 San Francisco 2',
    'sfo3': '🇺🇸 San Francisco 3',
    'ams2': '🇳🇱 Amsterdam 2',
    'ams3': '🇳🇱 Amsterdam 3',
    'sgp1': '🇸🇬 Singapore 1',
    'lon1': '🇬🇧 London 1',
    'fra1': '🇩🇪 Frankfurt 1',
    'blr1': '🇮🇳 Bangalore 1',
    'tor1': '🇨🇦 Toronto 1',
    'syd1': '🇦🇺 Sydney 1',
}


def localize_region(slug: str) -> str:
    return REGIONS.get(slug, slug)
