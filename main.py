"""
API de tasación de lotes.

Ejecutar:
    pip install fastapi uvicorn --break-system-packages
    uvicorn main:app --reload

Probar en: http://127.0.0.1:8000/docs
"""

from datetime import date
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from tasacion import tasar_lote
from zonas import ZONAS
from comparables import comparables_de_zona

app = FastAPI(
    title="API de Tasación de Lotes",
    description="Calcula una tasación estimada de un lote según su ubicación y características.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sirve la página web (HTML/CSS/JS) ubicada en /static
app.mount("/static", StaticFiles(directory="static"), name="static")


class ServiciosLote(BaseModel):
    """Servicios públicos disponibles en el lote puntual.
    Si un campo no se informa (None), se completa con el dato típico de la zona."""
    luz: Optional[bool] = Field(None, description="Tiene suministro eléctrico")
    agua_red: Optional[bool] = Field(None, description="Tiene agua de red (no de pozo)")
    cloacas: Optional[bool] = Field(None, description="Tiene conexión a cloacas")
    gas_red: Optional[bool] = Field(None, description="Tiene gas natural de red")
    transporte_publico: Optional[bool] = Field(None, description="Tiene transporte público cercano")


class TasacionRequest(BaseModel):
    lat: float = Field(..., description="Latitud del lote")
    lon: float = Field(..., description="Longitud del lote")
    superficie_m2: float = Field(..., gt=0, description="Superficie total del lote en m²")
    frente_m: float = Field(..., gt=0, description="Metros de frente del lote")
    fondo_m: Optional[float] = Field(None, gt=0, description="Metros de fondo del lote (opcional)")
    es_esquina: bool = Field(False, description="Si el lote está en esquina")
    fecha_dato_zona: Optional[date] = Field(
        None, description="Fecha de referencia del precio de zona usado (opcional)"
    )

    # --- Nuevos campos ---
    es_inundable: Optional[bool] = Field(
        None,
        description="Si el lote puntual es inundable. Si no se informa, se usa el dato típico de la zona.",
    )
    tiene_construccion: bool = Field(False, description="Si el lote tiene construcción existente")
    estado_construccion: Optional[str] = Field(
        None,
        description="Estado de la construcción: 'excelente', 'bueno', 'regular' o 'malo' (requerido si tiene_construccion=true)",
    )
    antiguedad_construccion_anios: Optional[float] = Field(
        None, ge=0, description="Antigüedad de la construcción en años"
    )
    superficie_construida_m2: Optional[float] = Field(
        None, gt=0, description="Superficie construida en m² (opcional)"
    )
    servicios: Optional[ServiciosLote] = Field(
        None, description="Servicios públicos disponibles en el lote puntual"
    )


class TasacionResponse(BaseModel):
    zona: dict
    servicios: dict
    precio_base_m2: float
    factores: dict
    precio_m2_ajustado: float
    superficie_m2: float
    valor_terreno: float
    construccion: dict
    tasacion_estimada: float
    comparacion_mercado: dict
    moneda: str


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/api")
def api_info():
    return {"mensaje": "API de tasación de lotes activa. Ver /docs para probar los endpoints."}


@app.get("/zonas")
def listar_zonas():
    """Devuelve las zonas configuradas y su precio base por m²."""
    return ZONAS


@app.get("/comparables/{zona_id}")
def comparables_zona(zona_id: str):
    """Devuelve los comparables de mercado cargados para una zona."""
    return comparables_de_zona(zona_id)


@app.post("/tasar", response_model=TasacionResponse)
def tasar(req: TasacionRequest):
    """
    Calcula la tasación estimada de un lote.

    Ejemplo de body:
    {
      "lat": -34.605,
      "lon": -58.38,
      "superficie_m2": 300,
      "frente_m": 12,
      "fondo_m": 25,
      "es_esquina": true,
      "es_inundable": false,
      "tiene_construccion": true,
      "estado_construccion": "bueno",
      "antiguedad_construccion_anios": 15,
      "superficie_construida_m2": 120,
      "servicios": {
        "luz": true,
        "agua_red": true,
        "cloacas": false,
        "gas_red": false,
        "transporte_publico": true
      }
    }
    """
    servicios_dict = req.servicios.model_dump() if req.servicios else None

    resultado = tasar_lote(
        lat=req.lat,
        lon=req.lon,
        superficie_m2=req.superficie_m2,
        frente_m=req.frente_m,
        fondo_m=req.fondo_m,
        es_esquina=req.es_esquina,
        fecha_dato_zona=req.fecha_dato_zona,
        es_inundable=req.es_inundable,
        tiene_construccion=req.tiene_construccion,
        estado_construccion=req.estado_construccion,
        antiguedad_construccion_anios=req.antiguedad_construccion_anios,
        superficie_construida_m2=req.superficie_construida_m2,
        servicios=servicios_dict,
    )
    return resultado
    
