# ABAN Crypto Exchange Project

## Introduction

This project is a simplified version of a cryptocurrency exchange platform. It includes basic functionalities for handling user accounts, placing orders, and processing orders with an exchange. The project uses Django and Django REST Framework for the backend API.

## Features

- User registration and authentication
- Creating and viewing exchange rates
- Placing orders for cryptocurrency
- Aggregating small orders for processing
- Simulating order processing with an external exchange

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/parmer110/ABAN_crypto_exchange_project.git
    cd ABAN_crypto_exchange_project
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv env
    source env/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the database:**

    Update the `DATABASES` setting in `crypto_exchange/settings.py` to match your PostgreSQL configuration.

5. **Apply migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

## Usage

### API Endpoints

- **Get Token:**
  
    ```
    POST /api/token/
    {
        "username": "<username>",
        "password": "<password>"
    }
    ```

- **Refresh Token:**
  
    ```
    POST /api/token/refresh/
    {
        "refresh": "<refresh_token>"
    }
    ```

- **Create Order:**
  
    ```
    POST /api/orders/
    {
        "currency_name": "BTC",
        "amount": 0.1
    }
    ```

- **Aggregate Orders:**
  
    ```
    POST /api/orders/aggregate_orders/
    ```

- **Buy from Exchange:**
  
    ```
    POST /api/orders/buy_from_exchange/
    {
        "currency_name": "BTC",
        "amount": 50.0
    }
    ```

### Running Tests

To run the tests, use the following command:

```bash
python manage.py test
