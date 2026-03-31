FROM zauberzeug/nicegui:latest

WORKDIR /app

# Copy requirements if it exists, otherwise skip
COPY requirements.txt* ./
RUN pip install --no-cache-dir -r requirements.txt || echo "No requirements.txt - skipping"

# Copy all your project files
COPY . .

# Expose the port NiceGUI will run on
EXPOSE 8080

# Run your app
CMD ["python", "gui.py"]