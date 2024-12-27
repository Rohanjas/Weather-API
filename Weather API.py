import sys
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton,QLineEdit
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
  def __init__(self):
    super().__init__()

    self.setFixedSize(342,508)
    self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
    self.setWindowTitle("Weather Finder")

    self.ques_label = QLabel("Enter Your City",  self)
    self.input_label = QLineEdit(self)
    self.search_button = QPushButton("Get Weather",  self)
    self.temp_label = QLabel("Welcome", self)
    self.emoji_label = QLabel("😺",  self)
    self.des_label = QLabel("Let's Find", self)

    self.initUI()
    self.input_label.returnPressed.connect(self.get_weather)
    self.search_button.clicked.connect(self.get_weather)

  def initUI(self):
    
    vbox = QVBoxLayout()

    vbox.addWidget(self.ques_label)
    vbox.addWidget(self.input_label)
    vbox.addWidget(self.search_button)
    vbox.addWidget(self.temp_label)
    vbox.addWidget(self.emoji_label)
    vbox.addWidget(self.des_label)

    self.setLayout(vbox)
    
    self.ques_label.setAlignment(Qt.AlignCenter)
    self.input_label.setAlignment(Qt.AlignCenter)
    self.temp_label.setAlignment(Qt.AlignCenter)
    self.emoji_label.setAlignment(Qt.AlignCenter)
    self.des_label.setAlignment(Qt.AlignCenter)


    self.ques_label.setObjectName("ques_label")
    self.input_label.setObjectName("input_label")
    self.search_button.setObjectName("search_button")
    self.temp_label.setObjectName("temp_label")
    self.emoji_label.setObjectName("emoji_label")
    self.des_label.setObjectName("des_label")

    self.input_label.setGeometry(0,0,45,0)

    self.input_label.setPlaceholderText("City ??")
    self.emoji_label.setGeometry(0,0,100,0)

    self.setStyleSheet("""
        
          QLabel#ques_label{
                font-size: 38px;
                font-weight: bold;
                padding: 5px 5px 4px 4px;
          }
          QLineEdit#input_label{
                font-size: 30px;
                font-weight: bold;
                padding-left: 5px;
                padding-right: 5px;
                padding-bottom: 2px;

          }
          
          QPushButton#search_button{
                font-size: 26px;
                font-family: calibri;
                font-weight: bold;
                padding-left: 5px;
                padding-right: 5px;
                padding-bottom: 4px;
          }

          QPushButton#search_button:hover{
               border: solid;
               border-width: 1px;
               border-radius: 3px;
               border-color: hsl(0, 1.60%, 75.70%);
               background-color: hsl(0, 0.00%, 88.20%);
          }
          QLabel#temp_label{
                font-size: 60px;
                font-weight: bold;
                padding-top: 9px;
                padding-left: 4px;
                padding-right: 4px;
                padding-bottom: -2px;
          }
          QLabel#emoji_label{
                font-size: 100px;
                font-weight: bold;
                padding-left: 4px;
                padding-right: 4px;
                padding-bottom: -6px; 
          }
          QLabel#des_label{
                font-size: 36px;
                font-weight: bold;
                padding-top: 3px;
                padding-left: 4px;
                padding-right: 4px;
                padding-bottom: 3px; 
                
          }
    """)

  def get_weather(self):
      try:
        city = self.input_label.text().strip()
        api_key = "7a71962848d46096a96a5730a857a2c7"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["cod"] == 200:
            self.display_weather(data)

      except requests.exceptions.HTTPError as httper: 
            match response.status_code:
               case 400:
                  self.display_error("Bad Request\nPlease Check \nYour Input") 
               
               case 401:
                  self.display_error("UnAuthorized\nInvalid API Key")
              
               case 403:
                  self.display_error("Forbidden\nAccess is Denied")
               
               case 404:
                  self.display_error("Check your Input\nCity Not Found")

               case 500:
                  self.display_error("Internal Server Error\nPlease Try Again Later")

               case 502:
                  self.display_error("Bad Gateway\nInvalid Response \nfrom the server")

               case 503:
                  self.display_error("Service Unavailable\nUnder Maintenance")

               case 504:
                  self.display_error("Gateway Timeout\nNo Response \nfrom the Server")

               case _:
                  self.display_error(f"HTTP Error Occured\n{httper}")

      except requests.exceptions.ConnectionError:
          self.display_error("Connection Error\nCheck Your\nInternet Connection")

      except requests.exceptions.Timeout:
          self.display_error("Timeout Error\nRequest Timed Out")

      except requests.exceptions.TooManyRedirects:
          self.display_error("Too Many Redirects\nCheck the URL")

      except requests.exceptions.RequestException as reqer:
          self.display_error("Request Error\n{reqer}")

  
  def display_error(self,message):
      
      self.temp_label.setStyleSheet("font-size: 30px;"
                                    "font-weight: light;")

      
      self.temp_label.setText(message)

      self.emoji_label.setText("😓")
      self.des_label.setText("Sorry!!")
      

  def display_weather(self,data):

    kelvin = float(data["main"]["temp"])
    celsius = kelvin - 273.15
    farenheit = (kelvin - 273.15) * 9/5
    self.temp_label.setStyleSheet("font-size: 60px;"
                                    "font-weight: bold;")

    self.temp_label.setText((f"{str(celsius):.4}°C"))
    len_data = len(data["weather"][0]["description"])
    
    if len_data > 15:
      data1 = data["weather"][0]["description"].split(" ")
      data1.insert(2,"\n")
      data2 = " ".join(data1)
      self.des_label.setText(str(data2.title()))

    else:
      self.des_label.setText(str(data["weather"][0]["description"]).title())
   
    emoji_id = data["weather"][0]["id"]
    self.emoji_label.setText(self.get_weather_emoji(emoji_id))

  @staticmethod
  def get_weather_emoji(weather_id):
     
     if 200 <= weather_id <= 232:
      return "⛈️"
     elif 300 <= weather_id <= 321:
      return "🌦️"
     elif 500 <= weather_id <= 531:
      return "🌧️"
     elif 600 <= weather_id <= 622:
      return "❄️"
     elif 700 <= weather_id <= 741:
      return "🌫️"
     elif weather_id == 762:
      return "🌋"
     elif weather_id == 771:
      return "💨"
     elif weather_id == 781:
      return "🌪️"
     elif weather_id == 800:
      return "🌞"
     elif 801 <= weather_id <= 804:
      return "🌥️"
     else:
      return "😓"
    

     


def main():
  
  app = QApplication(sys.argv)
  weatherapp = WeatherApp()
  weatherapp.show()
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()