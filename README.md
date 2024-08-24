# Holiday Fetcher

Holiday Fetcher is a Python project that retrieves and processes holiday data using the Calendarific API. This project uses FastAPI for building the API and Pydantic for data modeling and validation.

## Features

- Retrieve holidays by country and date.
- Filter holidays by date range.
- Save holiday data to JSON files.

## Installation

To set up and run the project, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/IlliaKadobanskij/HolidayFetcher.git
    cd holiday-fetcher
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the project root and add your API key and base URL:

    ```env
    CALENDARIFIC_API_KEY=your_calendarific_api_key
    BASE_URL=https://calendarific.com/api/v2/holidays
    ```

## Using Docker

To set up and run the project using Docker, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/IlliaKadobanskij/HolidayFetcher.git
    cd holiday-fetcher
    ```

2. **Start Docker and run following commands in root project folder**

    ```bash
    docker build -t your-image-name .
    docker run -d -p 8080:8080 --name your-container-name your-image-name
    ```


## Usage

### Credentials

Place your Calendarific api key in .env file

### Start the FastAPI server

It's started with Docker already or

Run the FastAPI development server using:

```bash
uvicorn app:app --reload
```

Got to http://localhost:8080/docs and make an API call with an example from OpenAPI spec

Check result from a response or json file from a data folder
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/IlliaKadobanskij/HolidayFetcher.git
git push -u origin main