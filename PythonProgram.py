from __future__ import division
import time
import csv
import serial
from TwitterAPI import TwitterAPI

# [angry, happy, sad]
emotion = [0,0,0]

# [R,G,B]
owe = "Nothing"
blinking = 0
BlinkIO = False
ecount = 0
mad = 0
sad = 0
happy = 0
love = 0
scared = 0
envy = 0
suprise = 0
off = (0,0,0)
cmad = (255,0,0)
csad = (0,255,0)
chap = (255,255,0)
clov = (255,0,255)
cscr = (255,255,255)
cenv = (0,255,0)
csup = (50,50,50)
omad = 0
osad = 0
ohap = 0
olov = 0
oscr = 0
oenv = 0
osup = 0
# number of times colour has been logged
count = 0

# delay between each log
delay = 60
blinkDelay = 2
# sets timer
timeout = time.time() + delay
blinktimer = time.time() + blinkDelay
#Boolean value for if Arduino is connected
connected = False

#Serial connection setup
ser = serial.Serial("COM3", 9600)

# Twitter API setup
TRACK_TERM = "i love you, i love her, i love him, all my love,i'm in love,i really love,happiest,so happy,so excited, i'm happy,woot,w00t,wow,O_o,can't believe,wtf,unbelievable,i hate,really angry,i am mad,really hate,so angry,i wish i,i'm envious,i'm envious,i'm jealous,i want to be,why can't i,i'm so sad,i'm heartbroken,i'm so upset,i'm depressed,i can't stop crying,i'm so scared, i'm really scared, i'm terrified,i'm really afraid,so scared"


# KEEP SECRET
CONSUMER_KEY = 'AyseNJkCcwJTROFYcH1WHtVUd'
CONSUMER_SECRET = 'Hlky1qEVNQE5LB1jFBkQTyVzEHz06BBhUqPMB4cxYXaanKOpkz'
ACCESS_TOKEN_KEY = '844230415191871490-BCqZfEE5y3ZzIXHE5egzQPRG3eBbu1B'
ACCESS_TOKEN_SECRET = 'D4PMkMAJ6JpV13UPr70VSuhKy95CZVorINmT08ccj4PM5'

api = TwitterAPI(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN_KEY,
    ACCESS_TOKEN_SECRET)

# Emotion algorithm
def send (emotion):
    serialColour = ','.join(map(str,off))
    ser.write(serialColour.encode())
    print "sent off"
    time.sleep(0.1)
    serialColour = ','.join(map(str,emotion))
    serv = serialColour.encode()
    print serv
    ser.write(serv)
    print "Sent once"
    time.sleep(0.4)
    ser.write(serv)
    print "Sent twice"
def sendBlink(emotion):
    serialColour = ','.join(map(str,emotion))
    ser.write(serialColour.encode())
def percentage(mood):
    output1 = mood / ecount
    output2 = output1 * 100
    output3 = int(output2)
    print output3
    return output3
def Calc_Change(per,old):
    if per == 0 and old == 0:
        print 0
        return 0
    elif old == 0 and per >= 0:
        print per
        return per
    elif per < old and per == 0:
        print -1
        return -1
    elif per < old:
        out1 = old / per
        out = out1 - out1 - out1
        print out
        return out
    else:
        out = per / old
        print out
        return out
def ColorCalc(emotion,colorval):
    global color
    global BlinkIO
    if emotion >= 2:
        BlinkIO = True
        color = colorval
        print "Large change detected"  
        return True
        
    else:
        BlinkIO = False
        
        return False
        
#MAIN PROGRAM
emo = (csup)
send(emo)
time.sleep(2)
send(off)
r = api.request('statuses/filter', {'track': TRACK_TERM})

