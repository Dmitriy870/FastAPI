"""Create post table 

Revision ID: 4fa9675ffcfe
Revises: 4083cf5a2367
Create Date: 2024-09-15 11:02:44.212816

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4fa9675ffcfe"
down_revision: Union[str, None] = "4083cf5a2367"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "post",
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("body", sa.Text(), server_default="", nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("user", sa.Column("username", sa.String(length=20), nullable=False))
    op.create_unique_constraint(None, "user", ["username"])
    op.drop_column("user", "name")
    op.drop_column("user", "price")
    op.drop_column("user", "description")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("description", sa.VARCHAR(), nullable=False))
    op.add_column("user", sa.Column("price", sa.INTEGER(), nullable=False))
    op.add_column("user", sa.Column("name", sa.VARCHAR(length=20), nullable=False))
    op.drop_constraint(None, "user", type_="unique")
    op.drop_column("user", "username")
    op.drop_table("post")
    # ### end Alembic commands ###
