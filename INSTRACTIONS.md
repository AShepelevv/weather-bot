#Procfile

```
bot: python3.6 bot.py
```

#config.pyc


#requirements.txt

```
pyowm==2.8.0
telebot==0.0.3
requests==2.7.0
pyTelegramBotAPI==3.2.0
```

#DEPLOYING
```
$ git commit -a -m "new commit"
$ git push heroku master
```

#SCALING
```
$ heroku ps:scale bot=1
```