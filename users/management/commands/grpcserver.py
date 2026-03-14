from django.core.management.base import BaseCommand # this is djangos base class for custom management commands
import grpc # to create the server
from concurrent import futures # grpc needs a thread pool to handle multiple requests at once
import users_pb2_grpc # contains the function to register our servicer with the server
from users.servicer import UserServicer # the class we just wrote with all the logic
import sys
from grpc_reflection.v1alpha import reflection # Without reflection, the gRPC server works but is "silent"
import users_pb2

class Command(BaseCommand):
    # the class must be called Command, Django looks for the exact same name
    help = "Start the gRPC server"

    def handle(self, *args, **options):
        # this is the method django calls when you run python manage.py grpcserver
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) # this creates the gRPC server with a thread pool of 10 workers -- meaning it can handle up to 10 requests simultaneously without them blocking each other
        users_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server) # this connects your userservicer logic to the server

        # add these two lines
        SERVICE_NAMES = (
            users_pb2.DESCRIPTOR.services_by_name['UserService'].full_name, #  gets the full name of your UserService (users.UserService)
            reflection.SERVICE_NAME,    # adds the reflection service itself to the list    
        )
        reflection.enable_server_reflection(SERVICE_NAMES, server) #Registers all those service names with the server so grpcurl list can discover them

        server.add_insecure_port("[::]:50051") # [::] means listen on all network interfaces (both local and external), 50051 is the default gRPC port, insecure means no SSL/TLS encryption 

        server.start() # starts the server in the background
        self.stdout.write(self.style.SUCCESS("gRPC server running on port 50051..."))# prints a message to the terminal
        sys.stdout.flush()
        server.wait_for_termination() # keeps the server running until you exit