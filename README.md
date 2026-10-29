# Minitab Service

A simple HTTP service built with Python and Flask that calculates the arithmetic mean and population standard deviation of a JSON array of numbers.

## Requirements

- Python
- Docker Desktop 

## Run Locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Set the `PORT` enviorment variable:

```powershell
$env:PORT = "8080"
```

The service defaults to port `3000`.

Start the service:

```bash
python app.py
```

## API Endpoints

### GET /

Returns a message confirming the service is running.

**Example response:**

```text
Minitab Service is running!
```

### GET /health

Returns the health status of the service.

**Example response:**

```json
{
  "status": "ok"
}
```

### POST /mean

Accepts a JSON array of numbers and returns the arithmetic mean rounded to three decimal places, with trailing zeros removed.

**Example request:**

```json
[1, 2, 3, 4]
```

**Example response:**

```text
2.5
```

### POST /stddev

Accepts a JSON array of numbers and returns the population standard deviation rounded to three decimal places, with trailing zeros removed.

**Example request:**

```json
[1, 2, 3]
```

**Example response:**

```text
0.816
```

### Input Validation and Errors

Both calculation endpoints return HTTP `400 Bad Request` when the input is invalid.

**1. Empty array**

Request:

```json
[]
```

Response:

```json
{
  "error": "Must contain at least one number"
}
```

**2. Non-numeric values**

Request:

```json
[1, "hello", 3]
```

Response:

```json
{
  "error": "All values must be numbers"
}
```

**3. Boolean values**

Request:

```json
[1, true, 3]
```

Response:

```json
{
  "error": "All values must be numbers"
}
```

**4. Non-array input**

Request:

```json
{
  "value": 5
}
```

Response:

```json
{
  "error": "Must be an array of numbers"
}
```

Malformed JSON is also rejected with HTTP `400 Bad Request`.

## Run Tests

Run the automated tests with:

```bash
python -m pytest -v
```

## Run with Docker

Build the image:

```bash
docker build -t minitab-service .
```

Run the container:

```bash
docker run --rm --name minitab-service-container -p 3000:3000 -e PORT=3000 minitab-service
```

Or use the included PowerShell script:

```powershell
.\run.ps1
```

The service is then available at [http://localhost:3000](http://localhost:3000).
