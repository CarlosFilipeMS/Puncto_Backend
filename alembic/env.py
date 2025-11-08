from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Caminho absoluto até a pasta principal do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Agora importa os módulos corretamente
from app.database import Base
from app.models import colaborador, empresa, jornada

# Importa explicitamente os modelos para registrá-los no Base.metadata
from app.models.colaborador import Colaborador
from app.models.empresa import Empresa
from app.models.jornada import Jornada, HorarioJornada

# Config Alembic
config = context.config

# Configura logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# URL do banco
DATABASE_URL = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

# Metadata das models
target_metadata = Base.metadata
# Config Alembic
config = context.config

# Configura logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# === AQUI ESTÁ A ALTERAÇÃO IMPORTANTE ===
# Pegamos a URL do banco de dados do ambiente (Docker)
DATABASE_URL = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    from sqlalchemy import create_engine

    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)


    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
