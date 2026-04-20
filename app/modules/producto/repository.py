# app/modules/producto/repository.py
from sqlmodel import select, Session
from app.core.repository import BaseRepository
from app.modules.producto.model import Producto

#Acá van todas las consultas específicas del producto.

class ProductoRepository(BaseRepository[Producto]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, Producto)

    #buscar productos por nombre
    def get_by_nombre(self, nombre: str) -> Producto | None:
        return self.session.exec(
            select(Producto).where(Producto.nombre == nombre)
    ).first()

    def get_active(self, offset: int = 0, limit: int = 20) -> list[Producto]:
        """
        Obtiene productos activas con paginación.

        Args:
            offset (int): Cantidad de registros a omitir.
            limit (int): Máximo de registros a devolver.

        Returns:
            list[Producto]: Lista de categorías activas.

        Nota:
            - No se define orden explícito → resultados no determinísticos
            - Se usa '== True' por limitaciones del ORM (evita warnings de estilo)
        """
        return list(
            self.session.exec(
                select(Producto)
                .where(Producto.deleted_at.is_(None))  # noqa: E712
                .offset(offset)
                .limit(limit)
            ).all()
        )

    def count(self) -> int:
        """
        Cuenta la cantidad total de productoS.

        Returns:
            int: Total de registros en la tabla Producto.
        """
        return len(self.session.exec(select(Producto)).all())
  