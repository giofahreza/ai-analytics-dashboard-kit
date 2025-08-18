# Constants for the TINSIG AI Dashboard

KABUPATEN_OPTIONS = [
    "Jakarta",
    "Bandung", 
    "Surabaya",
    "Medan",
    "Semarang",
    "Makassar",
    "Palembang",
    "Tangerang",
    "Depok",
    "Bekasi"
]

CHART_THEMES = [
    "Default",
    "plotly",
    "plotly_white", 
    "plotly_dark",
    "ggplot2",
    "seaborn",
    "simple_white"
]

MINING_TYPES = [
    "Timah",
    "Emas", 
    "Batubara",
    "Nikel",
    "Bauksit",
    "Tembaga",
    "Besi",
    "Pasir"
]

API_ENDPOINTS = {
    "backend_url": "http://localhost:8000",
    "source1_url": "http://localhost:8001",  # Illegal Mining
    "source2_url": "http://localhost:8002",  # Production
    "source3_url": "http://localhost:8003"   # IUP
}

MAP_STYLES = {
    "OpenStreetMap": "OpenStreetMap",
    "Satellite": "Esri.WorldImagery", 
    "Terrain": "OpenTopoMap"
}

COLOR_PALETTES = {
    "Default": "viridis",
    "Viridis": "viridis",
    "Plasma": "plasma", 
    "Inferno": "inferno",
    "Magma": "magma"
}
