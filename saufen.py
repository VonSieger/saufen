from time import sleep
from random import randint
import threading
import subprocess
import os
import sys

class GameInformation:
    def __init__(self, name):
        self.addPlayers(name)

#create action
    def addPlayers(self, players):
        self.players = players
        self.__generateActions(players)

    def __generateActions(self, players):
        self.actions = [["A drink for everybody!", "All of you, have to drink another one!"]]
        self.actions.append([])
        self.actions.append([])
        self.actions.append([])
        for p1 in players:
            self.actions[1].append(p1 + " you have to have the next sip")
            self.actions[1].append("What is about a drink for you " + p1 + "?")
            self.actions[2].append(p1 + ". Ex or Jew!" )
            self.actions[2].append(p1 + ". Ex or Merkel")
            #for player2 in players:
        #        if not player2 == player:
                #    self.actions[3].append(player2 + ". Play a round If I were you with" + player + ". It is your turn to choose an exercise.")

    #    print(self.actions)

    def getPlayers(self):
        return self.players

class SoundCreator(threading.Thread):
    def __init__(self, gameInfo, max, event):
        threading.Thread.__init__(self)
        self.gameInfo = gameInfo
        self.max = max
        self.event = event

    def run(self):
        while not self.event.is_set():
            if not self.event.wait(timeout = 60*randint(0, self.max)):
                type = self.gameInfo.actions[randint(0, len(self.gameInfo.actions)-1)]
                phrase = type[randint(0, len(type)-1)]
                self.__play(phrase)
            else:
                break

    def __play(self, phrase):
        subprocess.call(["pico2wave", "--wave=/home/boss/tmp/tmp.wav", "\"" + phrase + "\""], stdout = f, stderr = subprocess.STDOUT)
        subprocess.call(["mplayer", "/home/boss/tmp/tmp.wav"], stdout = f, stderr = subprocess.STDOUT)
        subprocess.call(["rm", "/home/boss/tmp/tmp.wav"], stdout = f, stderr = subprocess.STDOUT)

f = open(os.devnull, 'w')
names = []
print ("Who wants to get sloshed?")
while True:
    name = input()
    if name == "":
        break
    names.append(name)

if(len(names) == 0):
    sys.exit()

shutdownEvent = threading.Event()
gf = GameInformation(names)
sc = SoundCreator(gf, 5, shutdownEvent)
sc.start()

while True:
    ip = input ("/add: add a new Player\n/remove: remove a Player\n/exit: exit this game\n")
    if ip == "/exit":
        f.close()
        shutdownEvent.set()
        sys.exit(0)
    elif ip == "/add":
        ip = input("What's your name?\n")
        players = gf.getPlayers()
        if ip not in players:
            #players.append(ip)
            #print(players)
            players.append(ip)
            gf.addPlayers(players)
            print(ip + " is now drinking with you.")
        else:
            print(ip + " is already drinking.")
    elif ip == "/remove":
        players = gf.getPlayers()
        print("List of players:")
        for player in players:
            print(player)
        ip = input("Who do you want to remove?\n")
        if ip in players:
            players.remove(ip)
            print(ip + " is not drinking any more.")
            gf.addPlayers(players)
        else:
            print("You cannot remove " + ip + ". He/she did not join in before.")
