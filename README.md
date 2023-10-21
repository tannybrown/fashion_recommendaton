# Fashion_recommendaton

### 프로젝트 설명
1. 날씨별 패션 추천 시스템 프로젝트 입니다.
2. 사용자의 패션 선호도를 분석하여 날씨별 어떤 의상을 추천해줄지 판단합니다.


### 프로젝트 진행 사항
## 1. 데이터 수집
1. 초기에 SNS 패션 인스타그래머에게 컨택하여 패션 데이터 협조를 요청하므로써 데이터 수집.
2. 수집된 사진 데이터에대한 정보(적정온도, 의상 등등)를 dataframe으로 저장.
## 2. 추천 알고리즘 설계
3. 저장된 dataframe을 기반으로 recommender를 설계.
4. 초기에는 filtering 방식으로 user의 선호 스타일의 데이터만 필터링 하는 방식을 취했음. -> 하지만 이 경우, 새로운 스타일에 대한 가능성이 사라지는 단점이 있음
5. 따라서 가능성을 배제시키는 filtering 방식보다는, 각각의 요소를 점수화해서 추천을 해주는 scoring function 방식으로 재구성.
   
## 3. 추천 알고리즘 api 화
1. 서버와의 통신을 위한 api를 구성.
2. fastapi를 이용 Why? 프로젝트 기간상 직관적이고 빠르게 구현이 가능했고, Pydantic 기반으로 비동기처리에 높은 성능.
3. 서버의 기상청 날씨 데이터 파싱후 파싱된 날씨를 이전에 구현한 추천 알고리즘에 넣어주는 방식으로 구현.
