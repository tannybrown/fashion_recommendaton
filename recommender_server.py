from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import os
from typing import Optional
import recommender
# 연결하기. 넣기.

app = FastAPI()

class WeatherUltraShort(BaseModel):
    fcstDate: int
    fcstTime: int
    temp: int
    rainAmount: int
    windSpeed: int
    humid: int
    sky: int


class WeatherShort(BaseModel):
    fcstDate: int
    fcstTime: int
    temp: int
    rainAmount: int
    windSpeed: int
    humid: int
    sky: int
    rainPercentage: int

class WeatherMid(BaseModel):
    fcstDate: int
    rainPercentageAm: int
    rainPercentagePm: int
    skyAm: int
    skyPm: int
    tempLowest: int
    tempHighest: int
class WeatherAP(BaseModel) :
    fcstDate: int
    pm10Value : int
    pm25Value : int

class WeatherInfo(BaseModel):
    weatherUltraShort: List[WeatherUltraShort]
    weatherShort: List[WeatherShort]
    weatherMid: List[WeatherMid]
    weatherAP: List[WeatherAP]

class MemberInfo(BaseModel) :
    memberIdx : int
    memberSex : str
    memberCold : str
    memberHot : str
    memberPreferences : str

class ResponseData(BaseModel):
    memberInfo: MemberInfo
    weatherInfo: WeatherInfo
#    version: float
#    message: str


# uvicorn main:app --reload
@app.post("/recommend")
def recommend(responseData: ResponseData):
    # 추천 id list
    return_arr = []

    # data 쪼개기

    # 추천할 날짜(recomDate), 0은 오늘 1은 내일
    tomorrow = 0
    targetWeather = []
    weatherInfo = responseData.weatherInfo
    weatherUltraShort = weatherInfo.weatherUltraShort
    weatherShort = weatherInfo.weatherShort

    curMonth = weatherUltraShort[0].fcstDate // 100
    curTime = weatherUltraShort[0].fcstTime
    targetDate = weatherUltraShort[0].fcstDate
    # 7시 이후면 내일 날씨를 추천 해주는 것
    if curTime >= 2200:
        tomorrow = 1
        targetDate = weatherShort[0].fcstDate

    #내일 날씨 추천
    if tomorrow :
        # 다음날 예보 수집하기
        # 초단기 부터 수집하기
        index = 0
        for i in range(1,len(weatherUltraShort)):
            if weatherUltraShort[i].fcstTime == 0 :
                index = i
                break
        if index == 0 :
            targetWeather = weatherUltraShort[index:].copy()

        # 여기부터 단기 예보에서 뽑아내기
        # targetWeather에 날씨 정보 입력하기
        for i in range(len(weatherShort)):
            # targetWeather가 비었으면
            if targetWeather == [] :
                targetWeather.append(weatherShort[i])
            # 비어있지 않다면, 겹치지 않게 fcstTime이 더 크면 넣기
            else :
                if targetWeather[-1].fcstTime < weatherShort[i].fcstTime:
                    targetWeather.append(weatherShort[i])
                else :
                    # 다음날로 넘어갔는지 확인하기, 넘어갔으면 break
                    if targetDate != weatherShort[i].fcstDate:
                        break





    # 오늘 날씨 추천
    else :
        # 현재부터 오늘의 마지막 날씨 까지 받기
        index = 0
        for i in range(1,len(weatherUltraShort)):
            if weatherUltraShort[i].fcstTime == 0:
                index = i
                break

        if index == 0 :
            # index가 0이면 찾지 못한 것이므로, 그냥 전부 넣으면 됌
            targetWeather = weatherUltraShort.copy()
        else :
            targetWeather = weatherUltraShort[:index]

        #단기 예보에서 정보얻기
        for i in range(len(weatherShort)):
            if targetWeather[-1].fcstTime < weatherShort[i].fcstTime:
                targetWeather.append(weatherShort[i])
            else :
                # 둘이 같으면 겹쳐진거고, 다르면 다른날인것. 즉 날짜가 넘어간거임
                if targetDate != weatherShort[i].fcstDate:
                    break




        # targetWeather를 파싱해서 날씨, 습도, 등등 파악하기
        # 알고리즘에 집어넣기.

    tmp = []
    humid = []
    rain = []
    wind = []

    # 시간에 따라서 분류, 밤 ~ 아침(22~10), 점심(10~17), 그리고 저녁(17~22) 으로 3개의 분류.
    # 밤 - 아침 (9시부터 14시까지의 기온을 고려.)
    if curTime >= 2200 or curTime < 1000 :
        for weather in targetWeather :
            # 9시 이전은 고려 안함
            if weather.fcstTime < 900 :
                continue
            else :
                if weather.fcstTime > 1500 :
                    break
                else :
                    tmp.append(weather.temp * 0.1)
                    humid.append(weather.humid)
                    rain.append(weather.rainAmount)
                    wind.append(weather.windSpeed)

    # 점심(18시까지를 고려. why? 낮시간대 입는 옷이라 생각, 일교차가 크기에 너무 늦은 시간까지 고려하면 더울것으로 예상)
    elif curTime >= 1000 and curTime < 1700 :
        # 18시까지 보기
        for weather in targetWeather :
            if weather.fcstTime > 1800 :
                break
            else :
                tmp.append(weather.temp * 0.1)
                humid.append(weather.humid)
                rain.append(weather.rainAmount)
                wind.append(weather.windSpeed)

    # 저녁날씨 옷 추천임. 나머지 모두 고려.
    else :
        for weather in targetWeather :
            tmp.append(weather.temp * 0.1)
            humid.append(weather.humid)
            rain.append(weather.rainAmount)
            wind.append(weather.windSpeed)

    # 일단 1안으로 평균 내서 그냥 그값으로 가기.

    avg = [sum(tmp)/len(tmp),sum(humid)/len(humid),sum(rain)/len(rain),sum(wind)/len(wind) * 0.1, curMonth]

    print(2)
    tmp = recommender.human_feel_tmp(avg[0], avg[1], avg[3], avg[4])


    # user info data parsing
    userinfo = responseData.memberInfo
    usersex = sexToInt[userinfo.memberSex]
    
    # 덥고 추움
    usercold = strToInt[userinfo.memberCold]
    userhot = strToInt[userinfo.memberHot]
    # 선호스타일
    userpreferences = userinfo.memberPreferences
    # 문자열 to int
    arr = []
    for preference in userpreferences.split() :
        arr.append(styleToInt[usersex][preference])
    preferences = ','.join(arr)
    
    if usersex == 1 :
        df = male_df
    else :
        df = female_df
        
    answer = recommender.algorithm(tmp, avg[2], usercold,userhot,preferences, df)

    

    return {'fashionStr': answer}

