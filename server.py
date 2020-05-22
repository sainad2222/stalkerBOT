from newBot import tBot
import stopstalk

update_id = None

bot=tBot(r"config.cfg")
def make_reply(msg):
    reply=None
    if msg is not None:
        reply = stopstalk.text(msg)
        print(reply)
    return reply

while True:
    print("...")
    updates = bot.get_updates(offset=update_id)['result']
    if updates:
        for item in updates:
            update_id = item['update_id']
            try:
                message = item['message']['text']
            except:
                message = None
            from_ = item['message']['from']['id']
            reply = make_reply(message)
            bot.send_message(reply,from_)
from flask import Flask

app = Flask(__name__)
app.run(2222)