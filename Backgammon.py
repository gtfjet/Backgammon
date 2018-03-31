from Tkinter import *
from random import randint
from math import floor

# Globals
gui    = Tk()
var    = StringVar()
img    = PhotoImage(file="board.gif")
board  = Canvas(gui,width=500,height=500)
font   = "Helvetica"
bot    = [0,2,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,5,0,0,0,0,0]
player = [0,0,0,0,0,0,5,0,3,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,2]
dice   = [0,0,0,0]
off    = [0,0]
start  = -1
finish = -1
botsColor    = "#663c33"
playersColor = "#fffaf2"
playersTurn  = True

# Convert point and chip number to (x0,y0,x1,y1) tuple for drawing
def map(i,j):
    if i<12:
        k = 0 if i<6 else 20;
        return (500-i*40-k,500-j*40,500-(i+1)*40-k,500-(j+1)*40)
    else:
        k = 0 if i<18 else 20;
        return ((i-12)*40+k,j*40,(i-11)*40+k,(j+1)*40)

# Convert x,y coordinate to point number (i.e. 1-24 and 0 for bar)
def imap(x,y):
    if   x>=0 and x<=240 and y<=250:
        return int(floor(x/40)+13);
    elif x>=0 and x<=240 and y>250:
        return int(12-floor(x/40));
    elif x>=260 and x<=500 and y<=250:
        return int(floor((x-20)/40)+13);
    elif x>=260 and x<=500 and y>250:
        return int(12-floor((x-20)/40));
    elif x>240 and x<260:
        return 0 # zero is the bar
    else:
        return -1

# Draw board and chips
def draw():
    board.delete("all")
    board.create_image(0,0, anchor=NW, image=img)
    for index,val in enumerate(player):
        for j in range(val):
            if index>0:
                board.create_oval(map(index-1,j),fill=playersColor)
            else:
                board.create_oval(220+5*j,180+5*j,260+5*j,220+5*j,fill=playersColor)
    for index,val in enumerate(bot):
        for j in range(val):
            if index>0:
                board.create_oval(map(index-1,j),fill=botsColor)
            else:
                board.create_oval(220+5*j,220+5*j,260+5*j,260+5*j,fill=botsColor)

# Roll die
def roll():
    global dice
    # Check that they are zero first
    if dice[0]==0 and dice[1]==0 and dice[2]==0 and dice[3]==0:
        dice = [randint(1,6), randint(1,6), 0, 0]
        # Handle doubles
        if dice[0]==dice[1]:
            dice[2]=dice[0]
            dice[3]=dice[0]
        # Display
        who = 'Player:  ' if playersTurn else 'Bot:  '
        var.set(who+str(dice[0])+'  '+str(dice[1])+'  '+str(dice[2])+'  '+str(dice[3]))

# Click triggered from button press, sets the start global
def click(event):
    global start
    p = player if playersTurn else bot
    i = imap(event.x,event.y);
    if i>=0 and (dice[0]>0 or dice[1]>0 or dice[2]>0 or dice[3]>0):
        if i>0 and p[0]>0:
            # In jail, must re-enter from bar
            start = -1
        else:
            start = i if p[i]>0 else -1
    else:
        start = -1

# Release triggered from button release, handles move
def release(event):
    global start, finish, dice, playersTurn
    p = player if playersTurn else bot   
    b = bot if playersTurn else player   
    i = imap(event.x,event.y);
    if i>=0 and start>=0:
        if start==0:
            # Re-entering from bar
            d = (i-18) if playersTurn else (7-i)
        else:
            # Normal move
            d = (start-i) if playersTurn else (i-start)
        finish = i if b[i]<2 and d in dice else -1
    if finish>=0:
        # Move from start to finish
        p[start]-=1
        p[finish]+=1
        # Handle hits
        if b[finish]==1:
            b[finish]=0
            b[0]+=1
        draw()
        # Remove from dice
        for index,val in enumerate(dice):
            if val == d:
                dice[index]=0
                break
        who = 'Player:  ' if playersTurn else 'Bot:  '
        var.set(who+str(dice[0])+'  '+str(dice[1])+'  '+str(dice[2])+'  '+str(dice[3]))
        # Handle end of turn
        if dice[0]==0 and dice[1]==0 and dice[2]==0 and dice[3]==0:
            playersTurn = not playersTurn
            var.set("Player's turn" if playersTurn else "Bot's turn")
    # reset start/finish
    start  = -1
    finish = -1


# Create widgets
var.set("Player's turn")
Button(gui,text="ROLL",fg="green",command=roll,       font=(font, 16)).grid(row=0, column=0)
Button(gui,text="QUIT",fg="red",  command=gui.destroy,font=(font, 16)).grid(row=0, column=2)
Label(gui, fg="black",textvariable=var,font=(font, 20)).grid(row=0, column=1)
board.bind("<ButtonPress-1>",   click)
board.bind("<ButtonRelease-1>", release)
board.grid(row=1, column=1)
draw()
gui.title("Dave's Backgammon Game")
gui.mainloop()