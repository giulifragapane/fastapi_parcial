# app/modules/ingrediente/model.py
from typing import List, TYPE_CHECKING
from sqlmodel import Field, Relationship

from app.core.base import Base
from app.modules.producto.model import ProductoIngrediente

if TYPE_CHECKING:
    from app.modules.producto.model import Producto

class Ingrediente(Base, table=True):
    __tablename__ = "ingredientes"

    nombre: str = Field(max_length=100, unique=True, nullable=False)
    descripcion: str = Field(nullable=False)
    es_alergeno: bool = Field(default=False, nullable=False)

    # ── Relaciones inversa ───────────────────────
    productos: List["Producto"] = Relationship(
        back_populates="ingredientes",
        link_model=ProductoIngrediente
    )

