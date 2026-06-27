"""
Lógica de tasación de lotes.

La fórmula es transparente y editable:

    precio_total = precio_base_m2(zona) * superficie * factores_ajuste

Factores de ajuste (multiplicativos, parten de 1.0):
    - frente_factor: lotes con más metros de frente valen más (frente angosto penaliza)
    - esquina_factor: un lote en esquina suma valor
    - forma_factor: lotes irregulares (poco frente respecto al fondo) penalizan
    - antiguedad_dato_factor: si el precio de la zona es viejo, se aplica corrección

Todos los coeficientes están centralizados en `COEFICIENTES` para que sea fácil
ajustarlos sin tocar la lógica.
"""

import math
from datetime import date
from typing import Optional

from zonas import ZONAS, PRECIO_BASE_DEFAULT_M2

# ---------------------------------------------------------------------------
# Coeficientes de la fórmula (ajustables)
# ---------------------------------------------------------------------------
COEFICIENTES = {
    "esquina_bonus": 0.08,           # +8% si el lote es esquina
    "frente_ideal_m": 10.0,          # frente de referencia "normal"
    "frente_penalizacion_max": 0.15, # hasta -15% si el frente es muy angosto
    "frente_bonus_max": 0.10,        # hasta +10% si el frente es muy amplio
    "fondo_frente_ratio_ideal": 2.5, # relación fondo/frente considerada "normal"
    "forma_penalizacion_max": 0.10,  # hasta -10% por lote desproporcionado
    "depreciacion_anual_dato": 0.02, # 2% anual de ajuste si el dato de zona es viejo
}


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distancia entre dos puntos geográficos en km."""
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def encontrar_zona(lat: float, lon: float) -> dict:
    """
    Busca la zona más cercana cuyo radio cubra el punto dado.
    Si ninguna zona cubre el punto, devuelve una zona 'default' con precio base genérico.
    """
    candidatas = []
    for z in ZONAS:
        dist = _haversine_km(lat, lon, z["lat"], z["lon"])
        if dist <= z["radio_km"]:
            candidatas.append((dist, z))

    if candidatas:
        candidatas.sort(key=lambda x: x[0])
        return candidatas[0][1]

    # Si no cae en ninguna zona, devolvemos la más cercana igual, pero marcada como fuera de cobertura
    distancias = [(_haversine_km(lat, lon, z["lat"], z["lon"]), z) for z in ZONAS]
    distancias.sort(key=lambda x: x[0])
    zona_mas_cercana = distancias[0][1] if distancias else None

    return {
        "id": "fuera_de_cobertura",
        "nombre": f"Fuera de cobertura (más cercana: {zona_mas_cercana['nombre'] if zona_mas_cercana else 'N/A'})",
        "precio_base_m2": PRECIO_BASE_DEFAULT_M2,
    }


def _factor_frente(frente_m: float) -> float:
    """Ajusta el precio según qué tan angosto o amplio es el frente respecto al ideal."""
    ideal = COEFICIENTES["frente_ideal_m"]
    if frente_m <= 0:
        return 1.0
    diferencia_relativa = (frente_m - ideal) / ideal

    if diferencia_relativa < 0:
        # Frente angosto: penaliza, tope en frente_penalizacion_max
        penalizacion = min(abs(diferencia_relativa), 1.0) * COEFICIENTES["frente_penalizacion_max"]
        return 1.0 - penalizacion
    else:
        # Frente amplio: bonifica, tope en frente_bonus_max
        bonus = min(diferencia_relativa, 1.0) * COEFICIENTES["frente_bonus_max"]
        return 1.0 + bonus


def _factor_forma(frente_m: float, fondo_m: Optional[float]) -> float:
    """Penaliza lotes muy desproporcionados (relación fondo/frente lejos del ideal)."""
    if not fondo_m or frente_m <= 0:
        return 1.0
    ratio = fondo_m / frente_m
    ideal = COEFICIENTES["fondo_frente_ratio_ideal"]
    desvio_relativo = abs(ratio - ideal) / ideal
    penalizacion = min(desvio_relativo, 1.0) * COEFICIENTES["forma_penalizacion_max"]
    return 1.0 - penalizacion


def _factor_antiguedad_dato(fecha_dato: Optional[date]) -> float:
    """Si el precio de referencia de la zona es viejo, se aplica una depreciación simple."""
    if not fecha_dato:
        return 1.0
    años = (date.today() - fecha_dato).days / 365.25
    if años <= 0:
        return 1.0
    return max(0.5, 1.0 - años * COEFICIENTES["depreciacion_anual_dato"])


def tasar_lote(
    lat: float,
    lon: float,
    superficie_m2: float,
    frente_m: float,
    fondo_m: Optional[float] = None,
    es_esquina: bool = False,
    fecha_dato_zona: Optional[date] = None,
) -> dict:
    """
    Calcula la tasación estimada de un lote.

    Devuelve un detalle completo: zona detectada, precio base, cada factor
    aplicado y el resultado final, para que la tasación sea auditable.
    """
    zona = encontrar_zona(lat, lon)
    precio_base_m2 = zona["precio_base_m2"]

    factor_frente = _factor_frente(frente_m)
    factor_forma = _factor_forma(frente_m, fondo_m)
    factor_esquina = 1.0 + COEFICIENTES["esquina_bonus"] if es_esquina else 1.0
    factor_antiguedad = _factor_antiguedad_dato(fecha_dato_zona)

    factor_total = factor_frente * factor_forma * factor_esquina * factor_antiguedad
    precio_m2_ajustado = precio_base_m2 * factor_total
    precio_total = precio_m2_ajustado * superficie_m2

    return {
        "zona": {"id": zona["id"], "nombre": zona["nombre"]},
        "precio_base_m2": round(precio_base_m2, 2),
        "factores": {
            "frente": round(factor_frente, 4),
            "forma": round(factor_forma, 4),
            "esquina": round(factor_esquina, 4),
            "antiguedad_dato": round(factor_antiguedad, 4),
            "total": round(factor_total, 4),
        },
        "precio_m2_ajustado": round(precio_m2_ajustado, 2),
        "superficie_m2": superficie_m2,
        "tasacion_estimada": round(precio_total, 2),
        "moneda": "USD",
    }
  
