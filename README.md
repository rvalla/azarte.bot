![logo](https://gitlab.com/azarte/azarte.gitlab.io/-/raw/master/public/assets/img/logo_64.png)

# azarte: telegram bot

This is the code for a telegram bot. The idea is to play with randomness artistically but directly in a chat.
It is part of **azarte** project obviously.  

## online status

**Azarte Bot** is not currently deployed. It will be available during some moments of the week while I run
some tests. Stay tuned!

## commands

Here you can see the list of available commands. Some of them allow you to pass parameters.

- **/start**: returns simply a gretting.  
- **/attractor**: returns a random strange attractor. They are so beautiful.  
- **/poem**: returns a random poem built specially for you.  
- **/number (f)**: returns a random number rolling a dice with *f* faces.  
- **/sequence (f) (n)**: returns a random sequence of *n* numbers rolling a dice with *f* faces.  
- **/choice a b c**: returns a random word from your message.
- **/language**: to set the bot language, Spanish (default) or English.
- **/help**: returns a link to bring you here.  

## running the code

Note that you will need a *security.json* file on root which includes the bot's token to run this software.
I suggest the following fieldsvalthough currently only *token* (provided by [@BotFather](https://t.me/BotFather)
and *logging* (info, debugging or persistent) are mandatory:

```
{
	"bot_name": "Azarte Bot",
	"date": "2021-10-23",
	"username": "azarte_bot",
	"link": "https://t.me/azarte_bot",
	"token": "I won't tell you my token",
	"logging": "info"
}

```

## standing upon the shoulders of giants

This little project is possible thanks to a lot of work done by others in the *open-source* community. Particularly in
this case I need to mention:

- [**Python**](https://www.python.org/): the programming language I used.  
- [**python-telegram-bot**](https://python-telegram-bot.org/): the library I used to contact the *Telegram API*.  

Reach **azarte bot** [here](https://t.me/azarte_bot).
Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).
