# Lógica de negocio y operaciones CRUD para Producto con la base de datos
from fastapi import HTTPException, status
from sqlmodel import Session
from app.modules.producto.schema import ProductoCreate, ProductoUpdate, ProductoRead, ProductoList
from app.modules.producto.model import Producto
from app.modules.producto.unit_of_work import ProductoUnitOfWork

class ProductoService:

    def __init__(self, session: Session) -> None:
        self._session = session
    # ── Helpers privados ──────────────────────────────────────────────────────

    def _get_or_404(self, uow: IngredienteUnitOfWork, producto_id: int) -> Producto:
        """
        Obtiene un ingrediente por ID o lanza excepción HTTP 404 si no existe.

        Args:
            uow (IngredienteUnitOfWork): Unidad de trabajo activa.
            ingrediente_id (int): ID de la categoría.

        Returns:
            Ingrediente: Instancia encontrada.

        Raises:
            HTTPException: 404 si la categoría no existe.

        """
        producto = uow.producto.get_by_id(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id={producto_id} no encontrado",
            )
        return producto


    def _assert_nombre_unique(self, uow: ProductoUnitOfWork, nombre: str) -> None:
        """
        Valida que el nombre no esté en uso.

        Args:
            uow (IngredienteUnitOfWork): Unidad de trabajo activa.
            alias (str): Alias a validar.

        Raises:
            HTTPException: 409 si el nombre ya existe.

        Nota:
            Esta validación es a nivel aplicación, no reemplaza un UNIQUE en DB.
        """
        if uow.productos.get_by_nombre(nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El nombre '{nombre}' ya está en uso",
            )
    def create(self, data: ProductoCreate) -> ProductoRead:
        """
        Crea una nueva categoría.

        Flujo:
        - Valida unicidad de nombre
        - Construye entidad desde DTO
        - Persiste usando repositorio
        - Serializa antes de cerrar la transacción

        Args:
            data (IngredienteCreate): Datos de entrada.

        Returns:
            HeroPublic: DTO de salida.
        """
        with ProductoUnitOfWork(self._session) as uow:
            self._assert_nombre_unique(uow, data.nombre)

            producto = Producto(nombre=data.nombre, descripcion=data.descripcion, precio_base=data.precio_base, imagenes_url=data.imagenes_url, stock_cantidad=data.stock_cantidad, disponible=data.disponible)
            if data.categoria_ids:
                categorias = []
                for categoria_id in data.categoria_ids:
                    categoria = uow.categorias.get_by_id(categoria_id)
                    if not categoria:
                        raise HTTPException(
                                    status_code=status.HTTP_404_not_found,
                                    detail=f"La categoria con id='{categoria_id}' no encontrada.",
                            )
                    categorias.append(categoria)
                producto.categorias = categorias

            if data.ingrediente_ids:
                ingredientes = []
                for ingrediente_id in data.ingrediente_ids:
                    ingrediente = uow.ingredientes.get_by_id(ingrediente_id)
                    if not ingrediente:
                        raise HTTPException(
                                    status_code=status.HTTP_404_not_found,
                                    detail=f"El ingrediente con id='{ingrediente_id}' no encontrada.",
                            )
                    ingredientes.append(ingrediente)
                producto.ingredientes = ingredientes     

            uow.productos.add(producto)

            # Serializar dentro del contexto asegura acceso a atributos lazy
            result = ProductoRead.model_validate(producto)

        return result
    
    def get_by_id(self, producto_id: int) -> ProductoRead:
        """
        Obtiene una ingrediente por ID.

        Args:
            ingrediente_id (int): ID de la categoría.

        Returns:
            IngredienteRead: DTO de la categoría.

        Raises:
            HTTPException: 404 si no existe.
        """
        with ProductoUnitOfWork(self._session) as uow:
            producto = self._get_or_404(uow, producto_id)
            result = ProductoRead.model_validate(ingrediente)

        return result
    def update(self, ingrediente_id: int, data: IngredienteUpdate) -> IngredienteRead:
        """
        Actualiza un ingrediente existente de forma parcial (PATCH).

        Flujo:
        - Obtiene entidad
        - Valida nombre si cambia
        - Aplica cambios dinámicamente
        - Persiste cambios

        Args:
            ingrediente_id (int): ID de la categoría.
            data (IngredienteUpdate): Datos parciales.

        Returns:
            IngredienteRead: DTO actualizado.
        """
        with IngredienteUnitOfWork(self._session) as uow:
            ingrediente = self._get_or_404(uow, ingrediente_id)

            if data.nombre and data.nombre != ingrediente.nombre:
                self._assert_nombre_unique(uow, data.nombre)

            # Solo campos enviados por el cliente
            patch = data.model_dump(exclude_unset=True)

            for field, value in patch.items():
                setattr(ingrediente, field, value)

            ingrediente.updated_at = uow.now
            uow.ingredientes.add(ingrediente)
            result = IngredienteRead.model_validate(ingrediente)

        return result
    
    def soft_delete(self, ingrediente_id: int) -> None:
        """
        Realiza un borrado lógico de la categoría.

        Flujo:
        - Obtiene entidad
        - Marca como inactivo
        - Persiste cambio

        Args:
            ingrediente_id (int): ID de la categoría.

        Nota:
            No elimina físicamente el registro de la base de datos.
        """
        with IngredienteUnitOfWork(self._session) as uow:
            ingrediente = self._get_or_404(uow, ingrediente_id)
            if ingrediente.productos:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede eliminar un ingrediente asociado a uno o más productos."
                )
            ingrediente.deleted_at = uow.now
            ingrediente.updated_at = uow.now
            uow.ingredientes.add(ingrediente)
            
    # TO DO (REVISAR)
    def get_all(self, offset: int = 0, limit: int = 20) -> ProductoList:
        """
        Obtiene lista paginada de todos los ingredientes.

        Args:
            offset (int): Desplazamiento.
            limit (int): Límite de resultados.

        Returns:
            CategoriaList: DTO con lista de categorías y total.

        Nota:
            El total se calcula con una query separada.
        """
        with ProductoUnitOfWork(self._session) as uow:
            productos = uow.productos.get_all(offset=offset, limit=limit)
            total = len(productos)

            result = ProductoList(
                data=[ProductoRead.model_validate(c) for c in productos],
                total=total,
            )

        return result