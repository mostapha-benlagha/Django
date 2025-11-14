# Django REST API with MongoDB

A RESTful API built with Django REST Framework and MongoDB using mongoengine. This project provides endpoints for managing items, customers, and orders with JWT authentication.

## Features

- 🔐 JWT-based authentication (register, login, token refresh)
- 📦 CRUD operations for Items
- 👥 Customer management
- 🛒 Order management
- 🗄️ MongoDB integration with mongoengine
- 🔒 Protected endpoints with JWT authentication
- 🐍 Python 3.13 compatible

## Tech Stack

- **Django** 5.2.8
- **Django REST Framework** - API framework
- **djangorestframework-simplejwt** - JWT authentication
- **MongoDB** - NoSQL database
- **mongoengine** - MongoDB ODM for Python
- **pymongo** - MongoDB driver
- **legacy-cgi** - Python 3.13 compatibility

## Prerequisites

- Python 3.13+
- MongoDB (running on localhost:27017)
- pip (Python package manager)

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Ensure MongoDB is running**:
   - MongoDB should be running on `localhost:27017`
   - The database name is `mydatabase` (configurable in `myproject/settings.py`)

6. **Run migrations** (for Django's built-in apps):
   ```bash
   python manage.py migrate
   ```

7. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## Configuration

### MongoDB Connection

The MongoDB connection is configured in `myproject/settings.py`:

```python
mongoengine.connect(db="mydatabase", host="mongodb://localhost:27017")
```

To change the database or connection string, modify this line in `settings.py`.

## API Endpoints

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication Endpoints

#### Register User
- **URL:** `/api/auth/register/`
- **Method:** `POST`
- **Authentication:** Not required
- **Request Body:**
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```
- **Response:** User data and JWT tokens
  ```json
  {
    "user": {
      "id": "691692e6f7f1f73f372f32b7",
      "username": "john_doe",
      "email": "john@example.com"
    },
    "tokens": {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
  }
  ```

#### Login
- **URL:** `/api/auth/login/`
- **Method:** `POST`
- **Authentication:** Not required
- **Request Body:**
  ```json
  {
    "username": "john_doe",
    "password": "securepassword123"
  }
  ```
- **Response:** User data and JWT tokens (same format as register)

#### Refresh Token
- **URL:** `/api/auth/refresh/`
- **Method:** `POST`
- **Authentication:** Not required
- **Request Body:**
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
  ```
- **Response:** New access token

### Items Endpoints

#### List All Items
- **URL:** `/api/`
- **Method:** `GET`
- **Authentication:** Required (JWT)
- **Response:** Array of items

#### Create Item
- **URL:** `/api/`
- **Method:** `POST`
- **Authentication:** Required (JWT)
- **Request Body:**
  ```json
  {
    "name": "Product Name",
    "description": "Product description"
  }
  ```

#### Get Item by ID
- **URL:** `/api/<item_id>/`
- **Method:** `GET`
- **Authentication:** Required (JWT)

#### Update Item (Full)
- **URL:** `/api/<item_id>/`
- **Method:** `PUT`
- **Authentication:** Required (JWT)

#### Update Item (Partial)
- **URL:** `/api/<item_id>/`
- **Method:** `PATCH`
- **Authentication:** Required (JWT)

#### Delete Item
- **URL:** `/api/<item_id>/`
- **Method:** `DELETE`
- **Authentication:** Required (JWT)

### Customers Endpoints

#### List All Customers
- **URL:** `/api/customers/`
- **Method:** `GET`
- **Authentication:** Required (JWT)

#### Get Customer by ID
- **URL:** `/api/customers/<customer_id>/`
- **Method:** `GET`
- **Authentication:** Required (JWT)

### Orders Endpoints

#### List All Orders
- **URL:** `/api/orders/`
- **Method:** `GET`
- **Authentication:** Required (JWT)

#### Create Order
- **URL:** `/api/orders/`
- **Method:** `POST`
- **Authentication:** Required (JWT)
- **Request Body:**
  ```json
  {
    "customer": {
      "name": "Customer Name",
      "email": "customer@example.com"
    },
    "item": {
      "name": "Product Name",
      "description": "Product description"
    },
    "quantity": 5
  }
  ```

#### Get Order by ID
- **URL:** `/api/orders/<order_id>/`
- **Method:** `GET`
- **Authentication:** Required (JWT)

## Authentication

This API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. **Register or Login** to get access and refresh tokens
2. **Include the access token** in the Authorization header:
   ```
   Authorization: Bearer <access_token>
   ```

### Token Lifetime
- **Access Token:** 15 minutes
- **Refresh Token:** 7 days

### Example Request with Authentication

```bash
curl -X GET http://127.0.0.1:8000/api/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
  -H "Content-Type: application/json"
```

## Usage Examples

### Using cURL

#### Register a new user:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

#### Login:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

#### Get all items (with authentication):
```bash
curl -X GET http://127.0.0.1:8000/api/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

### Using Python requests

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api"

# Register
response = requests.post(f"{BASE_URL}/auth/register/", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
})
tokens = response.json()["tokens"]
access_token = tokens["access"]

# Use token for authenticated requests
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Get items
response = requests.get(f"{BASE_URL}/", headers=headers)
items = response.json()
```

## Project Structure

```
myproject/
├── api/                      # Main API application
│   ├── authentication.py     # Custom JWT authentication for MongoDB
│   ├── models.py             # MongoDB models (User, Item, Customer, Order)
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # API views
│   ├── urls.py               # API URL routing
│   └── services/             # Business logic layer
│       ├── auth.py           # Authentication services
│       ├── items.py          # Item services
│       ├── customers.py      # Customer services
│       └── orders.py         # Order services
├── myproject/                 # Django project settings
│   ├── settings.py           # Django settings
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI configuration
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Database Models

### User
- `username` (String, unique, required)
- `email` (String, unique, required)
- `password` (String, hashed, required)
- `created_at` (DateTime)

### Item
- `name` (String, required)
- `description` (String, optional)
- `created_at` (DateTime)

### Customer
- `name` (String, required)
- `email` (String, unique, required)
- `created_at` (DateTime)

### Order
- `quantity` (Integer, required)
- `customer` (Reference to Customer)
- `item` (Reference to Item)
- `created_at` (DateTime)

## Error Handling

The API returns standard HTTP status codes:

- `200 OK` - Successful GET, PUT, PATCH requests
- `201 Created` - Successful POST requests
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `404 Not Found` - Resource not found
- `405 Method Not Allowed` - Invalid HTTP method

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
For Django's built-in apps:
```bash
python manage.py makemigrations
python manage.py migrate
```

Note: MongoDB models (User, Item, Customer, Order) don't require migrations as they use mongoengine.

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `mongod` or check your MongoDB service
- Verify connection string in `settings.py`
- Check MongoDB is accessible on `localhost:27017`

### JWT Token Issues
- Tokens expire after 15 minutes (access) or 7 days (refresh)
- Use the refresh endpoint to get a new access token
- Ensure you're including the token in the Authorization header with "Bearer " prefix

### Python 3.13 Compatibility
- The `legacy-cgi` package is included for Python 3.13 compatibility
- If you encounter `cgi` module errors, ensure `legacy-cgi` is installed

## License

This project is open source and available for use.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

