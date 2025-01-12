from django.core.management.base import BaseCommand
from subprocess import Popen, TimeoutExpired
from sys import stdout, stderr
from django.conf import settings
import signal
import time

# Management command for production to start the Django REST server with Uvicorn and the gRPC server
class Command(BaseCommand):
    help = "Starts the Django REST server with Uvicorn and the gRPC server."

    grpc_port = settings.GRPC_SERVER_PORT
    rest_port = settings.REST_SERVER_PORT

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
    grpc_command = [
            "python",
            "manage.py",
            "grpcrunserver",
            f"0.0.0.0:{grpc_port}",
        ]


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
            processes = [rest_process, grpc_process]
            for proc in processes:
                try:
                    proc.wait(timeout=5)
                except TimeoutExpired:
                    self.stdout.write(f"Process {proc.pid} did not terminate in time. Forcing termination.")
                    proc.kill()

            self.stdout.write("Both servers have been stopped.")
            self.stdout.flush()