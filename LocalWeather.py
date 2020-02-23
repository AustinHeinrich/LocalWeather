from datetime import datetime
import requests
import tkinter as tk
import geolocation

from util_scripts import SeasonDiviner as sd

with open('assets/API_KEY.txt') as f:
  weather_key = f.readline()

input_font = 'Arial'
output_font = 'Courier'

MIN_HEIGHT = 375
MIN_WIDTH = 480
MAX_HEIGHT = MIN_HEIGHT * 2
MAX_WIDTH = MIN_WIDTH * 2


def get_weather(city):
  url = 'https://api.openweathermap.org/data/2.5/weather'

  params = {'APPID': weather_key, 'q': city, 'units': 'Metric'}
  response = requests.get(url, params=params)
  print(response.json())

  format_weather(response.json())


def format_weather(weather):
  try:
    city = weather['name']
    country = weather['sys']['country']
    city_label['text'] = city + ', ' + country

    description_label['text'] = weather['weather'][0]['description']

    temperature = weather['main']['temp']
    temperature_with_windchill = weather['main']['feels_like']
    temperature_label['text'] = ' ' + str(temperature) + '°C' + '\n\n ' + str(temperature_with_windchill) + '°C'
    with_chill['text'] = ' with wind chill'

    humidity_label['text'] = str(weather['main']['humidity']) + '% \n Humidity '

    print(weather['main']['temp_min'])
    print(weather['main']['temp_max'])

  except:
    city_label['text'] = 'There was a problem retrieving information about your query.'


class Root(tk.Tk):
  def __init__(self, window_title):
    super().__init__()
    self.title(window_title)
    self.minsize(height=MIN_HEIGHT, width=MIN_WIDTH)
    self.maxsize(height=MIN_HEIGHT, width=MIN_WIDTH)

    canvas = tk.Canvas(self, height=MIN_HEIGHT, width=MIN_WIDTH)
    canvas.pack()


root = Root('Local Weather')

# setting up the background based on the season
season = sd.get_season(datetime.now())
if season == 'Summer':
  background_image = tk.PhotoImage(file='./assets/images/summer.png')
elif season == 'Fall':
  background_image = tk.PhotoImage(file='./assets/images/fall.png')
elif season == 'Winter':
  background_image = tk.PhotoImage(file='./assets/images/winter.png')
else:
  background_image = tk.PhotoImage(file='./assets/images/spring.png')

background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0)

# user input & frame setup
input_frame = tk.Frame(root, bg='black', bd=2.5)
output_frame = tk.Frame(root, bg='black', bd=2.5)
input_frame.place(relx=0.5, rely=0.05, relwidth=0.7, relheight=0.08, anchor='n')
output_frame.place(relx=0.5, rely=0.175, relwidth=0.9, relheight=0.775, anchor='n')

entry = tk.Entry(input_frame, bg='#ffffff', font=(input_font, 14))
entry.place(relwidth=0.625, relheight=1)
entry.bind('<Return>', lambda x: get_weather(entry.get()))

button = tk.Button(input_frame, text="Get Weather", font=(input_font, 12), command=lambda: get_weather(entry.get()))
button.place(relx=0.7, relwidth=0.3, relheight=1)

# weather display
city_label = tk.Label(output_frame, anchor='nw', font=(output_font, 18, 'bold'), justify='left')
city_label.place(relwidth=1, relheight=1)

description_label = tk.Label(output_frame, anchor='n', font=(output_font, 12))
description_label.place(relx=0.3, rely=0.1, relwidth=0.35, relheight=0.1)

temperature_label = tk.Label(output_frame, anchor='nw', font=(output_font, 16))
temperature_label.place(rely=0.2, relwidth=0.5, relheight=0.3)
with_chill = tk.Label(output_frame, anchor='nw', font=(output_font, 10))
with_chill.place(rely=0.45, relwidth=0.5, relheight=0.1)

humidity_label = tk.Label(output_frame, anchor='ne', font=(output_font, 16))
humidity_label.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.3)

get_weather('Saskatoon')

root.mainloop()
