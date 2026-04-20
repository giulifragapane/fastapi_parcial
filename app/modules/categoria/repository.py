# app/modules/categoria/repository.py
from sqlmodel import select, Session
from sqlalchemy import func
from app.core.repository import BaseRepository
from app.modules.categoria.model import Categoria

#Acá van todas las consultas específicas de la categoría, como obtener por parent_id, etc.

class CategoriaRepository(BaseRepository[Categoria]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, Categoria)

    # Dame todas las subcategorías de una categoría padre
    def get_by_parent_id(self, parent_id: int) -> list[Categoria]:
        return self.session.exec(
            select(Categoria).where(Categoria.parent_id == parent_id)
        ).all()
    
    #buscar categoría por nombre
    def get_by_nombre(self, nombre: str) -> Categoria | None:
        return self.session.exec(
            select(Categoria).where(Categoria.nombre == nombre)
    ).first()

    def get_active(self, offset: int = 0, limit: int = 20) -> list[Categoria]:
        """
        Obtiene categorías activas con paginación.

        Args:
            offset (int): Cantidad de registros a omitir.
            limit (int): Máximo de registros a devolver.

        Returns:
            list[Categoria]: Lista de categorías activas.

        Nota:
            - No se define orden explícito → resultados no determinísticos
            - Se usa '== True' por limitaciones del ORM (evita warnings de estilo)
        """
        return list(
            self.session.exec(
                select(Categoria)
                .where(Categoria.deleted_at.is_(None))  # noqa: E712
                .offset(offset)
                .limit(limit)
            ).all()
        )

    def count(self) -> int:
        """
        Cuenta la cantidad total de categorias.

        Returns:
            int: Total de registros en la tabla Categoria.
        return len(self.session.exec(select(Categoria)).all())
        """
        return self.session.exec(
            select(func.count())
            .select_from(Categoria)
            .where(Categoria.deleted_at.is_(None))
        ).one()
  