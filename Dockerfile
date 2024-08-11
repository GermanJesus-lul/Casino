# Verwenden Sie ein offizielles Python-Image als Basis
FROM python:3.9-slim

# Setzen Sie das Arbeitsverzeichnis
WORKDIR /app

# Kopieren Sie die requirements-Datei und installieren Sie die Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den Rest der Anwendung
COPY . .

# Exposen Sie den Port, auf dem die Anwendung läuft
EXPOSE 3000

# Starten Sie die Anwendung
CMD ["bash", "entrypoint.sh"]
