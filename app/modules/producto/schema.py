# app/modules/producto/schema.py
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.categoria.schema import CategoriaRead
from app.modules.ingrediente.schema import IngredienteRead

# ── Base schema para el producto, con campos comunes a creación y actualización
class ProductoBase(BaseModel):
    nombre: str = Field(..., max_length=150)
    descripcion: str
    precio_base: Decimal = Field(..., ge=0)
    imagenes_url: List[str] = Field(default_factory=list)
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = True

    @field_validator("precio_base")
    @classmethod
    def redondear_precio(cls, v: Decimal) -> Decimal:
        return round(v, 2)

# ── Entrada ───────────────────────────────────────────────────────────────────
class ProductoCreate(ProductoBase):
    categoria_ids: List[int] = Field(default_factory=list)
    ingrediente_ids: List[int] = Field(default_factory=list)


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    precio_base: Optional[Decimal] = Field(None, ge=0)
    imagenes_url: Optional[List[str]] = None
    stock_cantidad: Optional[int] = Field(None, ge=0)
    disponible: Optional[bool] = None
    categoria_ids: Optional[List[int]] = None
    ingrediente_ids: Optional[List[int]] = None

# ── Salida ───────────────────────────────────────────────────────────────────
class ProductoRead(ProductoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    categorias: List[CategoriaRead] = Field(default_factory=list)
    ingredientes: List[IngredienteRead] = Field(default_factory=list)


class IngredienteEnProducto(BaseModel):
    """Ingrediente con su cantidad/unidad dentro de un producto."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str

class ProductoList(BaseModel):
    data: List[ProductoRead]
    total: int