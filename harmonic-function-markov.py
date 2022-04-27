import json
import os

majors = [os.listdir("homophonic-chorales-enriched/major"), "genie-inputs/majors.csv", "homophonic-chorales-enriched/major"]
minors = [os.listdir("homophonic-chorales-enriched/minor"), "genie-inputs/minors.csv", "homophonic-chorales-enriched/minor"]


def cc_to_bayes(cc):
    return cc.replace(">", "b").replace("<", "s").replace("#", "s")


def hf_to_string(base, down, degree, major, inversion, omit, key, extra):
    return f"{base}_{down}_{degree}_{major}_{inversion}_{omit}_{key}_{extra}"


def arr_cc_to_bayes(arr):
    if len(arr) == 0:
        return "empty"
    result = ""
    for cc in arr:
        result += cc_to_bayes(cc) + "_"
    return result[:-1]

for mode in [minors, majors]:
    with open(mode[1], "w") as m:
        # m.write(
        #     "prevBase,prevIsDown,prevDegree,prevIsMajor,prevInversion,prevOmit,prevExtra,prevStrongPlace,prevNote,prevKey,"
        #     "currentBase,currentIsDown,currentDegree,currentIsMajor,currentInversion,currentOmit,currentExtra,currentStrongPlace,currentNote,currentKey")
        m.write(
            "prevHF,prevNote,prevStrongPlace,currentHF,currentNote,currentStrongPlace,nextHF,nextNote,nextStrongPlace"
        )
        for name in mode[0]:
            with open(f"{mode[2]}/{name}", "r") as f:
                chorale = json.loads(f.readline())
                chords = []
                for measure in chorale["chords"]:
                    chords += measure
                prev_function = None
                prevStrongPlace = None
                prevNote = None
                current_function = None
                currentStrongPlace = None
                currentNote = None
                for chord in chords:
                    next_function = chord["chord"]["function"]
                    nextStrongPlace = chord["strong_place"]
                    nextNote = chord["base_note_in_key"]
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
                        nextBase = next_function["base"]
                        nextIsDown = next_function["isDown"]
                        nextDegree = next_function["degree"]
                        nextIsMajor = next_function["isMajor"]
                        nextInversion = cc_to_bayes(next_function["inversion"])
                        nextOmit = arr_cc_to_bayes(next_function["omit"])
                        nextExtra = arr_cc_to_bayes(next_function["extra"])
                        nextNote = cc_to_bayes(nextNote)
                        nextKey = cc_to_bayes(next_function["key"])
                        # m.write(
                        #     f"\n{prevBase},{prevIsDown},{prevDegree},{prevIsMajor},{prevInversion},{prevOmit},{prevExtra},{prevStrongPlace},{prevNote},{prevKey},"
                        #     f"{currentBase},{currentIsDown},{currentDegree},{currentIsMajor},{currentInversion},{currentOmit},{currentExtra},{currentStrongPlace},{currentNote},{currentKey}")
                        m.write(
                            f"\n{hf_to_string(prevBase, prevIsDown, prevDegree, prevIsMajor, prevInversion, prevOmit, prevKey, prevExtra)},{prevNote},{prevStrongPlace},"
                            f"{hf_to_string(currentBase, currentIsDown, currentDegree, currentIsMajor, currentInversion, currentOmit, currentKey, currentExtra)},{currentNote},{currentStrongPlace},"
                            f"{hf_to_string(nextBase, nextIsDown, nextDegree, nextIsMajor, nextInversion, nextOmit, nextKey, nextExtra)},{nextNote},{nextStrongPlace}"
                        )
                    prev_function = current_function
                    prevStrongPlace = currentStrongPlace
                    prevNote = currentNote
                    current_function = next_function
                    currentStrongPlace = nextStrongPlace
                    currentNote = nextNote
