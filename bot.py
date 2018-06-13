# -*- coding: utf-8 -*-
import config
import telebot
import pyowm

owm = pyowm.OWM(config.WEATHER_TOKEN)  # Init WeatherApiObject
bot = telebot.TeleBot(config.BOT_TOKEN)  # Init TeleBotObject


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! You can send me a city name and I will give "
                                      "you current weather at this place. Nice? Let's start!")


@bot.message_handler(content_types=['text'])
def start(message):
    try:
        observation = owm.weather_at_place(message.text)
    except pyowm.exceptions.not_found_error.NotFoundError:
        bot.send_message(message.chat.id, "Oops, such location does not exists.")
        pass
    else:
        weather = observation.get_weather()
        temp = weather.get_temperature('celsius')
        pressure = weather.get_pressure()['press'] / config.GRAV_ACC / config.HG_DENSITY * 1e5
        humidity = weather.get_humidity()
        forecast = owm.three_hours_forecast(message.text).get_forecast()

        weather_text = 'It is {0}˚С in {1} now. The lowest temperature will be {2}˚С and the highest ' \
                       'will be {3}˚С.\n'.format('{:+d}'.format(temp['temp']), message.text, temp['temp_min'],
                                                 temp['temp_max']) + \
                       '\nThe atmospheric pressure is {0} mmHg.\n'.format('{:3.0f}'.format(pressure)) + \
                       '\nThe humidity is {0}%.\n'.format(humidity) + '\nWeather forecast:\n'

        i = 0
        for w in forecast:
            if (i < 9 and i > 0):
                weather_text += '{:2d}:00'.format(w.get_reference_time(timeformat='date').hour) + \
                                '{:5.0f}˚C\n'.format(w.get_temperature('celsius')['temp'])
            i += 1

        bot.send_message(message.chat.id, weather_text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
