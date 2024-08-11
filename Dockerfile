# Verwenden Sie ein offizielles Python-Image als Basis
FROM python:3.9-slim

# Setzen Sie das Arbeitsverzeichnis
WORKDIR /app

# Installieren Sie Git
RUN apt-get update && apt-get install -y git

# Kopieren Sie die requirements-Datei und installieren Sie die Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den Rest der Anwendung
COPY . .

# Kopieren des Initialisierungsskripts
COPY init_db.py .

# Setzen Sie die Umgebungsvariable für Git
ENV GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git
# Exponieren Sie den Port, auf dem die Anwendung läuft
EXPOSE 5000

# Starten Sie die Anwendung
CMD ["sh", "-c", "python init_db.py && python flask_app.py"]