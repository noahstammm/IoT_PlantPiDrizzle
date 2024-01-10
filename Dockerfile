# Verwende ein Basisimage mit Python und Flask-Abhängigkeiten
FROM python:3.10.0

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die Anwendungsdateien in das Arbeitsverzeichnis
COPY app.py /app/app.py
COPY templates /app/templates

# Installiere die erforderlichen Python-Pakete
RUN pip install flask matplotlib pymongo apscheduler

# Exponiere den Port, auf dem die Anwendung läuft
EXPOSE 5000

# Starte die Anwendung beim Start des Containers
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]

