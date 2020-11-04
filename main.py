import telebot
import time
from collections import defaultdict
import requests
from threading import Timer
# from flask import Flask, request
# import os

# server = Flask(__name__)

# Token reading
import configparser
config = configparser.ConfigParser()
config.read(r'config.cfg')
token = config.get('creds', 'token')
secret = config.get('creds', 'secret')

bot = telebot.TeleBot(token=token)

# Available commands
commands = {
    'start': 'Start command',
    'help': 'To see available commands',
    'all': 'To get stopstalk scoreboard of institute top 75',
    'stalk': 'Stalk individual stopstalk user',
    'notify': 'register handle for cf rating changes'
}

# database
cllgurl = defaultdict(str)
cllgurl[
    946607441] = 'https://www.stopstalk.com/leaderboard.json?q=National+Institute+of+Technology%2C+Durgapur'
handles = defaultdict(str)
handles[
    946607441] = 'https://codeforces.com/api/user.rating?handle=sainad&secret=' + secret
ratings = defaultdict(int)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    college = bot.send_message(
        message.chat.id,
        "Welcome type /help to see available commands\nEnter your college name(as in stopstalk)"
    )
    bot.register_next_step_handler(college, process_cllg)


def process_cllg(college):
    clg = college.text.split()
    text = '+'.join(clg)
    text = text.replace(",", "%2C")
    cllgurl[college.chat.
            id] = "https://www.stopstalk.com/leaderboard.json?q=" + text
    bot.send_message(college.chat.id, "Recived Thanks")
    # bot.send_message(college.chat.id,
    #                  "Recived {} Thanks".format(cllgurl[college.chat.id]))


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "\n".join(f'/{k}: {v}' for k, v in commands.items()))


@bot.message_handler(commands=['all'])
def scrape_all(message):
    url = cllgurl[message.chat.id]
    res = requests.get(url).json()
    coders = res['users']
    msg = ''
    for idx, coder in enumerate(coders):
        msg += '{} {} {} {}\n'.format(idx + 1, coder[0], coder[1], coder[3])
        if idx == 74:
            break
    if msg:
        bot.send_message(message.chat.id, msg)
    else:
        bot.send_message(
            message.chat.id,
            "Institute not found Enter /start to enter institute name again")


@bot.message_handler(commands=['stalk'])
def stalk_user(message):
    stopstalk_user = bot.send_message(message.chat.id,
                                      "Enter stopstalk handle for stalking: ")
    bot.register_next_step_handler(stopstalk_user, stalk_user_helper)


def stalk_user_helper(message):
    user = message.text
    try:
        url = 'https://www.stopstalk.com/user/profile.json/' + user
        stalk_details = requests.get(url).json()
    except Exception:
        bot.send_message(message.chat.id, "User not found")
        return
    institute = stalk_details['row']['institute']
    institute = institute.replace(" ", "+")
    institute = institute.replace(",", "%2C")
    institute_url = 'https://www.stopstalk.com/leaderboard.json?q=' + institute
    try:
        institute_leaderboard = requests.get(institute_url).json()['users']
    except Exception:
        bot.send_message(message.chat.id, "Institute not found")
        return
    for idx, coder in enumerate(institute_leaderboard):
        if coder[1] == user:
            rank = idx + 1
            break
    msg = 'Full Name: {}\nStopStalk Rating: {}\nInstitute: {}\nInstitute rank: {}'.format(
        stalk_details['name'], stalk_details['row']['stopstalk_rating'],
        stalk_details['row']['institute'], rank)
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['notify'])
def get_handle(message):
    cf_handle = bot.send_message(message.chat.id, "Enter cf handle: ")
    bot.register_next_step_handler(cf_handle, get_handle_helper)


def get_handle_helper(message):
    handle = message.text
    url = 'https://codeforces.com/api/user.rating?handle=' + handle + '&secret=' + secret
    res = requests.get(url).json()
    if res['status'] != 'OK':
        bot.send_message(message.chat.id, res['comment'])
        return
    handles[message.chat.id] = url
    contests = res['result']
    ratings[message.chat.id] = len(contests)
    # bot.send_message(message.chat.id, url)
    bot.send_message(
        message.chat.id,
        "Received Thanks! You will be notified of rating changes")


## FIX: https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds
def ratingChangeHelper():
    for hand in handles:
        url = handles[hand]
        res = requests.get(url).json()
        contests = res['result']
        if len(contests) > ratings[hand] and ratings[hand] != 0:
            newRating = contests[-1]['newRating']
            oldRating = contests[-1]['oldRating']
            contest = contests[-1]['contestName']
            bot.send_message(
                hand,
                'Your rating changed by {} from {} to {} in {} contest'.format(
                    newRating - oldRating, oldRating, newRating, contest))
            ratings[hand] = len(contests)
    t = Timer(60, ratingChangeHelper)
    t.daemon = True
    t.start()


ratingChangeHelper()

bot.polling()

# @server.route('/' + token, methods=['POST'])
# def getMessage():
#     bot.process_new_updates(
#         [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return "!", 200

# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url='https://saiscrapperbot.herokuapp.com/' + token)
#     return "!", 200

# if __name__ == "__main__":
#     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))