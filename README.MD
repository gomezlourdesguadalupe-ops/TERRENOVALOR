# Tasación de Lotes — App web

Aplicación completa: backend en Python (FastAPI) + página web con formulario,
que calcula una tasación estimada de un lote a partir de su ubicación (lat/lon)
y sus características físicas (superficie, frente, fondo, esquina).

## Estructura

```
tasacion_api/
├── main.py        # API + sirve la página web
├── tasacion.py     # Fórmula de cálculo
├── zonas.py        # Tus zonas y precios base (ACÁ va tu data real)
├── static/
│   └── index.html  # La página web (formulario + resultado)
└── README.md
```

## Cómo correrla

```bash
pip install fastapi uvicorn --break-system-packages
cd tasacion_api
uvicorn main:app --reload
```

Abrí el navegador en **`http://127.0.0.1:8000`** — ahí está la app completa:
formulario a la izquierda, resultado de la tasación a la derecha.

(El Swagger/docs de la API sigue disponible en `http://127.0.0.1:8000/docs`
si querés probar los endpoints sueltos.)

## Cómo funciona la app

1. El usuario completa el formulario: ubicación (lat/lon, manual o con el botón
   "Usar mi ubicación" que pide permiso al navegador), superficie, frente, fondo
   y si es esquina.
2. Al apretar "Calcular tasación", el HTML le hace un `POST /tasar` a la misma
   API (todo corre en el mismo servidor, no hay que configurar URLs).
3. La API calcula con la fórmula de `tasacion.py` y devuelve el resultado, que
   se muestra como un "sello de tasación" con el desglose de cada coeficiente
   aplicado (frente, forma del lote, esquina, antigüedad del dato).

## Personalización

- **Cargar tus zonas reales**: editá la lista `ZONAS` en `zonas.py` con
  coordenadas, radio de cobertura y precio de mercado real por m².
- **Ajustar la fórmula**: modificá `COEFICIENTES` en `tasacion.py`.
- **Cambiar textos o estilo de la página**: todo está en `static/index.html`
  (HTML, CSS y JS en un solo archivo, sin dependencias de build).

## Llevarla a producción (subirla a internet)

Mientras corra solo en tu computadora (`127.0.0.1`), nadie más puede acceder.
Para que otra persona la use desde su navegador, necesitás desplegar el backend
en un servidor. Opciones simples y gratuitas/económicas para empezar:

- **Render** o **Railway**: conectás tu repositorio de GitHub, detectan que es
  una app FastAPI y la levantan con una URL pública (ej. `tu-app.onrender.com`).
- **Fly.io**: similar, con más control sobre recursos.
- **Un VPS propio** (DigitalOcean, AWS EC2, etc.): más trabajo de configuración,
  pero más control. Se corre `uvicorn` detrás de Nginx, con HTTPS vía Let's Encrypt.

Para cualquiera de estas, necesitás:
1. Subir el código a un repositorio Git (GitHub/GitLab).
2. Agregar un archivo `requirements.txt` con `fastapi` y `uvicorn`.
3. Indicarle a la plataforma el comando de inicio: `uvicorn main:app --host 0.0.0.0 --port $PORT`.

## Importante

Este es un modelo de **estimación basado en fórmulas configurables**, no una
tasación profesional ni un avalúo legal. Para uso real en transacciones, se
recomienda validar con un tasador matriculado y datos de mercado actualizados.

