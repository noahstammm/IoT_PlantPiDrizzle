# Verwende ein Basisimage mit Python und Flask-Abhängigkeiten
FROM python:3.8-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die Anwendungsdateien in das Arbeitsverzeichnis
COPY app.py /app/app.py
COPY templates /app/templates

# Installiere die erforderlichen Python-Pakete
RUN pip install flask matplotlib pymongo apscheduler

# Exponiere den Port, auf dem die Anwendung läuft
EXPOSE 8080

# Starte die Anwendung beim Start des Containers
CMD ["python", "app.py"]
