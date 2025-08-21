"""Atualiza tabela empresas

Revision ID: d03074628a7e
Revises: 077d55a5d55d
Create Date: 2025-08-20 21:51:07.509202

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd03074628a7e'
down_revision: Union[str, Sequence[str], None] = '077d55a5d55d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Tabela colaboradores
    op.add_column(
        'colaboradores',
        sa.Column(
            'role',
            sa.Enum('SUPER_USER', 'EMPRESA', 'ADMIN', 'COLABORADOR', name='role', native_enum=False),
            nullable=False,
            server_default='COLABORADOR'  # valor padrão para registros existentes
        )
    )
    op.add_column(
        'colaboradores',
        sa.Column(
            'status',
            sa.Enum('ATIVO', 'INATIVO', name='status', native_enum=False),
            nullable=False,
            server_default='ATIVO'
        )
    )

    # Tabela empresas
    op.add_column(
        'empresas',
        sa.Column(
            'role',
            sa.Enum('SUPER_USER', 'EMPRESA', 'ADMIN', 'COLABORADOR', name='role', native_enum=False),
            nullable=False,
            server_default='EMPRESA'  # valor padrão para registros existentes
        )
    )
    op.add_column(
        'empresas',
        sa.Column(
            'status',
            sa.Enum('ATIVO', 'INATIVO', name='status', native_enum=False),
            nullable=False,
            server_default='ATIVO'
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Tabela empresas
    op.drop_column('empresas', 'status')
    op.drop_column('empresas', 'role')

    # Tabela colaboradores
    op.drop_column('colaboradores', 'status')
    op.drop_column('colaboradores', 'role')
