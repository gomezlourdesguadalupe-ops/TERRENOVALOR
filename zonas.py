"""
Datos de referencia de zonas para la tasación.
Reemplazá estos valores por tus propios datos reales (precio por m² de mercado).

Cada zona ahora incluye, además del precio base:
  - inundable: True/False -> si la zona es propensa a inundaciones
  - nivel_adquisitivo: "alto" | "medio" | "bajo" -> poder adquisitivo típico de la zona
  - servicios_tipicos: qué servicios suele tener la zona "de fábrica" (se puede
    sobreescribir por lote en cada tasación si el lote puntual difiere de la zona).
"""

# Cada zona tiene: nombre, coordenadas centrales (lat, lon), precio base por m² en USD,
# radio aproximado de cobertura en km, si es inundable, nivel adquisitivo y servicios típicos.
ZONAS = [
    {
        "id": "zona_centro",
        "nombre": "Centro",
        "lat": -34.6037,
        "lon": -58.3816,
        "precio_base_m2": 1200.0,
        "radio_km": 3,
        "inundable": False,
        "nivel_adquisitivo": "alto",
        "servicios_tipicos": {
            "luz": True,
            "agua_red": True,
            "cloacas": True,
            "gas_red": True,
            "transporte_publico": True,
        },
    },
    {
        "id": "zona_norte",
        "nombre": "Zona Norte",
        "lat": -34.5100,
        "lon": -58.4900,
        "precio_base_m2": 950.0,
        "radio_km": 5,
        "inundable": False,
        "nivel_adquisitivo": "alto",
        "servicios_tipicos": {
            "luz": True,
            "agua_red": True,
            "cloacas": True,
            "gas_red": True,
            "transporte_publico": True,
        },
    },
    {
        "id": "zona_sur",
        "nombre": "Zona Sur",
        "lat": -34.7200,
        "lon": -58.3500,
        "precio_base_m2": 600.0,
        "radio_km": 5,
        "inundable": True,
        "nivel_adquisitivo": "medio",
        "servicios_tipicos": {
            "luz": True,
            "agua_red": True,
            "cloacas": False,
            "gas_red": False,
            "transporte_publico": True,
        },
    },
    {
        "id": "zona_oeste",
        "nombre": "Zona Oeste",
        "lat": -34.6500,
        "lon": -58.6500,
        "precio_base_m2": 500.0,
        "radio_km": 6,
        "inundable": False,
        "nivel_adquisitivo": "medio",
        "servicios_tipicos": {
            "luz": True,
            "agua_red": True,
            "cloacas": False,
            "gas_red": False,
            "transporte_publico": False,
        },
    },
]

# Precio por defecto si el lote no cae dentro del radio de ninguna zona conocida.
PRECIO_BASE_DEFAULT_M2 = 400.0

# Servicios por defecto si no se especifican para el lote ni hay dato de zona.
SERVICIOS_DEFAULT = {
    "luz": False,
    "agua_red": False,
    "cloacas": False,
    "gas_red": False,
    "transporte_publico": False,
}

# Nivel adquisitivo por defecto si la zona no especifica uno.
NIVEL_ADQUISITIVO_DEFAULT = "medio"
