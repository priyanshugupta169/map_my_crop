# Map My Crop Weather Service

This project implements a weather service API using FastAPI, providing functionalities to register users, authenticate them, and retrieve historic weather data.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/priyanshugupta169/map_my_crop.git
   cd map_my_crop
   ```

2. **Install dependencies using makefile:**
   ```bash
   make setup
   ```

3. **Install dependencies using Docker:**
   ```bash
   docker build -t map_my_crop . 
   ```

## Features

1. **Endpoints:**
   - User Registration.
   - User Authentication.
   - Protected Endpoints(Allowed only after user is logged in)
   - Retrieve Historic Weather Data(Weather data is obtained from the Open Meteo API.)

2. **Data Validation:**
   - Data validation is implemented using Pydantic models.

3. **Documentation:**
   - Comments have been added to the code for better understanding.

4. **Error Handling:**
   - Proper error handling is implemented for invalid requests.

## Usage

1. **Run the FastAPI application using makefile:**
   ```bash
   make run
   ```

2. **Run the FastAPI application using Docker:**
   ```bash
   docker run -p 8000:8000 map_my_crop
   ```

2. **Access the API documentation:**
   Open your web browser and navigate to `http://localhost:8000/docs` to access the Swagger UI documentation.

3. **Use the provided endpoints to interact with the API.**

## Database Integration

This project currently uses SQLite as the database backend. The database integration and schema design are implemented in the `database.py`, `models.py`, and `schemas.py` files.

## Testing

1. **Testing:**
   
   Tests for the API endpoints are written using FastAPI's test client.
   ```bash
   make test
   ```

## Contributors

- [Priyanshu Gupta](https://github.com/priyanshugupta169)

## License

This project is licensed under the [MIT License](LICENSE).
