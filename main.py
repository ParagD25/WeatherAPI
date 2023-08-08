from fastapi import FastAPI
from weather.routers import weather
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(weather.weatherRouter)


@app.get("/", tags=["Welcome"])
def home():
    return {"Message": "Welcome To Weather API"}
