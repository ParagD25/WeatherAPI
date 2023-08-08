from weather.models import Weather
import requests
from fastapi import APIRouter, Response, status, HTTPException
import os
from dotenv import load_dotenv


load_dotenv()

url = "https://weatherapi-com.p.rapidapi.com/current.json"

headers = {
    "X-RapidAPI-Key": os.getenv("API_KEY"),
    "X-RapidAPI-Host": os.getenv("API_HOST"),
}

weatherRouter = APIRouter(prefix="/weather", tags=["Weather"])


@weatherRouter.post("/getCurrentWeather", status_code=status.HTTP_201_CREATED)
def getCurrentWeather(weather: Weather):
    get_weather = weather.model_dump()

    try:
        querystring = {"q": f"{get_weather['city']}"}

        response = requests.get(url, headers=headers, params=querystring)

        json_response = {
            "Weather": str(response.json()["current"]["temp_c"]) + " C",
            "Longitude": str(response.json()["location"]["lon"]),
            "Latitude": str(response.json()["location"]["lat"]),
            "City": response.json()["location"]["name"]
            + " "
            + response.json()["location"]["country"],
        }

    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid City Name"
        )

    if get_weather["output_format"].lower() == "xml":
        xml_content = f"""
        <?xml version="1.0" encoding="UTF-8" ?>
        <root>
            <Temperature>{response.json()["current"]["temp_c"]}</Temperature>
            <City>{response.json()["location"]["name"]}</City>
            <Latitude>{response.json()["location"]["lat"]}</Latitude>
            <Longitude>{response.json()["location"]["lon"]}</Longitude>
        </root>
        """
        return Response(content=xml_content, media_type="application/xml")
    elif get_weather["output_format"].lower() == "json":
        return json_response
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Output Format"
        )
