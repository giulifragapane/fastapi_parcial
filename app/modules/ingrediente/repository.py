# app/modules/ingrediente/repository.py
from sqlmodel import select, Session
from app.core.repository import BaseRepository
from app.modules.ingrediente.model import Ingrediente


class IngredienteRepository(BaseRepository[Ingrediente]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, Ingrediente)

    def get_by_nombre(self, nombre: str) -> Ingrediente | None:
        return self.session.exec(
            select(Ingrediente).where(Ingrediente.nombre == nombre)
    ).first()

    def get_alergenos(self) -> list[Ingrediente]:
        return list(self.session.exec(
            select(Ingrediente).where(Ingrediente.es_alergeno == True)
        ).all())
