# /scripts/run_migrations.py

import alembic
from alembic.config import Config

def run_migrations():
	alembic_cfg = Config("alembic.ini")
	alembic.command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
	run_migrations()