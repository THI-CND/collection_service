from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from subprocess import Popen, TimeoutExpired
from sys import stdout, stderr
from django.conf import settings
import signal
import time

# Management command for development to start the Django REST development server and the gRPC server
class Command(BaseCommand):
    help = "Starts the Django REST development server and the gRPC server."

    grpc_port = settings.GRPC_SERVER_PORT
    rest_port = settings.REST_SERVER_PORT

    # Befehle für Uvicorn (REST) und gRPC
    rest_command = ['python', 'manage.py', 'runserver', f'0.0.0.0:{rest_port}']
    grpc_command = ["python", "manage.py", "grpcrunserver", f"0.0.0.0:{grpc_port}"]
    
    def handle(self, *args, **options):
        # Migrationen ausführen
        self.stdout.write("Running migrations...")
        call_command('migrate')

        # Standarddaten laden
        self.stdout.write("Checking if default data needs to be loaded...")
        self.load_default_data()

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

    def load_default_data(self):
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM collection_service_collection')
        if cursor.fetchone()[0] == 0:
            print("No collections found in database. Loading default data...")
            call_command('loaddata', 'default_database.json')
        else:
            print("Collections found in database. Skipping loading default data.")