import requests     # pip install requests

from bs4 import BeautifulSoup   # pip install beautifulsoup4

inputArea = input("날씨를 조회하려는 지역을 입력하시오: ")
weatherHtml = requests.get(f"https://search.naver.com/search.naver?query={inputArea}날씨")
# 네이버에서 '제주도날씨'로 검색한 결과의 html 파일 가져오기
print(weatherHtml.text)

weatherSoup = BeautifulSoup(weatherHtml.text, 'html.parser')
# print(weatherSoup)

# 날씨 지역 이름 가져오기
areaText = weatherSoup.find("h2", {"class": "title"}).text #(텍스트만 뽑는다.)
areaText = areaText.strip()     # 양쪽 공백 제거
print(f"지역이름 : {areaText}")

# 오늘의 온도
today_tempText = weatherSoup.find("div", {"class": "temperature_text"}).text  # 현재 온도 불러오기
today_tempText = today_tempText[6:12].strip()      # 6번째 글자부터 슬라이싱 후 양쪽 공백 제거
print(f"현재온도 : {today_tempText}")

# 어제와의 온도 비교
# yesterdayTempText = weatherSoup.find("span", {"class":"temperature down"}).text
# yesterdayTempText = yesterdayTempText.strip()
yesterdayTempText = weatherSoup.find("p", {"class":"summary"}).text
yesterdayTempText = yesterdayTempText[:15].strip()
print(f"어제와 날씨 비교 : {yesterdayTempText}")

# 오늘 날씨 상태
todayWeatherText = weatherSoup.find("span", {"class": "weather before_slash"}).text     # 오늘 날씨 텍스트
todayWeatherText = todayWeatherText.strip()
print(f"오늘 날씨 : {todayWeatherText}")

# 체감 온도
tempFeelsText = weatherSoup.find("dd", {"class": "desc"}).text
tempFeelsText = tempFeelsText.strip()
print(f"체감 온도 : {tempFeelsText}")

# 미세먼지, 초미세먼지, 자외선, 일몰
todayInfoText = weatherSoup.select("ul.today_chart_list>li", {"class":"txt"})
# todayInfoText = todayInfoText.strip()
finedust = todayInfoText[0].find("span", {"class":"txt"}).text
print("미세먼지 : "+finedust)
superfinedust = todayInfoText[1].find("span", {"class":"txt"}).text
print("초미세먼지 : "+superfinedust)
UVray = todayInfoText[2].find("span", {"class":"txt"}).text
print("자외선 : "+UVray)
sunSet = todayInfoText[3].find("span", {"class":"txt"}).text
print("일몰 시각 : "+sunSet)

