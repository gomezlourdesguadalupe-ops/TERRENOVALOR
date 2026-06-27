"""
Datos de referencia de zonas para la tasación.
Reemplazá estos valores por tus propios datos reales (precio por m² de mercado).
"""

# Cada zona tiene: nombre, coordenadas centrales (lat, lon), precio base por m² en USD
# y un radio aproximado de cobertura en km (para el matching por cercanía).
ZONAS = [
    {
        "id": "zona_centro",
        "nombre": "Centro",
        "lat": -34.6037,
        "lon": -58.3816,
        "precio_base_m2": 1200.0,
        "radio_km": 3,
    },
    {
        "id": "zona_norte",
        "nombre": "Zona Norte",
        "lat": -34.5100,
        "lon": -58.4900,
        "precio_base_m2": 950.0,
        "radio_km": 5,
    },
    {
        "id": "zona_sur",
        "nombre": "Zona Sur",
        "lat": -34.7200,
        "lon": -58.3500,
        "precio_base_m2": 600.0,
        "radio_km": 5,
    },
    {
        "id": "zona_oeste",
        "nombre": "Zona Oeste",
        "lat": -34.6500,
        "lon": -58.6500,
        "precio_base_m2": 500.0,
        "radio_km": 6,
    },
]

# Precio por defecto si el lote no cae dentro del radio de ninguna zona conocida.
PRECIO_BASE_DEFAULT_M2 = 400.0
