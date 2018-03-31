from Tkinter import *
from random import randint
from math import floor

# Globals
gui    = Tk()
var    = StringVar()
who    = StringVar()
img    = PhotoImage(file="board.gif")
board  = Canvas(gui,width=500,height=500)
font   = "Helvetica"
bot    = [2,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,5,0,0,0,0,0]
player = [0,0,0,0,0,5,0,3,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,2]
dice   = [0,0,0,0]
start  = -1
finish = -1
playersTurn = True

# Methods
def map(i,j):
    if i<12:
        k = 0 if i<6 else 20;
        return(500-i*40-k,500-j*40,500-(i+1)*40-k,500-(j+1)*40)
    else:
        k = 0 if i<18 else 20;
        return((i-12)*40+k,j*40,(i-11)*40+k,(j+1)*40)
     
def imap(x,y):
    if   x>=0 and x<=240 and y<=250:
        return int(floor(x/40)+12);
    elif x>=0 and x<=240 and y>250:
        return int(11-floor(x/40));
    elif x>=260 and x<=500 and y<=250:
        return int(floor((x-20)/40)+12);
    elif x>=260 and x<=500 and y>250:
        return int(18-floor((x-20)/40)-7);
    else:
        return -1
        
def draw():
    board.delete("all")
    board.create_image(0,0, anchor=NW, image=img)
    for index,val in enumerate(player):
        for j in range(val):
            board.create_oval(map(index,j),fill="#400000")
    for index,val in enumerate(bot):
        for j in range(val):
            board.create_oval(map(index,j),fill="#fffaf2")
        
def roll():
    global dice
    if dice[0]==0 and dice[1]==0 and dice[2]==0 and dice[3]==0:
        dice = [randint(1,6), randint(1,6), 0, 0]
        if dice[0]==dice[1]:
            dice[2]=dice[0]
            dice[3]=dice[0]
        var.set(str(dice[0])+'  '+str(dice[1])+'  '+str(dice[2])+'  '+str(dice[3]))

def click(event):
    global start
    p = player if playersTurn else bot
    i = imap(event.x,event.y);
    if i>=0 and (dice[0]>0 or dice[1]>0 or dice[2]>0 or dice[3]>0):
        start = i if p[i]>0 else -1
    else:
        start = -1

def release(event):
    global start, finish
    global dice
    global playersTurn
    p = player if playersTurn else bot   
    b = bot if playersTurn else player   
    i = imap(event.x,event.y);
    if i>=0 and start>=0:
        d = (start-i) if playersTurn else (i-start)
        finish = i if b[i]<2 and d in dice else -1
    if finish>=0:
        p[start]-=1
        p[finish]+=1
        draw()
        for index,val in enumerate(dice):
            if val == d:
                dice[index]=0
                break
        var.set(str(dice[0])+'  '+str(dice[1])+'  '+str(dice[2])+'  '+str(dice[3]))
        if dice[0]==0 and dice[1]==0 and dice[2]==0 and dice[3]==0:
            playersTurn = not playersTurn
            var.set('')
            who.set('Player' if playersTurn else 'Bot')
    # reset start/finish
    start  = -1
    finish = -1


who.set('Player' if playersTurn else 'Bot')
# Create widgets
Button(gui,text="ROLL",fg="green",command=roll,       font=(font, 16)).grid(row=0, column=0)
Button(gui,text="QUIT",fg="red",  command=gui.destroy,font=(font, 16)).grid(row=0, column=2)
Label(gui, fg="black",textvariable=var,font=(font, 20)).grid(row=0, column=1)
Label(gui, fg="black",textvariable=who,font=(font, 20)).grid(row=3, column=1)
board.bind("<ButtonPress-1>",   click)
board.bind("<ButtonRelease-1>", release)
board.grid(row=1, column=1)
draw()
gui.title("Dave's Backgammon Game")
gui.mainloop()