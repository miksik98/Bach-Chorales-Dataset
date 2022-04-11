from music21 import corpus, key, meter, note, stream
import json

base_notes = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

minors = 0
majors = 0


def save_to_minor(data, name):
    with open('homophonic-chorales/minor/' + name + '.json', 'w') as f:
        json.dump(data, f, default=dumper)
        print(name + " saved!")
        global minors
        minors += 1


def save_to_major(data, name):
    with open('homophonic-chorales/major/' + name + '.json', 'w') as f:
        json.dump(data, f, default=dumper)
        print(name + " saved!")
        global majors
        majors += 1


def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return None


def get_hs_note(n: note.Note):
    base_note = n.name[0]
    p = base_notes[base_note]
    p -= n.name.count("-")
    p += n.name.count("#")
    return Note(p + 12 * (n.octave + 1), base_note, n.duration.quarterLength / 4)


class Note:
    def __init__(self, pitch, base_note, duration):
        self.pitch = pitch
        self.base_note = base_note
        self.duration = duration

    def toJSON(self):
        return {
            "pitch": self.pitch,
            "base_note": self.base_note
        }


class Chord:
    def __init__(self, soprano, alto, tenor, bass, duration):
        self.soprano = soprano
        self.alto = alto
        self.tenor = tenor
        self.bass = bass
        self.duration = duration

    def toJSON(self):
        return {
            "soprano": self.soprano,
            "alto": self.alto,
            "tenor": self.tenor,
            "bass": self.bass,
            "duration": self.duration
        }


