import json
import os

majors = [os.listdir("homophonic-chorales-enriched/major"), "genie-inputs/majors.csv", "homophonic-chorales-enriched/major"]
minors = [os.listdir("homophonic-chorales-enriched/minor"), "genie-inputs/minors.csv", "homophonic-chorales-enriched/minor"]


def cc_to_bayes(cc):
    return cc.replace(">", "-").replace("<", "+")


def arr_cc_to_bayes(arr):
    if len(arr) == 0:
        return "empty"
    result = ""
    for cc in arr:
        result += cc_to_bayes(cc) + "_"
    return result[:-1]

for mode in [minors, majors]:
    with open(mode[1], "w") as m:
        m.write(
            "prevBase,prevIsDown,prevDegree,prevIsMajor,prevInversion,prevOmit,prevExtra,prevStrongPlace,prevNote,prevKey,"
            "currentBase,currentIsDown,currentDegree,currentIsMajor,currentInversion,currentOmit,currentExtra,currentStrongPlace,currentNote,currentKey")
        for name in mode[0]:
            with open(f"{mode[2]}/{name}", "r") as f:
                chorale = json.loads(f.readline())
                chords = []
                for measure in chorale["chords"]:
                    chords += measure
                prev_function = None
                prevStrongPlace = None
                prevNote = None
                for chord in chords:
                    current_function = chord["chord"]["function"]
                    currentStrongPlace = chord["strong_place"]
                    currentNote = chord["base_note_in_key"]
                    if prev_function is not None:
                        prevBase = prev_function["base"]
                        prevIsDown = prev_function["isDown"]
                        prevDegree = prev_function["degree"]
                        prevIsMajor = prev_function["isMajor"]
                        prevInversion = cc_to_bayes(prev_function["inversion"])
                        prevOmit = arr_cc_to_bayes(prev_function["omit"])
                        prevExtra = arr_cc_to_bayes(prev_function["extra"])
                        prevKey = cc_to_bayes(prev_function["key"])
                        currentBase = current_function["base"]
                        currentIsDown = current_function["isDown"]
                        currentDegree = current_function["degree"]
                        currentIsMajor = current_function["isMajor"]
                        currentInversion = cc_to_bayes(current_function["inversion"])
                        currentOmit = arr_cc_to_bayes(current_function["omit"])
                        currentExtra = arr_cc_to_bayes(current_function["extra"])
                        currentNote = cc_to_bayes(currentNote)
                        currentKey = cc_to_bayes(current_function["key"])
                        m.write(
                            f"\n{prevBase},{prevIsDown},{prevDegree},{prevIsMajor},{prevInversion},{prevOmit},{prevExtra},{prevStrongPlace},{prevNote},{prevKey},"
                            f"{currentBase},{currentIsDown},{currentDegree},{currentIsMajor},{currentInversion},{currentOmit},{currentExtra},{currentStrongPlace},{currentNote},{currentKey}")
                    prev_function = current_function
                    prevStrongPlace = currentStrongPlace
                    prevNote = currentNote
