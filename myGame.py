from Tkinter import *
import random

class Game(Canvas):

    width = 300
    height = 300
    userSize = 10
    coinSize = 10
    renderFactor = 10
    initialCoinDrop = 10


    def __init__(self, parent):
        Canvas.__init__(self,width=Game.width,height=Game.height,
            background='black',borderwidth=0)

        self.parent = parent

        self.initUI()
        self.pack()

    def initUI(self):

        self.initialTurn = True
        self.isGameOver = False
        self.gold = 0
        self.createJew()
        self.createCoins()

        self.focus_set()
        self.bind_all('<Key>',self.key)
        self.pack()

    def createJew(self):

        #self.x1 = 0
        #self.y1 = 0
        self.x1 = (Game.width//2)-(Game.userSize//2)
        self.y1 = (Game.height//2)-(Game.userSize//2)
        self.x2 = self.x1 + Game.userSize
        self.y2 = self.y1 + Game.userSize

        self.user = self.create_rectangle(self.x1,self.y1,self.x2,self.y2,
            fill='white')


    def createCoins(self):
        self.coins = []
        self.colors = ['red','yellow']
        self.dropCoins(Game.initialCoinDrop)

    def dropCoins(self,numOfCoins):
        for i in range(numOfCoins):
            tempX = random.randrange(0,Game.width-Game.coinSize,Game.coinSize)
            tempY = random.randrange(0,Game.height-Game.coinSize,Game.coinSize)
            tempColor = random.randint(0,len(self.colors)-1)

            tag = (str(tempX),str(tempY))
            self.create_rectangle(tempX,tempY,tempX+Game.coinSize,
                tempY+Game.coinSize,fill=self.colors[tempColor],
                tags=(tag,))
            self.coins.append([tempX,tempY,self.colors[tempColor]])

    def key(self,event):
        key = event.keysym

        if self.isGameOver:

            if event.char == 'r':
                self.delete(ALL)
                self.__init__(self.parent)
            else:
                self.create_text(150,180,text='No, r',fill='blue')
        else:
            if key == 'Left':
                self.update(-1,0)
            elif key == 'Right':
                self.update(1,0)
            elif key == 'Up':
                self.update(0,-1)
            elif key == 'Down':
                self.update(0,1)

    def update(self,x,y):
        factor = Game.renderFactor
        self.x1 += x*factor
        self.y1 += y*factor
        self.x2 += x*factor
        self.y2 += y*factor

        self.isBound()
        self.gameLogic()

        if self.isGameOver:
            self.create_text(150,150,text='GameOver',fill='blue')
            self.create_text(150,165,text='press r to continue',fill='blue')

    def isBound(self):
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2

        if x1 < 0 or y1 < 0:
            self.isGameOver = True
        elif x2 > Game.height or y2 > Game.width:
            self.isGameOver = True
        else:
            self.coords(self.user,self.x1,self.y1,self.x2,self.y2)

    def gameLogic(self):
        x1 = self.x1
        y1 = self.y1

        jsize = Game.userSize
        csize = Game.coinSize

        for coin in self.coins:

            if (
                (x1 == coin[0] and y1 == coin[1]) or
                (x1+jsize == coin[0]+csize and y1 == coin[1]) or
                (x1 == coin[0] and y1+jsize == coin[1]+csize) or
                (x1+jsize == coin[0]+csize and y1+jsize == coin[1]+csize)
                ):

                self.delete((str(coin[0]),str(coin[1])))
                self.coins.remove(coin)

                if self.initialTurn:
                    self.setColor(coin)
                elif coin[2] == self.color:
                    self.isGameOver = True
                else:
                    self.dropCoins(2)

                break
            else:
                continue
    def setColor(self,coin):
        coinColor = coin[2]
        if self.initialTurn:
            self.initialTurn = False
            self.color = coinColor
            self.itemconfig(self.user,fill=coinColor)
        else:
            self.gold += 1

class myGame(Frame):

    def __init__(self,parent):
        Frame.__init__(self,parent)

        parent.title('Jew Simulator')
        self.game = Game(parent)
        self.pack()

def main():
    root = Tk()
    game = myGame(root)
    root.mainloop()

main()
