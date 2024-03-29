# -*- coding: utf-8 -*-
import config
import telebot
import pyowm
import logging
import emoji


def get_emoji(weather):
    emoji.emojize(config.WEATHER_EMOJI[weather.get_status()], use_aliases=True)


owm = pyowm.OWM(config.WEATHER_TOKEN)  # Init WeatherApiObject
bot = telebot.TeleBot(config.BOT_TOKEN)  # Init TeleBotObject
logger = logging.getLogger(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! You can send me a city name and I will give "
                                      "you current weather at this place. Nice? Let's start!")


@bot.message_handler(content_types=['text'])
def start(message):
    logger.info('User has tried to know the weather in' + message.text)
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

        weather_text = 'It is *{0}˚С* and {4} in *{1}* now. The lowest temperature today will be {2}˚С, ' \
                       'the highest: {3}˚С.\n'.format('{:+.0f}'.format(temp['temp']),
                                                      message.text,
                                                      '{:+.0f}'.format(temp['temp_min']),
                                                      '{:+.0f}'.format(temp['temp_max']),
                                                      emoji.emojize(config.WEATHER_EMOJI[weather.get_status()]),
                                                                    use_aliases=True) + \
                       '\nThe atmospheric pressure is {0} mmHg.\n'.format('{:3.0f}'.format(pressure)) + \
                       '\nThe humidity is {0}%.\n'.format(humidity) + '\nWeather forecast:\n'

        i = 0
        weather_text += '```\n'

        for w in forecast:
            i += 1
            if (i < 9):
                weather_text += '{:02d}:00'.format(w.get_reference_time(timeformat='date').hour) + '\t' + \
                                '{:+5.0f}˚C'.format(w.get_temperature('celsius')['temp']) + '\t\t' + \
                                emoji.emojize(config.WEATHER_EMOJI[w.get_status()], use_aliases=True) + '\n'

        weather_text += '```'

        bot.send_message(message.chat.id, weather_text, parse_mode="Markdown")


if __name__ == '__main__':
    bot.polling(none_stop=True)
