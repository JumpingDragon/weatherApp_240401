import sys
import requests
from bs4 import BeautifulSoup

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

form_class = uic.loadUiType("ui/appUi.ui")[0]
# ui 폴더 내의 디자인된 ui 불러오기

class WeatherApp(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨 검색 프로그램")
        self.setWindowIcon(QIcon("icon/weather_icon.png"))
        self.statusBar().showMessage("WEATHER SEARCH APP VER 0.6")
        self.search_btn.clicked.connect(self.weather_search)

    def weather_search(self):
        try:
            inptArea = self.area_inpt.text()  # 사용자가 입력한 지역명 텍스트 가져오기

            weatherHtml = requests.get(f"https://search.naver.com/search.naver?query={inptArea}날씨")

            weatherSoup = BeautifulSoup(weatherHtml.text, 'html.parser')

            # 날씨 지역 이름 가져오기
            areaText = weatherSoup.find("h2", {"class": "title"}).text  # (텍스트만 뽑는다.)
            areaText = areaText.strip()  # 양쪽 공백 제거
            self.area_ttl.setText(areaText)  # 사용자가 입력한 지역명 텍스트 넣어주기

            # 오늘의 온도
            today_tempText = weatherSoup.find("div", {"class": "temperature_text"}).text  # 현재 온도 불러오기
            today_tempText = today_tempText[6:12].strip()  # 6번째 글자부터 슬라이싱 후 양쪽 공백 제거
            self.now_tmp.setText(today_tempText)  # 사용자가 입력한 지역명 텍스트 넣어주기

            # 어제와의 온도 비교
            # yesterdayTempText = weatherSoup.find("span", {"class":"temperature down"}).text
            # yesterdayTempText = yesterdayTempText.strip()
            yesterdayTempText = weatherSoup.find("p", {"class": "summary"}).text
            yesterdayTempText = yesterdayTempText[:15].strip()
            self.yst_tmp.setText(yesterdayTempText)

            # 오늘 날씨 상태
            todayWeatherText = weatherSoup.find("span", {"class": "weather before_slash"}).text  # 오늘 날씨 텍스트
            todayWeatherText = todayWeatherText.strip()
            # todayWeatherImg = weatherSoup.find("i", {"class": "wt_icon"}).text  # 오늘 날씨 이미지
            # print(f"오늘 날씨 : {todayWeatherImg}")
            # self.weather_img.setText(todayWeatherText)
            self.setWeatherImage(todayWeatherText)  # 날씨 이미지 출력 함수 호출

            # 체감 온도
            tempFeelsText = weatherSoup.find("dd", {"class": "desc"}).text
            tempFeelsText = tempFeelsText.strip()
            self.sen_tmp.setText(tempFeelsText)

            # 미세먼지, 초미세먼지, 자외선, 일몰
            todayInfoText = weatherSoup.select("ul.today_chart_list>li", {"class": "txt"})
            # todayInfoText = todayInfoText.strip()
            finedust = todayInfoText[0].find("span", {"class": "txt"}).text
            self.fndst1.setText(finedust)
            superfinedust = todayInfoText[1].find("span", {"class": "txt"}).text
            self.fndst2.setText(superfinedust)
        except:
            QMessageBox.warning(self, "오류", "존재하는 지역명으로 입력하세요.")
            self.area_ttl.setText("입력된 지역명 오류!")
            self.now_tmp.setText("")
            self.yst_tmp.setText(f"{inptArea} 지역은 존재하지 않습니다.")
            self.setWeatherImage("")
            self.sen_tmp.setText("-")
            self.fndst1.setText("-")
            self.fndst2.setText("-")



    def setWeatherImage(self, weatherText):  # 날씨에 따른 이미지 출력
        if weatherText == "맑음":
            wImg = QPixmap("icon/sunny.png")   # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(wImg))
            # ui에 준비된 label 이름에 이미지 출력하기
        elif weatherText == "구름많음" or weatherText == "흐림":
            wImg = QPixmap("icon/cloudy.png")   # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(wImg))
            # ui에 준비된 label 이름에 이미지 출력하기
        elif weatherText == "눈":
            wImg = QPixmap("icon/snow.png")   # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(wImg))
            # ui에 준비된 label 이름에 이미지 출력하기
        elif weatherText == "비":
            wImg = QPixmap("icon/rain.png")   # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(wImg))
            # ui에 준비된 label 이름에 이미지 출력하기
        else:
            self.weather_img.setText(weatherText)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WeatherApp()
    win.show()
    sys.exit(app.exec_())

