## Django gRPC API

A backend API built with Django and gRPC. The server exposes a UserService that can fetch and list users. Clients must use a gRPC client to communicate with it — not REST or a browser.
gRPC runs on port 50051. Django runs on port 8000.
Data is structured using Protocol Buffers (.proto files) instead of JSON.
This project is the foundation for learning how backend services communicate with each other using gRPC — faster, typed, and more structured than REST.

## Tech Stack

- Python 3.13
- Django 6.0
- gRPC / Protocol Buffers
- Pipenv (dependency management)
- SQLite (development database)

## Services

The UserService exposes two RPC methods:

- `GetUser` — fetch a single user by ID
- `ListUsers` — fetch all users

## Getting Started

### 1. Clone the repo

git clone https://github.com/YOUR_USERNAME/django-grpc.git
cd django-grpc

### 2. Install dependencies

pipenv install

### 3. Activate virtual environment

pipenv shell

### 4. Run migrations

python manage.py migrate

### 5. Create a superuser

python manage.py createsuperuser

### 6. Regenerate gRPC code (if you change the proto file)

python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/users.proto

### 7. Start the gRPC server

python manage.py grpcserver

Server runs on port 50051.

## Testing with grpcurl

List available services:
grpcurl -plaintext localhost:50051 list

Get a user by ID:
grpcurl -plaintext -d '{\"id\": 1}' localhost:50051 users.UserService/GetUser

List all users:
grpcurl -plaintext localhost:50051 users.UserService/ListUsers

## Project Structure

core/ Django project config (settings, urls, wsgi)
users/ Users app (models, servicer, management commands)
protos/ Protocol Buffer definitions
users_pb2.py Auto-generated protobuf messages
users_pb2_grpc.py Auto-generated gRPC servicer base
