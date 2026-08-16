from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from pydantic import BaseModel

from app.db.database import Base

ModelType = TypeVar(
    "ModelType",
    bound=Base,
)
CreateSchemaType = TypeVar(
    "CreateSchemaType",
    bound=BaseModel,
)
UpdateSchemaType = TypeVar(
    "UpdateSchemaType",
    bound=BaseModel,
)


class BaseRepository(Generic[
        ModelType,
        CreateSchemaType,
        UpdateSchemaType,
    ]):

    def __init__(
        self,
        session: Session,
        model: type[ModelType],
        pk_field: str,
    ):
        self.session = session
        self.model = model
        self.pk_field = pk_field
        self.pk = getattr(model, pk_field)

    def get(
            self,
            obj_id: int,
    ) -> ModelType | None:
        """
        Get a database object.
        """

        stmt = select(self.model).where(
            self.pk == obj_id
        )

        return self.session.scalar(stmt)

    def create(
            self,
            create_data: CreateSchemaType,
            *,
            commit: bool = True,
    ) -> ModelType:
        """
        Create a new database object.
        """
        db_obj = self.model(
            **create_data.model_dump()
        )
        self.session.add(db_obj)

        if commit:
            self.session.commit()
            self.session.refresh(db_obj)
        else:
            self.session.flush()

        return db_obj

    def update(
            self,
            db_obj: ModelType,
            update_data: UpdateSchemaType,
    ) -> ModelType:
        """
        Update a database object.
        """

        update_values = update_data.model_dump(
            exclude_unset=True,
        )
        for field, value in update_values.items():
            setattr(
                db_obj,
                field,
                value,
            )
        self.session.commit()
        self.session.refresh(db_obj)

        return db_obj

    def delete(
            self,
            db_obj: ModelType,
    ) -> None:
        """
        Delete a database object.
        """
        self.session.delete(db_obj)
        self.session.commit()
