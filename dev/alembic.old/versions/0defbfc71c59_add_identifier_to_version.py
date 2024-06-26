"""add identifier to version

Revision ID: 0defbfc71c59
Revises: 29e42ce4be3f
Create Date: 2024-01-05 13:25:15.547450

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0defbfc71c59"
down_revision: Union[str, None] = "29e42ce4be3f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("version") as batch_op:
        batch_op.alter_column("doi", nullable=True)

    op.execute(
        """ALTER TABLE version
               ADD COLUMN identifier SERIAL
        """
    )
    op.execute(f"UPDATE version SET doi = '10.36478/fairhub.' || identifier::TEXT")
    op.create_unique_constraint("unique_identifier", "version", ["identifier"])
    op.create_unique_constraint("unique_doi", "version", ["doi"])
