from newBot import tBot
import stopstalk
import rating
import time
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
    ratingChanges = rating.ratingChange()
    if(ratingChanges):
        if(mine):
            bot.send_message(ratingChanges,mine)
    if updates:
        for item in updates:
            update_id = item['update_id']
            try:
                message = item['message']['text']
            except:(ratingChanges,)
                message = None
            from_ = item['message']['from']['id']
            mine = item['message']['from']['id']
            reply = make_reply(message)
            bot.send_message(reply,from_)
time.sleep(5)