
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN useradd --create-home --shell /usr/sbin/nologin appuser

# Copy application code and assign ownership
COPY --chown=appuser:appuser app.py .

# Run the application without root privileges
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
