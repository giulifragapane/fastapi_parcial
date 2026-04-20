# app/modules/ingrediente/repository.py
from sqlmodel import select, Session
from sqlalchemy import func
from app.core.repository import BaseRepository
from app.modules.ingrediente.model import Ingrediente


class IngredienteRepository(BaseRepository[Ingrediente]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, Ingrediente)

    def get_by_nombre(self, nombre: str) -> Ingrediente | None:
        return self.session.exec(
            select(Ingrediente).where(Ingrediente.nombre == nombre)
    ).first()

    def get_alergenos(self, offset: int = 0, limit: int = 20) -> list[Ingrediente]:
        
        return list(
            self.session.exec(
                select(Ingrediente)
                .where(Ingrediente.es_alergeno)
                .offset(offset)
                .limit(limit)
        ).all())
    
    def get_active(self, offset: int = 0, limit: int = 20) -> list[Ingrediente]:
        """
        Obtiene ingredientes activas con paginación.

        Args:
            offset (int): Cantidad de registros a omitir.
            limit (int): Máximo de registros a devolver.

        Returns:
            list[Ingrediente]: Lista de ingredientes activos.

        Nota:
            - No se define orden explícito → resultados no determinísticos
            - Se usa '== True' por limitaciones del ORM (evita warnings de estilo)
        """
        return list(
            self.session.exec(
                select(Ingrediente)
                .where(Ingrediente.deleted_at.is_(None))  # noqa: E712
                .offset(offset)
                .limit(limit)
            ).all()
        )
    
    def count(self) -> int:
        """
        Cuenta la cantidad total de ingredientes.
        Returns:
            int: Total de registros en la tabla Ingredientes.
        return len(self.session.exec(select(Ingrediente)).all())
        """
        return self.session.exec(
            select(func.count())
            .select_from(Ingrediente)
            .where(Ingrediente.deleted_at.is_(None))
        ).one()