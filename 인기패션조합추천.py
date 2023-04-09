import os
import pandas as pd

#설문조사 결과 데이터 불러오기
base_src = 'Data'
u_data_src = os.path.join(base_src,'fashion_survey.txt')
r_cols = ["카라티 청바지",	"카라티 슬랙스"	,"카라티 카고팬츠"	,"카라티 반바지",	"셔츠 청바지"	,"셔츠 슬랙스",	"셔츠 스웻팬츠",	"셔츠 카고팬츠",	"셔츠 반바지",	"반팔 청바지",	"반팔 슬랙스",	"반팔 스웻팬츠",	"반팔 카고팬츠",	"반팔 반바지",	"긴팔 청바지",	"긴팔 슬랙스",	"긴팔 스웻팬츠",	"긴팔 카고팬츠",	"긴팔 반바지"]
ratings = pd.read_csv(u_data_src,
                      sep = '\t',
                      names = r_cols,
                      encoding='latin-1'
                      )

print(ratings.head())

#transpose
ratings = ratings.transpose()

#rating sum of each combination
ratings =  ratings.sum(axis=1).to_frame()
ratings.index.name = "combination"
ratings = ratings.rename(columns={0:'rating'})

print(ratings.head())


# 인기 패션 조합 추천 방식
def recom_fashion(n_items):
    fashion_mean = ratings.groupby(['combination'])['rating'].mean()
    fasion_sort = fashion_mean.sort_values(ascending=False)[:n_items]
    recom_fashion = ratings.loc[fasion_sort.index]
    
    return recom_fashion
  
  
  
print(recom_fashion(3))