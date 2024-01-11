### README.md
## Pflanzen Dashboard
Dieses Repository enthält eine einfache Webanwendung zur Überwachung des Feuchtigkeitsniveaus einer Pflanze. Die Anwendung basiert auf Flask für das Backend, Matplotlib für die Diagrammerstellung und MongoDB für die Speicherung von Daten. Das Frontend wird durch eine HTML-Vorlage (dashboard.html) bereitgestellt.

# Voraussetzungen
Um die Anwendung auszuführen, sind die folgenden Voraussetzungen erforderlich:

Python (Version 3.x empfohlen)
Flask
Matplotlib
pymongo
apscheduler
Sie können die erforderlichen Python-Pakete mit dem folgenden Befehl installieren:

```
pip install Flask matplotlib pymongo apscheduler
```

#Konfiguration
Stellen Sie sicher, dass Sie eine MongoDB-Instanz haben, da die Anwendung darauf zugreift. Konfigurieren Sie die MongoDB-Verbindungsdaten in der app.py Datei:


# MongoDB-Konfiguration
```
mongo_uri = 'mongodb+srv://<BENUTZER>:<PASSWORT>@<CLUSTER>.mongodb.net/<DATENBANK>?retryWrites=true&w=majority'
db_name = 'IoT'
collection_name = 'Cluster'
collection_name2 = 'message'
```
Ersetzen Sie <BENUTZER>, <PASSWORT>, <CLUSTER> und <DATENBANK> durch Ihre eigenen MongoDB-Zugangsdaten.

# Ausführung der Anwendung
Führen Sie die Anwendung mit dem folgenden Befehl aus:

```
python app.py
```

Die Anwendung wird auf http://127.0.0.1:5000/ bereitgestellt. Öffnen Sie diesen Link in Ihrem Webbrowser, um das Dashboard anzuzeigen.

# Struktur der Anwendung
app.py: Enthält die Hauptlogik der Flask-Anwendung, einschließlich der Routen, Datenabruf und Diagrammerstellung.
dashboard.html: Die HTML-Vorlage für das Frontend des Dashboards. Zeigt das Feuchtigkeitsdiagramm, die Bewässerungsinformationen und Warnungen an.

# Datenaktualisierung
Die Anwendung verwendet einen Hintergrund-Scheduler, um die Daten periodisch aus der MongoDB abzurufen und das Diagramm zu aktualisieren. Standardmäßig wird alle 60 Sekunden aktualisiert, aber dies kann in der get_data_periodically Funktion in der app.py Datei angepasst werden.

# Hinweis
Dieses Projekt ist nur als Beispiel gedacht und kann je nach den spezifischen Anforderungen angepasst werden. Es wird empfohlen, die Anwendung gemäß den eigenen Bedürfnissen zu erweitern und zu verbessern.
