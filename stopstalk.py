import requests
url = 'https://www.stopstalk.com/leaderboard.json?q=National+Institute+of+Technology%2C+Durgapur'
res=requests.get(url).json()

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def text(input_text):
    coders = res['users']
    rep=''
    if(RepresentsInt(input_text)):
        if(int(input_text)<=200):
            nxt=7
        else:
            nxt=3
    else:
        nxt=0
    if(input_text!='All'):
        for coder in coders:
            if(str(coder[nxt])==input_text):
                rep=str(coder[7])+' '+coder[0]+' '+str(coder[3])+'\n'
            if(coder[3]==0):
                break
    elif(input_text=='All'):
        count=0
        for coder in coders:
            if(count>=75):
                break
            count+=1
            rep+=str(coder[7])+' '+coder[0]+' '+str(coder[3])+'\n'
    if(rep==''):
        return 'Command not Found'
    return rep