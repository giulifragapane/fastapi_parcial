# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.core.database import create_db_and_tables
from app.modules.categoria.model import Categoria
from app.modules.producto.model import Producto
from app.modules.ingrediente.model import Ingrediente
from app.modules.categoria.router import router as categoria_router
"""
---ES EL PUNTO DE ENTRADA DE LA APLICACIÓN---
- Aquí se crea la instancia de FastAPI, se configura el lifespan (ciclo de vida) de la aplicación, 
y se incluyen los routers.
"""

@asynccontextmanager # Su funcion es definir el ciclo de vida de la aplicación, 
# en este caso, para crear las tablas al iniciar la app
async def lifespan(app: FastAPI):
    create_db_and_tables() # Llamamos a la función que crea las tablas en la base de datos al iniciar la app
    yield # Aquí se ejecuta el código de la app (routers, etc)
    
app = FastAPI(
    title="API Parcial", 
    description="API para el parcial de programación backend", 
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(categoria_router)
