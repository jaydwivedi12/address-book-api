# Address Book API
A production-ready Address Book REST API built with FastAPI.

## Features

- Create address
- Update address
- Delete address
- Retrieve all addresses
- Find addresses within a given distance
- SQLite database
- Input validation
- Structured logging
- Global error handling
- API versioning (`/api/v1`)

## Tech Stack

- FastAPI
- SQLAlchemy (ORM)
- SQLite
- Pydantic
- Geopy


## Project Structure

```

address-book-api/
│
├── app/
│   ├── api/              # Route handlers
│   ├── core/             # Logging & configuration
│   ├── db/               # Database session & base
│   ├── models/           # ORM models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic layer
│   ├── dependencies.py   # Dependency injection
│   └── main.py           # Application entry point
│
├── tests/
├── requirements.txt
├── .gitignore
└── README.md

````


# How To Run The Application

## 1. Clone the repository

```bash
git clone https://github.com/jaydwivedi12/address-book-api
cd address-book-api
````

## 2. Create a virtual environment

```bash
python3 -m venv venv
```

### Activate it:

**Mac/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Create `.env` file

Create a file named `.env` in the project root with:

```
DATABASE_URL=sqlite:///./address.db
```


## 5. Run the application

```bash
uvicorn app.main:app --reload
```


## 6. Access API Documentation

**Swagger UI**

```
http://127.0.0.1:8000/docs
```


# 🐳 Running with Docker

## Build the image

```bash
docker build -t address-book-api .
```

## Run the container
```bash
docker run -p 8000:8000 --env-file .env address-book-api
```

***API will be availabe at:***

```
http://127.0.0.1:8000/docs
```

# API Endpoints

Base path:

```
/api/v1/addresses
```

### Create Address

`POST /api/v1/addresses`

### Get All Addresses

`GET /api/v1/addresses`

### Update Address

`PUT /api/v1/addresses/{address_id}`

### Delete Address

`DELETE /api/v1/addresses/{address_id}`

### Find Nearby Addresses

`GET /api/v1/addresses/nearby?latitude=...&longitude=...&distance_km=...`


# Validation Rules

* Latitude must be between -90 and 90
* Longitude must be between -180 and 180
* Distance must be greater than 0
* Name cannot be blank

---

# Logging

The application logs:

* Incoming requests
* Successful operations
* Failed database operations
* Unexpected server errors
* Request duration



## Configuration

All configuration is externalized using environment variables.

### Required Environment Variable:

* `DATABASE_URL`



## Testing

This project includes automated tests using:

- pytest
- FastAPI TestClient

### Run tests

Make sure your virtual environment is activated, then run:

```bash
pytest
```

### Expected output

```
3 passed
```

### What is tested?

* Successful address creation
* Retrieval of stored addresses
* Nearby search functionality

The test suite validates core API behavior and helps prevent regressions.


##  Health Check

**GET /health**

Returns:

```json
{
  "status": "ok"
}
```