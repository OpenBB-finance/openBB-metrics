set -e
while true; do
    echo "Waiting for database to be ready..."
    sleep 10
    echo "Database is ready?"
    echo "Starting alembic upgrade..."
    alembic upgrade head
    echo "Waiting for alembic upgrade to finish..."
    sleep 10
    echo "Alembic upgrade finished"
    echo "Starting uvicorn..."
    uvicorn main:app --host 0.0.0.0 --port 8000
    echo "Api should be running now"
done