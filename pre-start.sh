#! /usr/bin/env bash

# Let the DB start
python ./app/backend_pre_start.py

# Generate new migration files if there are schema changes
alembic revision --autogenerate -m "Auto-generated migration"

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./app/initial_data.py
