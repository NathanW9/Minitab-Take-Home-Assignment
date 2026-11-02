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

Set the `PORT` environment variable (optional):

```powershell
$env:PORT = "8080"
```

The service defaults to port `3000` if no environment variable is provided.

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

## Input Validation and Errors

Both calculation endpoints validate incoming requests and return appropriate error responses.

Invalid inputs return HTTP `400 Bad Request`.

Examples include:

**1. Empty array**

Request:

```json
[]
```

**2. Non-numeric values**

Request:

```json
[1, "hello", 3]
```

**3. Boolean values**

Request:

```json
[1, true, 3]
```

**4. Non-array input**

Request:

```json
{
  "value": 5
}
```

**5. NaN and Infinity values**

Non-finite values are rejected to prevent invalid calculation results.

Malformed JSON is also rejected with HTTP `400 Bad Request`.

### Request Size Limit

Incoming requests are limited to 1 MB to prevent excessively large payloads from consuming unnecessary application resources.

Requests exceeding this limit return HTTP `413 Request Entity Too Large`.

## Logging

The application uses Python's logging module to record important events and errors.

Logging includes:
- Application startup and the port being used.
- Warnings when invalid input is received.
- HTTP requests recorded by Flask's development server.

When running in Docker, application logs can be viewed using:

```powershell
docker logs minitab-service-container
```

## Run Tests

Run the automated tests with:

```bash
python -m pytest -v
```

The tests cover calculation results, input validation, oversized requests, and application health checks.

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

## Testing the Running Service

Once the service is running, open a separate PowerShell window to test the endpoints, make sure port number is correct

Home endpoint
```powershell
irm http://localhost:3000/
```

Health check
```powershell
irm http://localhost:3000/health
```

Calculate mean (expected: 3)
```powershell
irm http://localhost:3000/mean -Method Post -ContentType "application/json" -Body '[1, 2, 3, 4, 5]'
```

Calculate population standard deviation (expected: 1.414)
```powershell
irm http://localhost:3000/stddev -Method Post -ContentType "application/json" -Body '[1, 2, 3, 4, 5]'
```

Empty array
```powershell
irm http://localhost:3000/mean -Method Post -ContentType "application/json" -Body '[]'
```

Non-numeric values
```powershell
irm http://localhost:3000/stddev -Method Post -ContentType "application/json" -Body '[1, "hello", 3]'
```

## Continuous Integration

The project uses GitHub Actions to automatically run checks when changes are pushed or a pull request is opened.

The workflow:
1. Checks out the repository.
2. Sets up Python 3.13.
3. Installs project dependencies.
4. Runs automated tests using pytest.
5. Builds the Docker image to verify the Docker configuration.

This helps catch errors and confirm that the application and Docker image build successfully before changes are merged.
