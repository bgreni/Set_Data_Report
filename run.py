from setterChoices import SetterChoicesReport
from SetDataContainer import SetDataContainer as sdc
import argparse
import pandas as pd
import time
from multiprocessing import Process, Queue
import os


def getForSingleGame(threaded, filename):
    """Run the script only on a single game"""

    scr = SetterChoicesReport()
    fullPath = os.path.abspath(filename)
    pathList = fullPath.split("/")
    filename = pathList.pop()
    # ge the path without the filename
    path = "/".join(pathList)
    print(filename, path)
    if threaded:
        scr.runThreaded(filename, path)
    else:
        scr.run(filename, path)


def threadFunc(bigPath, game, scr, data, queue=None):
    path = bigPath + game.split("/")[0]
    scr.runThreaded(game.split("/")[1], path, data)
    queue.put((scr.totalPTAMap, scr.ptaByRotation))


def getForAllGames(makeAll):
    # CHANGE BACK
    GameStatsFolder = "/Game-Stats/"
    bigPath = os.getcwd() + GameStatsFolder
    # get a list of all folders under the Game-Stats folder
    allGames = [d for d in os.listdir("Game-Stats") if os.path.isdir(os.path.join("./Game-Stats", d))]
    filterList = ["LocationMaps", "SetCallMaps", "PTAMaps", "ImportantTimesMaps", "PositiveResetMaps", "NegativeResetMaps", "RunBreakMaps"]
    # filter out the folders containing the heatmap images
    for s in filterList:
        if s in allGames:
            allGames.remove(s)
    print(allGames)
    # format strings so they reference the csv files containing game data
    allGames = ["{}/{}.csv".format(d, d) for d in allGames]
    datas = []
    threads = []
    ptaQueue = Queue()
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
            # start a process for this particular game
            p = Process(target=threadFunc, args=[bigPath, game, scr, data, ptaQueue])
            p.start()
            threads.append(p)
        datas.append(data)
    allGamesPTA = sdc().getChoices()
    allGamesPTAByRotation = \
        {"1": sdc().getChoices(),
         "2": sdc().getChoices(),
         "3": sdc().getChoices(),
         "4": sdc().getChoices(),
         "5": sdc().getChoices(),
         "6": sdc().getChoices()}
    # combine data from each game for the all games total report
    for thread in threads:
        map1, byRotation = ptaQueue.get()
        combineMaps(allGamesPTA, map1, byRotation, allGamesPTAByRotation)
        thread.join()
    bigboidata = pd.concat(datas)
    scr = SetterChoicesReport(allptaByRotation=allGamesPTAByRotation)
    scr.givenData = True
    scr.runThreaded("All Games", bigPath, bigboidata)
    print("{:.3f} total seconds".format(time.time() - start))


def combineMaps(map1, map2, ptaByRotation, allGamesPTAByRotation):
    # combine for grand total maps
    for key in map1.keys():
        for i in range(len(map1[key])):
            map1[key][i] += map2[key][i]

    # combine for totals by rotation map
    for rotation in ptaByRotation.keys():
        for pos in ptaByRotation[rotation].keys():
            for i in range(len(ptaByRotation[rotation][pos])):
                allGamesPTAByRotation[str(rotation)][pos][i] += ptaByRotation[rotation][pos][i]

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

