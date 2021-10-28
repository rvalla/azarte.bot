![logo](https://gitlab.com/azarte/azarte.gitlab.io/-/raw/master/public/assets/img/logo_64.png)

# azarte: telegram bot changelog

## 2021-10-28: v0.2 alpha

Now there is a new **Messages()** class to control the text content of bot's messages. I added a field
in *security.json* to configure *logging* behavior (it can be *info*, *debugging* or *persistent*).  
The **bot** can speak English or Spanish now. The user can set the language with */language* command.
None user's data is saved so if the **bot** restarts it is necessary to set English again (Spanish is
the default language).  

The **bot** commands added or changed are:

- **/poem**: returns a random poem built specially for you in your selected language.  
- **/choice a b c**: returns a random word from your message.
- **/language**: to set the bot language, Spanish (default) or English.

## 2021-10-23: v0.1 alpha

First steps setting the bot. Testing *commandhandling* and different types of sent objects. The **bot** is in
*bot.py* file but use a set of classes. For now they are:

- **Text()**: it stores texts and methods to generate related messages.  
- **MyRandom()**: a class with custom *random functions*.  

The **bot** initial commands are:

- **/start**: returns simply a gretting.  
- **/attractor**: returns a random strange attractor. They are so beautiful.  
- **/poem**: returns a random poem built specially for you in spanish.  
- **/number (f)**: returns a random number rolling a dice with *f* faces.  
- **/sequence (f) (n)**: returns a random sequence of *n* numbers rolling a dice with *f* faces.  
- **/help**: returns a link to bring you here.  

Reach **azarte bot** [here](https://t.me/azarte_bot).
Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).
