#Dave - ClickClickBrew.dev
#1/31/25
#Bowling Computer - player.py
import random

class Player:
    #This is for Player objects, which contain a name and necessary data for building a scorecard -
    fGap = 10 #Defines the whitespace between frames in output functions (frameLine and scoreLine)

    def __init__(self, tname = "bowler" + str(random.randint(0, 1337))):
        #Declaring all the data to track scores

        self.name = tname #player name if we don't want it to be 'bowler423'
        
        self.frames = []
        for i in range(0, 13):
            self.frames.append([-1, -1])
        #The data on each roll is in frames, accessed like: frames[frame][roll 1(0) or 2(1)]
        #frames is then filled with -1's, to differentiate "no data" from "rolled a gutterball"
        #While I hastily set up 13 frames (to account for strikes on the 10th), it looks like
        #only 11 are needed (frame 10 being [9], two strikes going to [11])
        
        self.current_frame = 0; self.current_round = 0;
        #Used to track where append() should put the next number

        self.spare = False;                     #Flag for handling spares 
        self.frameScores = []                   #Scores at each frame
        for i in range(0, 13):
            self.frameScores.append(0)
        self.totalScore = 0                     #total score
        
        
            

    def append(self, hit):
        #How we'll add data on pins knocked down for each roll.
        #Should add a stop when the game's over - currently relies on main.py knowing when to quit
        if hit == 10 and self.current_round == 0:  #-------------------------------------------Strike Handler
            self.frames[self.current_frame][0]  = 10
            self.current_frame+=1
            if self.spare: self.updateScore(); self.spare = False
            return "Strike!"
        if self.current_round != 0 and (hit + self.frames[self.current_frame][0]) == 10: #-----Spare Handling
            self.frames[self.current_frame][1] = hit; print(hit)
            self.current_round = 0; self.current_frame+=1
            self.spare = True
            return "Spare!"
        self.frames[self.current_frame][self.current_round] = hit #----------------------------Regular Hits
        if self.current_round > 0:
            self.current_round = 0; self.current_frame+=1
            self.updateScore()
        else:
            self.current_round+=1


    def updateScore(self):
        #Updates the per-frame and total scores (self.frameScores[] and self.totalScore)
        score = 0;
        for i in range(0, self.current_frame):
            if i == 10: break
            if self.frames[i][0] == 10:    #-----------------------------frame being processed is a strike
                if self.frames[i+1][0] == 10 and self.frames[i+2][0] != -1:
                    score += 10 + 10 + self.frames[i+2][0]
                    self.frameScores[i] = score                    
                elif self.frames[i+1][1] != -1:
                    score += 10 + self.frames[i+1][0] + self.frames[i+1][1]
                    self.frameScores[i] = score
            elif (self.frames[i][0] + self.frames[i][1]) == 10: #--------frame being processed is a spare
                if self.frames[i+1][0] != -1:
                    score += 10 + self.frames[i+1][0]
                    self.frameScores[i] = score
            elif self.frames[i][1] != -1: #------------------------------not a special frame
                score += self.frames[i][0] + self.frames[i][1]
                self.frameScores[i] = score
        
        self.totalScore = score
        return 1
    
    def pS(self, x,y):
        #Function I made way too late to simplify what would be multiple instances of str(frame[x][y])
        #and checking if they should be X for strike, blank space, etc. 
        #Makes everything two characters - "10" & " 6" instead of "10" & "6", so things line up right.
        val = self.frames[x][y]
        if val < 0:
            return "  "
        if val == 10:
            return "10"
        if val < 10:
            return " " + str(val)
        return "ER" 

    def frameLine(self):
        #This makes the upper portion of the scorecard - name, individual rolls, and total score
        #returned as a long string for main.py to print
        rString = format(self.name, "<16")
        #TODO: r1, r2 and the chain of ifs in the for loop are probably redundant, were written before pS() was defined
        r1 = ""; r2 = ""
        for i in range(0, 9):
            if self.frames[i][0] == 10:
                r1 = " X"
                r2 = "  "
            elif (self.frames[i][0] + self.frames[i][1]) == 10:
                r1 = str(self.frames[i][0])
                r2 = " /"
            else:
                if self.frames[i][0] == -1:
                    r1 = r2 = "  "
                elif self.frames[i][1] == -1:
                    r1 = str(self.frames[i][0]); r2 = "  "
                else:
                    r1 = self.pS(i, 0); r2 = self.pS(i, 1)
            rString = rString + format(r1 + "|" + r2, f"<{self.fGap}")
        if self.frames[9][0] != -1:
            if self.frames[9][0] == 10 and self.frames[10][0] == 10:
                if self.frames[11][0] == 10:
                    rString = rString + format("X|X|X", f"<{self.fGap}")
                elif self.frames[11][0] != -1:
                    rString = rString + format("X|X|" + self.pS(11,0), f"<{self.fGap}")
                else:
                    rString = rString + format("X|X| ", f"<{self.fGap}")
            elif (self.frames[9][0] + self.frames[9][1]) == 10:
                if self.frames[10][0] != -1:
                    rString = rString + format(self.pS(9,0) + "|" + self.pS(9,1) + "|" + self.pS(10,0), f"<{self.fGap}")
                else:
                    rString = rString + format(self.pS(9,0) + "|" + self.pS(9,1) + "|" + "  ", f"<{self.fGap}")
            else:
                rString = rString + format(self.pS(9,0) + "|" + self.pS(9,1), f"<{self.fGap}")
        else:
            rString = rString + format("  |  ", f"<{self.fGap}")
        rString = rString + str(self.totalScore)
        return rString

    def scoreLine(self):
        #This makes the lower portion of the scorecard - scores per frame
        #returned as a long string for main.py to print
        rString = format(" ", "<16")
        for i in range(0, 10):
            if self.frameScores[i] == 0:
                rString = rString + format(" ", f"<{self.fGap}")
            else:
                rString = rString + format(str(self.frameScores[i]), f"<{self.fGap}")
        return rString



