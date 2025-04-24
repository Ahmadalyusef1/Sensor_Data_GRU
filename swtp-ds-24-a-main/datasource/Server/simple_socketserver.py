import socketserver
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import NewTopic, KafkaAdminClient
import time, datetime
import os

# Pfad zum Speichern des Zählerwerts
counter_file_path = "counter.txt"


class WuerfelServer(socketserver.BaseRequestHandler):
    def handle(self):
        addr = self.client_address[0]
        print("[{}] Verbindung hergestellt".format(addr))
        # l ist eine JSON-Zeile vom Würfel. Da die Übertragung des
        # Streams nicht zwingend zeilenweise funktioniert, liefert l
        # auch den Anfang einer unvollständig empfangenen Zeile.
        # Zählerwert aus der Datei laden
        counter = load_counter()
        l = ""
        while True:
            # l (im Idealfall leer) wird mit dem nächsten empfangenen
            # Paket verkettet.
            s = l + self.request.recv(4096).decode()  # decode wandelt byte-Strom zu String
            if s:
                # print("[{}] {}\n".format(addr, s)) # Kontrollausgabe
                for l in s.splitlines():  # Datenpaket in Zeilen zerlegen
                    # Falls l mit einer geschweiften Klammer endet,
                    # ist ein vollständiger JSON-String enthalten.
                    if len(l) > 0 and l[-1] == '}':
                        gyro = json.loads(l)  # JSON-Zeile -> Dictionary
                        l = ""
                        timestamp = datetime.datetime.now()
                        timestmap_ms = int(timestamp.timestamp() * 1000)
                        # print("date : " , timestamp )
                        # gyro['date'] = timestamp
                        print("timestmap_ms : ", timestmap_ms)
                        print("counter : ", counter)
                        gyro['counter'] = counter
                        gyro['timestamp'] = timestmap_ms
                        print("[{}] {}".format(gyro["n"], gyro["gx"]))  # Ergebnisausgabe (Beispiel)
                        producer.send('swtp_team_a', gyro)
                        # Zähler erhöhen und speichern
                        counter += 1
                        save_counter(counter)
                    else:
                        print(l)  # Debug-Ausgabe
            else:
                print("[{}] Verbindung geschlossen".format(addr))
                break


def load_counter():
    """Den Zählerwert aus einer Datei laden."""
    if os.path.exists(counter_file_path):
        with open(counter_file_path, 'r') as file:
            counter = int(file.read().strip())
    else:
        counter = 0
    return counter


def save_counter(counter):
    """Den Zählerwert in eine Datei speichern."""
    with open(counter_file_path, 'w') as file:
        file.write(str(counter))


if __name__ == '__main__':
    # dict to json
    encode = lambda x: json.dumps(x).encode("utf-8")
    # decode = lambda x: json.loads(x.decode('utf-8'))
    # connect to Kafka

    producer = KafkaProducer(bootstrap_servers="slo.swe.th-luebeck.de:9092", value_serializer=encode, acks=0, retries=3,
                             linger_ms=2, batch_size=0)

    server = socketserver.ThreadingTCPServer(("", 5005), WuerfelServer)
    server.serve_forever()

