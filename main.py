
import requests
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
import json 
import os
from datetime import datetime
import math
from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse




app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/weather/report",response_class=HTMLResponse)
async def root(request: Request,city_name:str="Noida"):
    # city_name="noida"
    user_api="fc802b05fccf507b6a3a1cbffdd0e3a4"
    complete_api_link="https://api.openweathermap.org/data/2.5/weather?q="+city_name+"&appid="+user_api
    api_link=requests.get(complete_api_link)
    api_data=api_link.json()

    if api_data['cod']=='404':
        print("Invalidcity: {}, please check your city name".format(city_name))
    else:
        dic={}
        temp_city=str(int((api_data['main']['temp'])-273.15))+" celsius"
        dic['current_temperature']=temp_city
        weather_desc=api_data['weather'][0]['description']
        dic['current_weather_desc']=weather_desc
        hmdt=str(api_data['main']['humidity'])+" %"
        dic['current_Humidity']=hmdt
        wind_spd=api_data['wind']['speed']
        print(wind_spd,type(wind_spd))
        dic['current_wind_speed']=str(wind_spd)
        date_time=datetime.now().strftime("%d %b %Y | %I:%M:%S:%p")
        dic['date_time']=date_time

        # json_object = json.dumps(dic, indent=4) 
        # print(type(dic))
        return templates.TemplateResponse("index.html", {"request": request, "data": dic})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)