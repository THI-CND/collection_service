from django.core.management.base import BaseCommand
from sys import stdout, stderr
from subprocess import Popen, TimeoutExpired
import time

class Command(BaseCommand):
    help = "Starts both the Django REST server and the gRPC server."

    commands = [
        ['python', 'manage.py', 'grpcrunserver', '0.0.0.0:50051'],
        ['python', 'manage.py', 'runserver', '0.0.0.0:8000']
    ]

    def handle(self, *args, **options):
        proc_list = []

        # Starte beide Server-Prozesse mit den kompletten Commands als Strings
        for command in self.commands:
            proc = Popen(command, stdout=stdout, stderr=stderr)
            proc_list.append(proc)

        # Warte auf KeyboardInterrupt und stoppe die Prozesse
        try:
            while True:
                time.sleep(1)  # Verhindere, dass der Hauptthread sofort beendet wird
        except KeyboardInterrupt:
            self.stdout.write("\nStopping both servers...")

            # Sende SIGTERM an alle Prozesse, um sie sicher zu stoppen
            for proc in proc_list:
                proc.terminate()  # Sanftes Beenden der Prozesse
                try:
                    proc.wait(timeout=5)  # Warte auf das Beenden des Prozesses
                except TimeoutExpired:
                    # Falls der Prozess nicht innerhalb der Zeit beendet wird, zwinge ihn zum Stoppen
                    self.stdout.write(f"Process {proc.pid} did not terminate in time. Forcing termination.")
                    proc.kill()

            self.stdout.write("Both servers have been stopped.")
            self.stdout.flush()