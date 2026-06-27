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

app = FastAPI(
    title="API de Tasación de Lotes",
    description="Calcula una tasación estimada de un lote según su ubicación y características.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sirve la página web (HTML/CSS/JS) ubicada en /static
app.mount("/static", StaticFiles(directory="static"), name="static")


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


class TasacionResponse(BaseModel):
    zona: dict
    precio_base_m2: float
    factores: dict
    precio_m2_ajustado: float
    superficie_m2: float
    tasacion_estimada: float
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
      "es_esquina": true
    }
    """
    resultado = tasar_lote(
        lat=req.lat,
        lon=req.lon,
        superficie_m2=req.superficie_m2,
        frente_m=req.frente_m,
        fondo_m=req.fondo_m,
        es_esquina=req.es_esquina,
        fecha_dato_zona=req.fecha_dato_zona,
    )
    return resultado
    
