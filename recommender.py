import os
import openpyxl
import pandas as pd
import calculate_temperature as ct
import sys
import shutil
import style_filter


# 체감온도
def human_feel_tmp(Ta,Rh,V,month) :

  #여름 체감온도
  if month >= 5 and month <= 9:
    if Rh >= 50 and Rh <= 55 :
      return Ta
    else :
      return ct.summer(Ta,Rh)
    
  #겨울철 체감온도  
  else :
    if V < 1.3 :
      return Ta
    else :
      return ct.winter(Ta,V)


# 추천 알고리즘 - 5개 추천
def algorithm(tmp, rain, usercold,userhot,preferences, df) :
  # 추위 민감도에 따른 추천 유형(1에가까우면 추위를 잘견딤!)
  considerCold = {
        1: (2,3,0),
        2: (2,2,1),
        3: (3,1,1),
        4: (2,1,2),
        5: (2,0,3)
    }
  # 1에 가까울 수록 더위를 잘 견딤
  considerWarm = {
        1: (2,0,3),
        2: (2,1,2),
        3: (3,1,1),
        4: (2,2,1),
        5: (2,3,0)
  }
  
  # 리턴할 배열
  answer = []
  
  # 추위/더위 민감도
  category =()
  
  # 해당 유저의 정보


  # 비가 올 경우, 강우량 2.5mm 이하는 -1 , 그 이상은 -2 (얕은비와 일반 비의 차이)
  if rain == 0 :
    pass
  elif rain < 2.5 :
    tmp -= 0.5
  else :
    tmp -= 1

  # 추위민감도를 이용한 추천 분류(18~25는 민감도 고려 x)
  # 더위 민감도
  if tmp >= 25 :
    category = considerWarm[userhot]
  elif tmp <= 18 :
    category = considerCold[usercold]
  else :
    category = (5,0,0)
  print(tmp)
  
  redundant = set()
  answer,redundant = style_filter.recommend_style(tmp,preferences,df,category[0],answer,redundant)
  answer,redundant = style_filter.recommend_style(tmp + 1,preferences,df,category[1],answer,redundant)
  answer,redundant = style_filter.recommend_style(tmp - 1,preferences,df,category[2],answer,redundant)
  
  return answer






# # user data 읽기
# user_df = pd.read_excel(os.getcwd() +'\\Data\\user.xlsx', engine= 'openpyxl')
# user_df = user_df.drop(columns= 'Unnamed: 0')
#


# # 기상청 정보. 기온, 습도 , 풍속 , 강수량 받기
# user_id = int(sys.argv[1]) # 유저 id
# ta = float(sys.argv[2]) # 기온
# rh = float(sys.argv[3]) # 습도
# v = float(sys.argv[4]) # 풍속
# rain = float(sys.argv[5]) # 강수량
# month = int(sys.argv[6]) # 해당 달


#
# # fashion data 읽기 (성별에 따라서, 여자는 1 , 남자는 2)
# user_row = user_df.loc[user_df['user_id'] == user_id]
# sex = user_row['sex']
# if list(sex)[0] == 1 :
#   df = pd.read_excel(os.getcwd() +'\\Data\\dataframe1.xlsx', engine= 'openpyxl')
# else :
#   df = pd.read_excel(os.getcwd() +'\\Data\\dataframe2.xlsx', engine= 'openpyxl')
#
# df = df.drop(columns= 'Unnamed: 0')
# df['category'] = df['category'].astype(str)
# # df = pd.read_excel('C:\\Users\\w2980\\Desktop\\graduation\\Data\\dataframe1.xlsx', engine= 'openpyxl')
#
#
# tmp = human_feel_tmp(ta,rh,v,month)
# answer = algorithm(tmp,rain,user_id,user_df,df)
#
# # 사진이 담긴 폴더 경로
# source_folder = os.getcwd() + '\\추천이미지\\'
#
# # 사진을 저장할 새로운 폴더 경로
# destination_folder = os.getcwd() + '\\result\\' + str(user_id)
#
# # 목적지 폴더가 존재하면 비우기
# if os.path.exists(destination_folder):
#     shutil.rmtree(destination_folder)
#
# # 새로운 폴더 생성
# os.makedirs(destination_folder)
#
# # 배열에 있는 파일 이름에 해당하는 사진 파일들 result 폴더에 저장
# for file_name in answer:
#     insta_id = file_name.rsplit('.',1)[0].split("-")[1]
#     source_file_path = os.path.join(source_folder + insta_id, file_name)
#     destination_file_path = os.path.join(destination_folder, file_name)
#     shutil.copy(source_file_path, destination_file_path)