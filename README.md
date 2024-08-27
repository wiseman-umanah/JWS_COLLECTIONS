# JWS Collections

JWS Collections is an e-commerce platform API built using Flask and SQLAlchemy. It provides endpoints for user authentication, product management, cart management, and order processing. 

## Features

- User Authentication (Sign up, Log in, Log out)
- Product Management (Add, Update, List, and Delete Products)
- Cart Management (Add items to cart, View cart, Remove items from cart)
- Order Management (Checkout process)
- Swagger API Documentation
- JWT-based Authentication
- CORS support

## Installation

### Prerequisites

- Python 3.11+
- MySQL or MariaDB

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/wiseman-umanah/JWS_COLLECTIONS.git
    cd JWS_COLLECTIONS
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

4. Create a `.env` file to store your environment variables:

    ```plaintext
        SECRET_KEY=yoursecretkey
        DB_USER=your_db_user
        DB_PASSWORD=your_db_password
        DB_HOST=yourhostname
        DB_PORT=yourdbport
        DB_NAME=yourdbname
        SSL_CA=path_to_yourprivatekey
        STORAGE_METHOD=db(this specific whether to use database storage or file storage)

    ```

5. Start the Flask application:

    ```bash
    python3 -m api.v1.app
    ```
    OR
    ```bash
    gunicorn api.v1.app:app
    ```

## Usage

### Authentication

- **Sign Up**: POST `/api/v1/signup`
User sign up to create new user. New User:

```bash
curl -X 'POST' \
  'https://{host | localhost}:{port number | 5000 | 8000}/api/v1/signup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "yourpassword",
  "username": "Bobby",
  "firstname": "Bob",
  "lastname": "Dylan",
}'
  -H 'accept: application/json'
```

- **Log In**: POST `/api/v1/login`
Log in to use API, this returns a session token for authorization use

```bash
curl -X 'POST' \
  'https://{host | localhost}:{port number | 5000 | 8000}/api/v1/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "yourpassword",
}'
```

### Products

- **Add Product**: POST `/api/v1/products` (Admin only)
This route is for admin use only to create and add new product to database.

```bash
curl -X 'POST' \
  'https://{host | localhost}:{port number | 5000 | 8000}/api/v1/products' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {your session token}' \
  -d '{
  "shoe_name": "Air Max 95",
  "shoe_category": "sneakers",
  "shoe_brand": "Nike",
  "shoe_price": 10,
  "shoe_color": "brown",
  "shoe_image": "https://www.imgur.com/..."
}'
```

- **Update Product**: PUT `/api/v1/products/<id>` (Admin only)
Updating products in database, restricted to add use only

```bash
curl -X 'PUT' \
  'https://{host | localhost}:{port number | 5000 | 8000}/api/v1/products/{id of the product}' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {your session token}' \
  -d '{
  "shoe_price": 10,
  "shoe_color": "yellow"
}'
```

- **List Products**: GET `/api/v1/products` (Global to anybody, no signin required)
Retrieve all stocks and products available in database

```bash
curl -X 'GET' \
  'https://{host | localhost}:{port number | 5000 | 8000}/api/v1/products'
```

- **Delete Product**: DELETE `/api/v1/products/<id>` (Admin only)
Product deletion restricted to only Admins

```bash
curl -X 'DELETE' \
  'https://{host | localhost}:{port number | 5000 | 8000}/api/v1/products/{ the id of product }' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {your session token}'
```

### Cart

- **Add to Cart**: POST `/api/v1/cart/add`
Add product to cart. New cart created if not available
Only logged in users

```bash
curl -X 'POST' \
  'https://{host | localhost}:{port number | 5000 | 8000}/api/v1/cart/add' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {your session token}' \
  -d '{
  "shoe_id": "shoe123",
  "quantity": 1
}'
```

- **View Cart**: GET `/api/v1/cart`
Retrieves the cart of logged in user

```bash
curl -X 'GET' \
  'https://{host | localhost}:{port number | 5000 | 8000}/api/v1/cart' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {your session token}'
```

- **View All Carts**: GET `/api/v1/carts` (Admin only)
Restricted to only admins. To get all carts

```bash
curl -X 'GET' \
  'https://{host | localhost}:{port number | 5000 | 8000}/api/v1/carts' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {your session token}' \
```

### Orders

- **Checkout**: POST `/api/v1/checkout`
Cart checking and payment implementation of logged in user

```bash
curl -X 'POST' \
  'https://{host | localhost}:{port number | 5000 | 8000}/api/v1/checkout' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {your session token}'
```

- **View All Orders**: GET `/api/v1/orders/<order_id>` (Admin only)
Get all orders made, restricted to only admins

```bash
curl -X 'GET' \
  'https://{host | localhost}:{port number | 5000 | 8000}/api/v1/orders/{order id}' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {your session token}'
```

### Users

- **View all Users**: GET `api/v1/users` (Admin Only)

## API Documentation

The API documentation is available at `/swagger`

Visit: [On Vercel](https://jws-collections-gi44.vercel.app/swagger/)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a new Pull Request

## Development
The Database storage method has been thoroughly tested as compared to the File storage system which might shows which is under development.

`Please use database storage i.e STORAGE_METHOD=db`

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/wiseman-umanah/JWS_COLLECTIONS/blob/master/LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Flask-Swagger-UI](https://github.com/swagger-api/swagger-ui)
- [Flask-CORS](https://flask-cors.readthedocs.io/)

## Developers
- [ Wiseman Umanah ](https://github.com/wiseman-umanah)
- [ Sandra Oghenesode ](https://github.com/sandysode)
- [ Jane Wugathi ](https://github.com/codingbot995)

## Support
Buy us a coffee ☕
