import os
import signal
import subprocess
from sys import stdout, stderr
import time
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Start both REST and gRPC servers using Gunicorn with UvicornWorker."

    def add_arguments(self, parser):
        parser.add_argument(
            "--rest-port", type=int, default=8000, help="Port for the REST server (default: 8000)"
        )
        parser.add_argument(
            "--grpc-port", type=int, default=50051, help="Port for the gRPC server (default: 50051)"
        )
        parser.add_argument(
            "--rest-workers", type=int, default=4, help="Number of workers for the REST server (default: 4)"
        )
        parser.add_argument(
            "--grpc-workers", type=int, default=2, help="Number of workers for the gRPC server (default: 2)"
        )

    def handle(self, *args, **options):

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

        rest_port = options["rest_port"]
        grpc_port = options["grpc_port"]
        rest_workers = options["rest_workers"]
        grpc_workers = options["grpc_workers"]

        self.stdout.write("Starting both REST and gRPC servers...")

        # Gunicorn command for REST server
        rest_command = [
            "gunicorn",
            "config.asgi:application",
            "-k",
            "uvicorn_worker.UvicornWorker",
            "--bind",
            f"0.0.0.0:{rest_port}",
            "--workers",
            str(rest_workers),
        ]

        # Gunicorn command for gRPC server
        grpc_command = ["python", "manage.py", "grpcrunserver", f"0.0.0.0:{grpc_port}"]
        # grpc_command = [
        #     "gunicorn",
        #     "config.asgi:grpc_application",
        #     "-k",
        #     "uvicorn_worker.UvicornWorker",
        #     "--bind",
        #     f"0.0.0.0:{grpc_port}",
        #     "--workers",
        #     str(grpc_workers),
        # ]

        # Start REST server in a subprocess
        rest_process = subprocess.Popen(rest_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Start gRPC server in a subprocess
        grpc_process = subprocess.Popen(grpc_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            # Monitor the processes
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stdout.write("Stopping both servers...")
            self._terminate_process(rest_process, "REST")
            self._terminate_process(grpc_process, "gRPC")
            self.stdout.write("Servers stopped successfully.")

    def _terminate_process(self, process, name):
        """Terminate a subprocess safely."""
        if process.poll() is None:  # Check if the process is still running
            self.stdout.write(f"Terminating {name} server...")
            process.send_signal(signal.SIGINT)  # Send SIGINT signal
            try:
                process.wait(timeout=5)  # Wait for the process to terminate
            except subprocess.TimeoutExpired:
                self.stdout.write(f"Forcing termination of {name} server...")
                process.kill()  # Force terminate if it doesn't stop