FROM zauberzeug/nicegui:latest

WORKDIR /app

# Install dependencies
COPY requirements.txt* ./
RUN uv pip install -r requirements.txt

# Force copy the static folder (most reliable method)
COPY static /app/static

# Copy everything else
COPY . .

EXPOSE 8080

CMD ["python", "gui.py"]