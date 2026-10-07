FROM python:3.12-slim

# Keep Python output immediate and avoid bytecode files in the image.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# All application commands run from this directory.
WORKDIR /app

# Install dependencies in a separate layer so Docker can reuse it when app.py changes.
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the Flask application and template/static assets into the image.
COPY app.py .
COPY templates ./templates
COPY static ./static

# Document the port used by the Flask API.
EXPOSE 5000

# Bind Flask to every container interface so the published port is reachable.
CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=5000"]
