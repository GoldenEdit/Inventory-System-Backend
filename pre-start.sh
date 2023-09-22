#! /usr/bin/env bash

echo "Starting pre-start.sh script..."

# Let the DB start
echo "Running backend_pre_start.py..."
python ./app/backend_pre_start.py

# Generate new migration files if there are schema changes
echo "Generating new migration files..."
alembic revision --autogenerate -m "Auto-generated migration"

# Run migrations
echo "Running migrations..."
alembic upgrade head

# Create initial data in DB
echo "Creating initial data in DB..."
python ./app/initial_data.py

echo "Exiting pre-start.sh script."
