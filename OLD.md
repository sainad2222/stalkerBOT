# OLD
# saiscrapperbot
### Bot Functions (so far):
1. Notifies with a message whenever ratings are changed in codeforces
![RatingChange](https://user-images.githubusercontent.com/44405294/83235109-009f2580-a1af-11ea-9723-2404b5009645.png)
2. Fetches your leaderboard details form stopstalk
![StopStalk](https://user-images.githubusercontent.com/44405294/83235101-fc730800-a1ae-11ea-89b1-6deba481c46b.png)

Available commands: (based on the url specified)


1. All -> Fetches leaderboard details of top 75
2. Any rank -> Gets details at rank specified
3. username -> fetches details from username
4. Full Name -> fetches details from Full Name


### Usage:
1. Go to `BotFather` in telegram and create a bot
2. Above step will give you an api token
3. Clone this repository to a folder
`git clone https://github.com/sainad2222/saiscrapperbot.git`
4. Navigate to the folder and edit config.cfg and paste your token there
5. Now go to stopstalk.py and change url there to your college url(add .json after leaderboard)
6. You can host this script in heroku for free
