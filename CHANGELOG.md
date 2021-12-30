![logo](https://gitlab.com/azarte/azarte.gitlab.io/-/raw/master/public/assets/img/logo_64.png)

# azarte: telegram bot changelog

## 2021-12-30: v0.4 beta

Adding new text assets in english (translations still need to be reviewed). Fixing minor bugs. The **bot**
answer with *random replies* when somebody chat with it directly in groups now.    

The changes in the **bot** commands are:

- **/noise**: the command to access auditive alternatives. You can ask for random sounds and La Monte Young's styled
scores.  
- **/genuary**: the command to enter the artificially generated month of time where we build code that makes beautiful
things.  

## 2021-11-14: v0.3.1 beta

Fixing minor and stupid bugs. The bot is running correctly now. Handling text messages outside any command,
notifying the user when time is needed to build an answer.

## 2021-11-11: v0.3 beta

The **bot** has a clear structure now. Both **Image()** and **Sound()** classes were added to create
objects in the moment. The user can select between the different options in each category using an
*InlineKeyboard* now, so I decided to make some changes in the *bot commands*.

The changes in the **bot** commands are:

- **/poem** command was removed.
- **/attractor** command was removed.
- **/color**: the new command to access the different visual alternatives.
- **/text**: the new command to access the different textual alternatives.  

The **bot** has new features since this version:

- **abstract**: to ask for a random abstract from a text.
- **microtale**: simply sends a microtale from a database.
- **definition**: a *fictional definition* of a word.
- **lines**: a drawing created in the moment based on two random walks.
- **escape**: a drawing based on a series of lines which escape from the canvas.
- **clock**: a minimalistic drawing base on current time (UTC-3).
- **distribution**: a common histogram but with cool colors.
- **surprise**: the bot sends a random selected photo from its database.


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
