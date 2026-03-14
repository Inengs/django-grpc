import grpc # needed to send error codes back to the client
import users_pb2 # contains message classes (UserRequest, UserResponse)
import users_pb2_grpc # this users_pb2_grpc contains the base servicer class ans we want to fill in actual logic
from django.contrib.auth.models import User # used to query database for users

class UserServicer(users_pb2_grpc.UserServiceServicer):
    # this inherits from generated base class
    def GetUser(self, request, context):
        # request is the incoming data from the client, context allows you send back errors or metadata to the client
        try: 
            user = User.objects.get(pk=request.id) # find the user whose primary keys matches the ID the client sent
            return users_pb2.UserResponse(
                # take the user we found and pack it into a UserResponse protobuf message 
                id=user.id,
                username=user.username,
                email=user.email,
            )
        except User.DoesNotExist:
            # if no user is found with that ID
            context.set_code(grpc.StatusCode.NOT_FOUND) #  sends a NOT_FOUND status back 
            context.set_details(f"User {request.id} not found") # sends a human readable error message
            return users_pb2.UserResponse() # returns an empty response
        
    def ListUsers(self, request, context):
        users = User.objects.all() # give me every user in the database
        return users_pb2.UsersResponse(
            users=[
                users_pb2.UserResponse(
                    id=u.id,
                    username=u.username,
                    email=u.email
                )
                for u in users
            ]
        )
    # [do_something(item) for item in collection] - list comprehension


