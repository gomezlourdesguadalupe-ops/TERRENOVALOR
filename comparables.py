"""
Comparables de mercado por zona.

Cargá aquí terrenos de referencia que encuentres publicados en sitios como
Zonaprop o Argenprop. Estos datos son SOLO los que vos copiás manualmente:
el sistema NO se conecta a esos sitios automáticamente (no se puede hacer
de forma confiable ni permitida).

Cómo cargar un comparable:
  - zona_id: debe coincidir con el "id" de una zona en zonas.py
  - fuente: de dónde sacaste el dato (ej: "Zonaprop", "Argenprop", "Tasación propia")
  - direccion_aprox: referencia de ubicación, sin datos sensibles
  - superficie_m2: superficie del lote comparado
  - precio_publicado: precio total publicado (en la moneda que se haya publicado)
  - moneda: "USD" o "ARS"
  - fecha: fecha en que se relevó el dato, formato "AAAA-MM-DD"
  - link: opcional, URL del aviso (para verificar después)

Para refrescar los precios de una zona, simplemente edita o agrega entradas
en la lista COMPARABLES. No hace falta tocar ningún otro archivo.
"""

COMPARABLES = [
    {
        "zona_id": "zona_centro",
        "fuente": "Zonaprop",
        "direccion_aprox": "Av. Corrientes y Callao (aprox.)",
        "superficie_m2": 280.0,
        "precio_publicado": 336000.0,
        "moneda": "USD",
        "fecha": "2026-05-10",
        "link": None,
    },
    {
        "zona_id": "zona_centro",
        "fuente": "Argenprop",
        "direccion_aprox": "Av. Pueyrredón al 1500 (aprox.)",
        "superficie_m2": 320.0,
        "precio_publicado": 384000.0,
        "moneda": "USD",
        "fecha": "2026-04-22",
        "link": None,
    },
    {
        "zona_id": "zona_norte",
        "fuente": "Zonaprop",
        "direccion_aprox": "San Isidro, zona residencial (aprox.)",
        "superficie_m2": 400.0,
        "precio_publicado": 380000.0,
        "moneda": "USD",
        "fecha": "2026-05-02",
        "link": None,
    },
    {
        "zona_id": "zona_norte",
        "fuente": "Argenprop",
        "direccion_aprox": "Vicente López, cerca de la costa (aprox.)",
        "superficie_m2": 350.0,
        "precio_publicado": 332500.0,
        "moneda": "USD",
        "fecha": "2026-03-15",
        "link": None,
    },
    {
        "zona_id": "zona_sur",
        "fuente": "Zonaprop",
        "direccion_aprox": "Avellaneda, zona residencial (aprox.)",
        "superficie_m2": 300.0,
        "precio_publicado": 180000.0,
        "moneda": "USD",
        "fecha": "2026-04-01",
        "link": None,
    },
    {
        "zona_id": "zona_sur",
        "fuente": "Argenprop",
        "direccion_aprox": "Lanús, cerca de ruta (aprox.)",
        "superficie_m2": 250.0,
        "precio_publicado": 137500.0,
        "moneda": "USD",
        "fecha": "2026-02-18",
        "link": None,
    },
    {
        "zona_id": "zona_oeste",
        "fuente": "Zonaprop",
        "direccion_aprox": "Morón, zona residencial (aprox.)",
        "superficie_m2": 300.0,
        "precio_publicado": 150000.0,
        "moneda": "USD",
        "fecha": "2026-05-05",
        "link": None,
    },
    {
        "zona_id": "zona_oeste",
        "fuente": "Argenprop",
        "direccion_aprox": "Ramos Mejía, zona residencial (aprox.)",
        "superficie_m2": 280.0,
        "precio_publicado": 137200.0,
        "moneda": "USD",
        "fecha": "2026-03-28",
        "link": None,
    },
]


def comparables_de_zona(zona_id: str) -> list:
    """Devuelve todos los comparables cargados para una zona dada."""
    return [c for c in COMPARABLES if c["zona_id"] == zona_id]