bach_paths = corpus.corpora.CoreCorpus().getComposer('bach')
all_bach_paths = corpus.getComposer('bach')
print("Total number of Bach pieces to process from music21: %i" % len(all_bach_paths))
for it, p_bach in enumerate(all_bach_paths):
    print(p_bach)
    p = corpus.parse(p_bach)
    if len(p.parts) != 4:
        continue
    k = None
    m = None
    parts = [[], [], [], []]
    for i, part in enumerate(p.parts):
        for measure in part.elements[1:]:
            if type(measure) is stream.Measure:
                parts[i].append([])
                for n in measure.elements:
                    if type(n) == key.Key:
                        minor = n.asKey(mode='minor')
                        major = n.asKey(mode='major')
                    if type(n) == meter.TimeSignature:
                        m = n.ratioString.split('/')
                    if type(n) == note.Note:
                        last = n
                        parts[i][-1].append(get_hs_note(n))
    dur = []

    for i in parts:
        c = 0
        for j in i:
            for nn in j:
                c += nn.duration
        dur.append(c)

    # skip pieces with rests and not equal voice lengths
    if dur[0] != dur[1] or dur[1] != dur[2] or dur[2] != dur[3]:
        continue

    # find the exact key of piece
    global_key = None
    file_name = str(p_bach)
    if last.name == minor.tonic.name:
        global_key = minor
    elif last.name == major.tonic.name:
        global_key = major
    else:
        # Exceptions, pieces with wrong key signatures or with many modulations inside

        if 'bwv102' in file_name or 'bwv176.6' in file_name:
            global_key = key.Key("c")
        elif 'bwv121' in file_name or 'bwv127' in file_name or 'bwv245.37' in file_name or 'bwv277.krn' in file_name or 'bwv281.krn' in file_name or 'bwv283' in file_name or 'bwv288' in file_name or 'bwv289' in file_name or 'bwv298' in file_name or 'bwv314' in file_name or 'bwv322' in file_name or 'bwv328' in file_name or 'bwv335' in file_name or 'bwv371' in file_name or 'bwv38.6' in file_name or 'bwv382' in file_name or 'bwv387' in file_name or 'bwv422' in file_name or 'bwv64.2' in file_name or 'bwv67.4' in file_name or 'bwv83.5' in file_name:
            continue
        elif 'bwv135' in file_name or 'bwv153.5' in file_name or 'bwv244.62' in file_name or 'bwv245.15' in file_name or 'bwv248.5' in file_name or 'bwv305' in file_name or 'bwv312' in file_name or 'bwv337' in file_name or 'bwv342' in file_name or 'bwv383' in file_name:
            global_key = key.Key("a")
        elif 'bwv145.5' in file_name:
            global_key = key.Key("f#")
        elif 'bwv184.5' in file_name or 'bwv248.28' in file_name or 'bwv271' in file_name:
            global_key = key.Key("D")
        elif 'bwv293' in file_name or 'bwv296' in file_name:
            global_key = key.Key("G")
        elif 'bwv254' in file_name or 'bwv265' in file_name or 'bwv276' in file_name or 'bwv277' in file_name or 'bwv297' in file_name or 'bwv4.8' in file_name or 'bwv425' in file_name or 'bwv87.7' in file_name:
            global_key = key.Key("d")
        elif 'bwv266' in file_name or 'bwv319' in file_name:
            global_key = key.Key("e")
        elif 'bwv270' in file_name or 'bwv311' in file_name:
            global_key = key.Key("b")
        elif 'bwv354' in file_name:
            global_key = key.Key("b-")
        elif 'bwv370' in file_name:
            global_key = key.Key("C")
        elif 'bwv357' in file_name or 'bwv73.5' in file_name or 'bwv85.6' in file_name or 'bwv93.7' in file_name:
            global_key = key.Key("c")
        elif 'bwv40.8' in file_name:
            global_key = key.Key("f")
        elif 'bwv309' in file_name or 'bwv341' in file_name or 'bwv343' in file_name or 'bwv344' in file_name or 'bwv351' in file_name or 'bwv364' in file_name or 'bwv372' in file_name or 'bwv40.3' in file_name or 'bwv403' in file_name or 'bwv408' in file_name or 'bwv412' in file_name or 'bwv423' in file_name:
            global_key = key.Key("g")
        else:
            raise Exception("Unknown key of " + file_name)

    chords = []

    for measure_index in range(len(parts[0])):
        sopranoNotes = parts[0][measure_index]
        altoNotes = parts[1][measure_index]
        tenorNotes = parts[2][measure_index]
        bassNotes = parts[3][measure_index]

        sopranoOffset = 0
        altoOffset = 0
        altoIndex = 0
        tenorOffset = 0
        tenorIndex = 0
        bassOffset = 0
        bassIndex = 0
        chords.append([])
        lastOffset = 0
        for i, sNote in enumerate(sopranoNotes):
            while altoOffset < sopranoOffset:
                altoOffset += altoNotes[altoIndex].duration
                if altoIndex != len(altoNotes) - 1:
                    altoIndex += 1
            while tenorOffset < sopranoOffset:
                tenorOffset += tenorNotes[tenorIndex].duration
                if tenorIndex != len(tenorNotes) - 1:
                    tenorIndex += 1
            while bassOffset < sopranoOffset:
                bassOffset += bassNotes[bassIndex].duration
                if bassIndex != len(bassNotes) - 1:
                    bassIndex += 1
            so = sopranoOffset
            sopranoOffset += sNote.duration
            if (altoOffset == so and tenorOffset == so) or (
                    altoOffset == so and bassOffset == so) or (
                    tenorOffset == so and bassOffset == so):
                chords[-1].append(Chord(sNote, altoNotes[altoIndex], tenorNotes[tenorIndex], bassNotes[bassIndex],
                                        sopranoOffset - lastOffset))
                lastOffset = sopranoOffset
    k, mode = global_key.name.split(" ")
    data = {
        'chords': chords,
        'key': k,
        'metre': f"{m[0]}/{m[1]}"
    }
    if mode == 'minor':
        save_to_minor(data, file_name.split('\\')[-1].split('.')[0])
    elif mode == 'major':
        save_to_major(data, file_name.split('\\')[-1].split('.')[0])
    else:
        raise Exception("Unknown key representation")

print("majors:", majors)
print("minors:", minors)
print("total:", majors + minors)