# user_id = 1

# user_df = pd.read_excel(os.getcwd() +'\\Data\\user.xlsx', engine= 'openpyxl')
# user_df = user_df.drop(columns= 'Unnamed: 0')

# user_row = user_df.loc[user_df['user_id'] == user_id]
# sex = user_row['sex']
strToInt = {"매우 그렇지 않다" : 1,'그렇지 않다': 2 ,'보통이다' : 3,'그렇다' : 4,'매우 그렇다' : 5}
styleToInt = [0,{'캐주얼' : '1','스트릿':'2','미니멀':'3','클래식/오피스룩':'4'},{'캐주얼':'1','큐티/러블리':'2','클래식/오피스룩':'3','모던시크':'4','미니멀':'5','키치':'6','스트릿':'7'}]
sexToInt = {'남성':1,'여성':2}
male_df = pd.read_excel(os.getcwd() +'/Data/dataframe2.xlsx', engine= 'openpyxl')
male_df = male_df.drop(columns= 'Unnamed: 0')
male_df['category'] = male_df['category'].astype(str)

female_df = pd.read_excel(os.getcwd() +'/Data/dataframe1.xlsx', engine= 'openpyxl')
female_df = female_df.drop(columns= 'Unnamed: 0')
female_df['category'] = female_df['category'].astype(str)

# if list(sex)[0] == 1 :
#   df = female_df
# else :
#   df = male_df

# 여러번 도는지 확인용
print(1)
