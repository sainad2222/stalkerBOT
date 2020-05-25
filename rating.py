import requests
import time
url='https://codeforces.com/api/user.rating?handle=sainad&secret=5897c4a26a9080a8bcaa97c7b9ab7f85ab684b74'
res = requests.get(url).json()['result']
prevRating=res[-1]['newRating']
def ratingChange():
    res=requests.get(url).json()['result']
    newRating=res[-1]['newRating']
    oldRating=res[-1]['oldRating']
    contest=res[-1]['contestName']
    if(newRating!=prevRating):
        prevRating=newRating
        return 'Your rating changed by {} from {} to {} in {} contest'.format(newRating-oldRating,oldRating,newRating,contest)