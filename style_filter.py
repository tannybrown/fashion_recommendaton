import math

def min_max_regularization(df,col_name) :
    df_min = df[col_name].min()
    df_max = df[col_name].max()
    for index,row in df.iterrows() :
        df.loc[index,'reg_'+ col_name] = (row[col_name] - df_min) / (df_max - df_min)
    return df
    
def tmp_regularization(df,col_name) :
    df_max = df[col_name].max()
    for index, row in df.iterrows() :
        df.loc[index, 'reg_' + col_name] = (row[col_name] / df_max)
    return df


# 유저가 선호하는 스타일의 데이터 필터링 -> 필터링은 위험하니 scoring방식으로 변경
def filter_user_style(tmp,user_id, df, user_df,count,answer):
    if count == 0 :
        return answer
    
    # 특정 user_id에 해당하는 유저 스타일 정보 가져오기 -> 스코어 점수를 주기!
    user_style = user_df[user_df['user_id'] == user_id]['style'].iloc[0]
    user_style = set(user_style.split(","))

    # -> 데이터별 스코어 주기, 체감온도와 적정온도 빼기, 정규화 함수 만들기,
    for index, row in df.iterrows() :
        # 취향별 스코어
        item_category = set(row['category'].split(","))
        item_category &= user_style
        df.loc[index,'style_score'] = len(item_category)
        #온도 스코어
        df.loc[index,'tmp_score'] = abs(row['적정온도'] - tmp)
    
    df = min_max_regularization(df,'style_score')
    df = tmp_regularization(df,'tmp_score')
    
    # 정규화 점수 column 추출
    col_list = []
    for col in df.columns :
        if 'reg_' in col :
            col_list.append(col)
    
    # 점수 합산
    for index, row in df.iterrows() :
        total = 0
        for col in col_list :
            total += row[col]
        df.loc[index,'total_score'] = total
    
    sorted_df = df.sort_values(by=['total_score', 'tmp_score'],ascending = [True,True])

    # count만큼 answer에 담기
    for _, row in sorted_df.iterrows():
        
        # break조건
        if count == 0 :
            break

        # 파일명 만들기
        name = toName(row)
        
        if name in answer :
            pass
        else :
            answer.append(name)
            count -= 1  

    return answer    


# def tmpMinus(df, tmp,pre) :
#     df['diff'] = abs(df['적정온도'] - tmp)
    
#     # 겹치는 스타일 수 체크
#     df['겹치는_스타일_수'] = df['category'].apply(lambda x: len(set(x) & pre))

#     # 'diff' 열의 값에 따라 먼저 정렬하고, '겹치는_스타일_수' 열의 값에 따라 정렬
#     sorted_df = df.sort_values(by=['diff', '겹치는_스타일_수'], ascending=[True, False]).drop(columns='겹치는_스타일_수')

#     return sorted_df


def toName(row) :
    name = str(row['p_id']) + "-" + row['insta_id'] + '.jpg'
    return name


# 예시 테스트
# user_id_to_filter = 1
# result_df = filter_user_style(user_id_to_filter, df, user_df,2,[])