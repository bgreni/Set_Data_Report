from setterChoices import SetterChoicesReport
import argparse
import pandas as pd
import time
from multiprocessing import Process
import os


def getForSingleGame(threaded, filename):
    scr = SetterChoicesReport()
    fullPath = os.path.abspath(filename)
    pathList = fullPath.split("/")
    filename = pathList.pop()
    path = "/".join(pathList)
    print(filename, path)
    if threaded:
        scr.runThreaded(filename, path)
    else:
        scr.run(filename, path)


def threadFunc(bigPath, game, scr, data):
    path = bigPath + game.split("/")[0]
    scr.runThreaded(game.split("/")[1], path, data)


def getForAllGames(makeAll):
    bigPath = os.getcwd() + "/Game-Stats/"
    allGames = [d for d in os.listdir("Game-Stats") if os.path.isdir(os.path.join("./Game-Stats", d))]
    filterList = ["LocationMaps", "SetCallMaps", "PTAMaps", "ImportantTimesMaps", "PositiveResetMaps", "NegativeResetMaps", "RunBreakMaps"]
    for s in filterList:
        if s in allGames:
            allGames.remove(s)
    print(allGames)
    allGames = ["{}/{}.csv".format(d, d) for d in allGames]
    datas = []
    threads = []
    start = time.time()
    for game in allGames:
        scr = SetterChoicesReport()
        scr.givenData = True
        fullpath = bigPath + game
        try:
            data = pd.read_csv(fullpath, sep=",")
        except:
            raise IOError("could not read file: {}".format(game))
        if makeAll:
            p = Process(target=threadFunc, args=[bigPath, game, scr, data])
            p.start()
            threads.append(p)
        datas.append(data)
    bigboidata = pd.concat(datas)
    scr = SetterChoicesReport()
    scr.givenData = True
    scr.runThreaded("All Games", bigPath, bigboidata)
    for thread in threads:
        thread.join()
    print("{:.3f} total seconds".format(time.time() - start))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--allGames",
                        action="store_true",
                        help="Generate plots from combination of all games")
    parser.add_argument("--makeAll",
                        action="store_true",
                        help="Make plots for each individual game as well")
    parser.add_argument("--singleFile",
                        action="store_true",
                        help="Have the user chose a single file to run")
    parser.add_argument("--threaded",
                        action="store_true",
                        help="run the program in threaded mode")
    parser.add_argument("--filename",
                        action="store",
                        dest="filename",
                        help="run the program in threaded mode")
    args = parser.parse_args()

    if args.singleFile:
        if args.threaded:
            getForSingleGame(True, args.filename)
        else:
            getForSingleGame(False, args.filename)
    elif args.allGames:
        if args.makeAll:
            getForAllGames(True)
        else:
            getForAllGames(False)
    else:
        print("No valid arguments where given")

