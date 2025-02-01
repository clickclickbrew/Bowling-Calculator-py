#Dave - ClickClickBrew.dev
#1/31/25
#Bowling Computer - main.py

from player import Player

#Test on one player
#tp = Player("Test Dude")
#1 Player Test
#inp = input(" :    ")
#while inp != "end":
#    tp.append(int(inp))
#    print(tp.frameLine())
#    print(tp.scoreLine())
#    inp = input(" :    ")

#Set up the players with names - TODO: Needs attention re:format()
tName = input(format("Enter the first player's name:", '<20'))
players = []
while tName.upper() != "END":
    tplay = Player(tName)
    players.append(tplay)
    tName = input(format("Who else? (or type \'end\') ", " <20"))




#The first 9 frames
for i in range (0, 9):
    for x in players:
        roll = 0;
        for p1 in players:
            print(p1.frameLine())
            print(p1.scoreLine())
        roll = int(input(format("How many pins did " + x.name + " knock down? ", "<25")))
        x.append(roll)
        if roll == 10:  #strike check
            print("Strike! Congrats!")
            continue
        #print updated scorecard, ask for second score
        for p2 in players:
            print(p2.frameLine())
            print(p2.scoreLine())
        roll = int(input(format("How many more pins did " + x.name + " take out? ", "<25")))
        x.append(roll)

#Frame 10
for p in players:
    roll1 = 0; roll2 = 0;
    for p1 in players:
        print(p1.frameLine())
        print(p1.scoreLine())
    roll1 = int(input(format("How many pins did " + p.name + " knock down?", "<20")))
    p.append(roll1)
    if roll1 == 10:
        print("OVERTIME!")
        for p1 in players:
            print(p1.frameLine())
            print(p1.scoreLine())
        roll2 = int(input(format("How'd the second roll go for " + p.name + "?", "<20")))
        p.append(roll2)
        for p1 in players:
            print(p1.frameLine())
            print(p1.scoreLine())
        roll2 = int(input(format("Final roll for " + p.name + "?", "<20")))
        p.append(roll2)
        continue
    roll2 = int(input(format("How'd the second roll go for " + p.name + "?", "<20")))
    p.append(roll2)
    for p1 in players:
        print(p1.frameLine())
        print(p1.scoreLine())
    if (roll1 + roll2) == 10:
        print("OVERTIME!")
        for p1 in players:
            print(p1.frameLine())
            print(p1.scoreLine())
        roll2 = int(input(format("Final roll for " + p.name + "?", "<20")))

#The final score, picking a winner
for p1 in players:
        print(p1.frameLine())
        print(p1.scoreLine())
highScore = [0,0] #[score, player number]
for i in range(0, len(players)):
    if players[i].totalScore > highScore[0]:
        highScore[1] = i
print("And that's game! Congratulations " + players[highScore[1]].name + " on the victory!")