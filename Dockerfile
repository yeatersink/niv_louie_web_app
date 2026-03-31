FROM zauberzeug/nicegui:latest

WORKDIR /app

# Copy requirements and install using uv (this is the recommended way for NiceGUI Docker images)
COPY requirements.txt* ./
RUN uv pip install -r requirements.txt

# Copy all your project files
COPY . .

EXPOSE 8080

# Run the app
CMD ["python", "gui.py"]