for item in r: # for each tweet
    if time.time() > blinktimer and BlinkIO == True:
        
        print blinking
        if blinking == 0:
            blinking = 1
            sendBlink(color)
            print "blink on"
        elif blinking == 1:
            blinking = 0
            colors = (0,0,0)
            sendBlink(colors)
            print "blink off"
        blinktimer = time.time() + blinkDelay
    if time.time() > timeout: # If time elapsed
        print "Percentages"
        pmad = percentage(mad)
        psad = percentage(sad)
        phap = percentage(happy)
        penv = percentage(envy)
        psup = percentage(suprise)
        pscr = percentage(scared)
        plov = percentage(love)
        print "Change"
        fmad = Calc_Change(pmad,omad)
        fsad = Calc_Change(psad,osad)
        fhap = Calc_Change(phap,ohap)
        fenv = Calc_Change(penv,osad)
        fsup = Calc_Change(psup,osup)
        fscr = Calc_Change(pscr,oscr)
        flov = Calc_Change(plov,olov)
        emotions = {'mad' : fmad, 'sad' : fsad, 'happy' : fhap, 'envy' : fenv, 'suprise' : fsup, 'scared' : fscr, 'love' : flov}
        we = max(emotions,key=emotions.get)
        print "the world's mood is: " + we
        if we == owe:
            print "Same emotion"
        else:
            if we == 'mad':
                blinkI = ColorCalc(fmad,cmad)
                if blinkI == False:
                    send(cmad)
                    
            elif we == 'sad':
                blinkI = ColorCalc(fsad,csad)
                if blinkI == False:
                    send(csad)
                    
            elif we == 'happy':
                blinkI = ColorCalc(fhap,chap)
                if blinkI == False:
                    send(chap)
                    
            elif we == 'envy':
                blinkI = ColorCalc(fenv,cenv)
                if blinkI == False:
                    send(cenv)
                    
            elif we == 'suprise':
                blinkI = ColorCalc(fsup,csup)
                if blinkI == False:
                    send(csup)
            elif we == 'scared':
                blinkI = ColorCalc(fscr,cscr)
                if blinkI == False:
                    send(cscr)
            elif we == 'love':
                blinkI = ColorCalc(flov,clov)
                if blinkI == False:
                    send(clov)
        owe = we
        omad = pmad
        osad = psad
        ohap = phap
        oenv = penv
        osup = psup
        oscr = pscr
        olov = plov
        love = 0
        scared = 0
        suprise = 0
        sad = 0
        mad = 0
        happy = 0
        envy = 0
        ecount = 0
        timeout = time.time() + delay #resets timer
        
    #Manipulates tweet to add to emotion counter    
    leitem = item['text'] if 'text' in item else item # select tweet text
    
    if ('i hate' or 'really angry' or 'i am mad' or 'really hate' or 'so angry') in leitem: # if tweet contains angry
        mad += 1
        ecount += 1
        print "mad"
    if ('happiest' or 'so happy' or 'so excited' or "i'm happy" or 'woot' or 'w00t' )in leitem: # if tweet contains happy but not 'not happy'
        happy += 1
        ecount += 1
        print "happy"
    if ("i'm so sad" or "i'm heartbroken" or "i'm so upset" or "i'm depressed" or "i can't stop crying") in leitem: 
        sad += 1 # add 1 to sad count
        ecount += 1
        print "sad"
    if ('i love you' or 'i love her' or 'i love him' or 'all my love' or "i'm in love" or 'i really love') in leitem:
        love += 1
        ecount += 1
        print "Love"
    if ('wow' or 'O_o' or "can't believe" or 'wtf' or 'unbelieveable') in leitem:
        suprise += 1
        ecount += 1
        print "suprise"
    if ('i wish i' or "i'm envious" or "i'm jealous" or 'i want to be' or "why can't i") in leitem:
        envy += 1
        ecount += 1
        print "envy"
    if ("i'm so scared" or "i'm really scared" or "i'm terrified" or "i'm really afraid" or "so scared") in leitem:
        scared += 1
        ecount += 1
        print "scared"
        

        
        
ser.close()

