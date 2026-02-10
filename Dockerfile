# Folosim o versiune ușoară de Python
FROM python:3.9-slim

# Setăm folderul de lucru
WORKDIR /app

# Copiem fișierele tale în container
COPY . .

# Instalăm ingredientele
RUN pip install --no-cache-dir -r requirements.txt

# Pornim botul
CMD ["python", "main.py"]
