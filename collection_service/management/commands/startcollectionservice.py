from django.core.management.base import BaseCommand
from subprocess import Popen, TimeoutExpired
from sys import stdout, stderr
import os
import signal
import time
class Command(BaseCommand):
    help = "Starts the Django REST server with Uvicorn and the gRPC server."

    grpc_port = os.getenv("GRPC_SERVER_PORT", "50051")
    rest_port = os.getenv("REST_SERVER_PORT", "8000")

        # Befehle für Uvicorn (REST) und gRPC
    
    rest_command = [
            "gunicorn",
            "config.asgi:application",
            "-k",
            "uvicorn_worker.UvicornWorker",
            "--bind",
            f"0.0.0.0:{rest_port}",
            "--workers",
            str(4),
            "--access-logfile", "-",
            "--log-level", "info",
        ]
    grpc_command = ["python", "manage.py", "grpcrunserver", f"0.0.0.0:{grpc_port}"]
    


    def handle(self, *args, **options):
        
        # Prozesse starten
        rest_process = Popen(self.rest_command, stdout=stdout, stderr=stderr)
        grpc_process = Popen(self.grpc_command, stdout=stdout, stderr=stderr)

        self.stdout.write(f"REST server started on port {self.rest_port}.")
        self.stdout.write(f"gRPC server started on port {self.grpc_port}.")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stdout.write("\nStopping both servers...")
            rest_process.send_signal(signal.SIGTERM)
            grpc_process.terminate()

            # Warten, bis die Prozesse beendet sind
            try:
                rest_process.wait(timeout=5)
                grpc_process.wait(timeout=5)
            except TimeoutExpired:
                self.stdout.write(f"Process {proc.pid} did not terminate in time. Forcing termination.")
                rest_process.kill()
                grpc_process.kill()

            self.stdout.write("Both servers have been stopped.")
            self.stdout.flush()



    def handledfjsd(self, *args, **options):
        proc_list = []

        # Starte beide Server-Prozesse mit den kompletten Commands als Strings
        for command in self.commands:
            proc = Popen(command, stdout=stdout, stderr=stderr)
            self.stdout.write(f"Server started with command: {' '.join(command)}")
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