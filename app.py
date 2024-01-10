from flask import Flask, render_template
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import datetime
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# MongoDB-Konfiguration
mongo_uri = 'mongodb+srv://janosi:1234@cluster.lp4msmq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
db_name = 'IoT'
collection_name = 'Cluster'

# Verbindung zur MongoDB herstellen
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

# Zwischengespeicherte Daten
cached_data = {'timestamps': [], 'moisture_levels': []}

# Funktion zum Abrufen von Daten
def get_data():
    formatted_timestamps, moisture_levels = get_data_from_mongo()
    cached_data['timestamps'] = formatted_timestamps
    cached_data['moisture_levels'] = moisture_levels

# Funktion zum periodischen Abrufen von Daten
def get_data_periodically():
    scheduler.add_job(func=get_data, trigger='date')

# Indexroute
@app.route('/')
def index():
    get_data()  # Daten sofort abrufen
    plot_url, warning_message = create_plot(cached_data['timestamps'], cached_data['moisture_levels'])

    return render_template('dashboard.html', plot_url=plot_url, warning_message=warning_message)

# Scheduler für die periodische Aktualisierung
scheduler = BackgroundScheduler()
scheduler.add_job(func=get_data_periodically, trigger='interval', seconds=60)  # Aktualisiere alle 60 Sekunden
scheduler.start()

def get_data_from_mongo():
    cursor = collection.find().sort('timestamp', -1).limit(10)

    # Extrahiere die Zeitstempel und Feuchtigkeitswerte aus allen Dokumenten
    timestamps = []
    moisture_levels = []

    # Gruppiere die Datenpunkte nach der Minute des Zeitstempels
    grouped_data = {}

    for entry in cursor:
        timestamp = entry['timestamp']
        datetime_obj = datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=datetime.timezone.utc)
        formatted_time = datetime_obj.strftime('%Y-%m-%d %H:%M')

        # Gruppiere die Datenpunkte nach der Minute des Zeitstempels
        if formatted_time in grouped_data:
            grouped_data[formatted_time].append(entry['moisture_level'])
        else:
            grouped_data[formatted_time] = [entry['moisture_level']]

    # Berechne den Durchschnitt für jede Minute
    for timestamp, values in grouped_data.items():
        average_moisture = sum(values) / len(values)
        timestamps.append(timestamp)
        moisture_levels.append(average_moisture)

    return timestamps, moisture_levels



def create_plot(timestamps, values):
    fig, ax = plt.subplots(figsize=(15, 6))

    # Färbe die Punkte rot, wenn moisture_level gleich 0 ist
    colors = ['red' if value == 0 else 'blue' for value in values]

    # Invertiere die Achsen, um das neueste Datum rechts zu platzieren
    ax.invert_xaxis()

    # Zeichne eine Linie, die die Punkte verbindet
    for i in range(len(timestamps) - 1):
        line_color = 'red' if values[i] == 0 else 'blue'
        ax.plot([timestamps[i], timestamps[i + 1]], [values[i], values[i + 1]], marker='o', linestyle='-', color=line_color)

    # Füge die farbigen Punkte hinzu
    ax.scatter(timestamps, values, color=colors, marker='o')

    ax.set(xlabel='Zeitstempel', ylabel='Werte', title='Diagramm')
    ax.grid()

    # Überprüfe, ob die Werte für heute 0 sind
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    print('today',today)

    # Extrahiere die Werte für den aktuellen Tag
    today_values = [value for timestamp, value in zip(timestamps, values) if timestamp.startswith(today)]

    # Überprüfe, ob mindestens ein Wert für den heutigen Tag 0 ist und zeige eine Warnung
    if any(value == 0 for value in today_values):
        warning_message = 'ACHTUNG! Deine Pflanze hat möglicherweise Durst!'
    else:
        warning_message = ''

    # Konvertiere das Diagramm in ein Bild, das in HTML eingebettet werden kann
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    plt.close(fig)
    print('warning_message', warning_message)

    return f'data:image/png;base64,{plot_url}', warning_message







if __name__ == '__main__':
    app.run(debug=True)
