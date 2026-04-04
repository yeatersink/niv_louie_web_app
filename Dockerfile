FROM zauberzeug/nicegui:latest

WORKDIR /app

# Install dependencies
COPY requirements.txt* ./
RUN uv pip install -r requirements.txt

# Explicitly copy static files first (this is the most reliable way)
COPY static/ /app/static/

# Copy the rest of the application code
COPY . .

EXPOSE 8080

CMD ["python", "gui.py"]