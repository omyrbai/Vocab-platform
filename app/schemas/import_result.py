from pydantic import BaseModel, Field

from app.enums.import_action import ImportAction
from app.schemas.upsert_result import UpsertResult


class ImportResult(BaseModel):
    """
    Result of an import operation.
    """

    created: list[UpsertResult] = Field(
        default_factory=list
    )

    updated: list[UpsertResult] = Field(
        default_factory=list
    )

    skipped: list[UpsertResult] = Field(
        default_factory=list
    )

    def add(
            self,
            result: UpsertResult,
    ) -> None:
        """
        Add an upsert result to the appropriate collection.
        """

        if result.action is ImportAction.CREATED:
            self.created.append(result)

        elif result.action is ImportAction.UPDATED:
            self.updated.append(result)

        else:
            self.skipped.append(result)

    @property
    def created_count(
            self,
    ) -> int:
        return len(self.created)

    @property
    def updated_count(
            self,
    ) -> int:
        return len(self.updated)

    @property
    def skipped_count(
            self,
    ) -> int:
        return len(self.skipped)

    @property
    def total_count(
            self,
    ) -> int:
        return (
            self.created_count
            + self.updated_count
            + self.skipped_count
        )

