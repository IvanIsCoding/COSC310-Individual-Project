# Elon Musk Bot ![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54) ![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=logo=telegram&logoColor=white) ![Flask](https://img.shields.io/badge/flask-%23000.svg?logo=flask&logoColor=white)

<p align="center"> 
<img width="620" height="414" src="static/img/ElonMusk.png">
</p>

Elon Musk Bot is a chatbot inspired by the entrepreneur and billionaire Elon Musk. It can answer questions about Tesla, SpaceX, cryptocurrencies - give it a try!

## Setting Up

To launch the Elon Musk bot, first [install Python](https://realpython.com/installing-python/) on your machine. Once Python is installed, launch your terminal on the folder containing the repository and run:

```
pip install -r requirements.txt
```

Then, start Docker and run:
```
docker pull mongo
docker run mongo
```

## Creating your own Telegram bot based on this code

To create your own Telegram bot, first go to https://t.me/botfather. Send the following message to Botfather:

```
/newbot
```

Botfather will ask you for the name and the username for your bot. After you pick the two, you will receive a message along this lines:

```
Done! Congratulations on your new bot. You will find it at t.me/LINK_TO_YOUR_BOT. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
HERE_IS_YOUR_LONG_SECRET_TOKEN
Keep your token secure and store it safely, it can be used by anyone to control your bot.
```

Then, copy the secret token to a file named `env.yaml` at the root of this repository as follows:

```yaml
TOKEN: "HERE_IS_YOUR_LONG_SECRET_TOKEN"
```

Obviously, replace "HERE_IS_YOUR_LONG_SECRET_TOKEN" with the real token you got from Botfather. Once that is done and you saved `env.yaml`, make sure you have installed Python and the requirements:

```
pip install -r requirements.txt
```

Then, run the Telegram bot:

```
python src/app.py
```

Lastly, go to t.me/LINK_TO_YOUR_BOT (the link you obtained from Botfather) and chat with the bot! 

## Code Structure

```
    .
    ├── app.py                    # Code for the Python back-end - it handles requests to the bot
    ├── elon_musk_bot.py          # Code for the Telegram bot - it handles Telegram requests
    ├── data.json                 # Answers to the predefined topics Elon Musk bot can answer
    ├── template                  # Contains the front-end logic for the user interace
    └── README.md                 # This file!
```

## Built With

* [Python](https://www.python.org/) - Back End

## Authors

- [Kiet Phan](https://github.com/ketphan02)
- [Ivan Carvalho](https://github.com/IvanIsCoding)
- [Lydia Lin](https://github.com/yuqi88)
- [Akshat Singal](https://github.com/aksingal-dev)
- [Paula Wong-Chung](https://github.com/KafkaNoNeko)

