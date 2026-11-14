# API Data Fetcher

A small Python command-line application that fetches user data from a public REST API, validates selected fields, and displays the results.

The project was created to practice working with REST APIs, error handling, input validation, and automated testing in Python.

## Features

- Fetches user data from the JSONPlaceholder REST API.
- Uses a predefined API endpoint and a 5-second request timeout.
- Handles HTTP errors, request failures, and invalid JSON responses.
- Validates user names and email addresses.
- Checks the structure of the API response and individual user records.
- Displays user names and email addresses in the terminal.
- Includes automated tests using pytest and mocked HTTP requests.

## Technologies

- Python
- Requests
- pytest
- unittest.mock

## Installation

Clone the repository and navigate to the project directory.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Usage

Run the application:

```powershell
python main.py
```

The application fetches user data from:

https://jsonplaceholder.typicode.com/users

It validates the name and email fields and displays the results in the terminal.

## Running Tests

Run all automated tests:

```powershell
python -m pytest -v
```

The tests cover input validation, user data processing, successful API requests, HTTP errors, timeouts, and invalid JSON responses.

HTTP requests are mocked in unit tests so they can run without a network connection.

## Limitations

- The application uses a single predefined API endpoint.
- Email validation performs basic format checks and does not fully implement email address standards.
- Results are displayed in the terminal and are not saved to a file.

## Future Improvements

Possible future improvements include saving results to a file, adding logging, and extending data validation.
