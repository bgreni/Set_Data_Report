from setterChoices import SetterChoicesReport
import argparse
import pandas as pd
import time
from multiprocessing import Process

def getForSingleGame(threaded):
    scr = SetterChoicesReport()
    filename, path = scr.getFileName()
    if threaded:
        scr.runThreaded(filename, path)
    else:
        scr.run(filename, path)

def threadFunc(bigPath, game, scr, data):
    path = bigPath + game.split("/")[0]
    scr.runThreaded(game.split("/")[1], path, data)

def getForAllGames(makeAll):
    bigPath = "/Users/briangrenier/PycharmProjects/TestProject/Game-Stats/"
    allGames = ["Oct-18-vs-TWU/Oct-18-vs-TWU.csv",
                "Oct-19-vs-TWU/Oct-19-vs-TWU.csv",
                "Oct-25-vs-UBCO/Oct-25-vs-UBCO.csv",
                "Oct-26-vs-UBCO/Oct-26-vs-UBCO.csv",
                "Sept-20-vs-TRU/Sept-20-vs-TRU.csv"]
    datas = []
    start = time.time()
    threads = []
    for game in allGames:
        scr = SetterChoicesReport()
        scr.givenData = True
        fullpath = bigPath + game
        data = pd.read_csv(fullpath, sep=",")
        if makeAll:
            # path = bigPath + game.split("/")[0]
            # scr.runThreaded(game.split("/")[1], path, data)
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
    args = parser.parse_args()

    if args.singleFile:
        if args.threaded:
            getForSingleGame(True)
        else:
            getForSingleGame(False)
    elif args.allGames:
        if args.makeInd:
            getForAllGames(True)
        else:
            getForAllGames(False)
    else:
        print("No valid arguments where given")

