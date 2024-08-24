from fastapi import FastAPI
from holiday_fetcher.routes import router as HolidayFetcherRouter


app = FastAPI()

app.include_router(HolidayFetcherRouter, tags=['Holiday Fetcher'])
