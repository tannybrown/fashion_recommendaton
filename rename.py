import os

insta_name = "not.bad_nb"

def rename_photos(folder_path):
    # 해당 폴더로 이동
    os.chdir(folder_path)

    # 폴더 내의 파일 리스트를 가져옴
    file_list = os.listdir()

    # 넘버링을 위한 변수 초기화
    count = 1


    # 파일마다 반복하며 이름 변경
    for filename in file_list:

        # 파일 확장자 추출
        extension = os.path.splitext(filename)[1]

        # 파일 이름 변경
        new_filename = f"{count}-{insta_name}{extension}"
        os.rename(filename, new_filename)

        # 넘버링 증가
        count += 1



if __name__ == "__main__":
    folder_path = os.getcwd() + '\\추천이미지\\{}'.format(insta_name)   # 여기에 폴더 경로를 입력하세요
    rename_photos(folder_path)