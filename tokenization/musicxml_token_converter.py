# tokenization/musicxml_token_converter.py
# Convert between MusicXML and the compact token stream.
# Requires: music21 (pip install music21)

import argparse, json
from typing import List
from music21 import converter as m21converter, note, chord, meter, key, stream, duration, clef, expressions, dynamics
from musicxml_tokens import VOCAB, tok2id, id2tok

def musicxml_to_tokens(path: str) -> List[str]:
    s = m21converter.parse(path)
    tokens = []
    # Global context (first time signature, key, clef per part)
    ts = s.recurse().getElementsByClass(meter.TimeSignature)
    if ts:
        tokens += [f"TIME_NUM/{ts[0].numerator}", f"TIME_DEN/{ts[0].denominator}"]
    ky = s.recurse().getElementsByClass(key.KeySignature)
    if ky:
        fifths = ky[0].sharps
        mode = "major" if getattr(ky[0], 'mode', 'major') == 'major' else 'minor'
        tokens += [f"KEY_FIFTHS/{fifths}", f"KEY_MODE/{mode}"]
    parts = s.parts if s.parts else [s]
    for si, part in enumerate(parts, start=1):
        tokens.append(f"STAFF/{si}")
        # clef (best guess)
        c = part.recurse().getElementsByClass(clef.Clef)
        if c:
            if isinstance(c[0], clef.TrebleClef):
                tokens.append("CLEF/G")
            elif isinstance(c[0], clef.BassClef):
                tokens.append("CLEF/F")
            else:
                tokens.append("CLEF/C")
        measures = part.getElementsByClass(stream.Measure)
        for m in measures:
            tokens.append("MEASURE_START")
            # dynamics attached to measure start (rough)
            for dyn in m.recurse().getElementsByClass(dynamics.Dynamic):
                mark = f"DYN/{dyn.value}"
                if mark in VOCAB:
                    tokens.append(mark)
                    break
            for el in m.recurse().notesAndRests:
                if isinstance(el, note.Note):
                    pitch = f"PITCH/{el.pitch.step}{el.pitch.octave}"
                    acc = el.pitch.accidental
                    acc_tok = f"ACC/{0 if acc is None else acc.alter}"
                    dur_q = el.duration.quarterLength
                    tokens += [pitch, acc_tok, f"DUR/{_dur_to_frac(dur_q)}"]
                    if el.tie:
                        if el.tie.type in ("start","continue"):
                            tokens.append("TIE_START")
                        if el.tie.type in ("stop","continue"):
                            tokens.append("TIE_STOP")
                    if el.expressions:
                        tokens.append("SLUR_START")  # heuristic
                elif isinstance(el, chord.Chord):
                    # chord: head + CHORD for subsequent notes
                    base = el[0]
                    pitch = f"PITCH/{base.pitch.step}{base.pitch.octave}"
                    acc_tok = f"ACC/{0 if base.pitch.accidental is None else base.pitch.accidental.alter}"
                    tokens += [pitch, acc_tok, f"DUR/{_dur_to_frac(el.duration.quarterLength)}"]
                    for n in el[1:]:
                        tokens += ["CHORD", f"PITCH/{n.pitch.step}{n.pitch.octave}",
                                   f"ACC/{0 if n.pitch.accidental is None else n.pitch.accidental.alter}"]
                else:
                    # rest
                    tokens += ["REST", f"REST_DUR/{_dur_to_frac(el.duration.quarterLength)}"]
            tokens.append("MEASURE_END")
    return tokens

def tokens_to_musicxml(tokens: List[str], out_path: str):
    s = stream.Score()
    part = stream.Part()
    cur_measure = stream.Measure()
    cur_voice = stream.Voice()
    quarter = 1.0
    i = 0
    # defaults
    ts_num, ts_den = 4, 4
    ky_fifths, ky_mode = 0, 'major'
    while i < len(tokens):
        t = tokens[i]
        if t.startswith("TIME_NUM/"):
            ts_num = int(t.split("/")[1])
        elif t.startswith("TIME_DEN/"):
            ts_den = int(t.split("/")[1])
            cur_measure.append(meter.TimeSignature(f"{ts_num}/{ts_den}"))
        elif t.startswith("KEY_FIFTHS/"):
            ky_fifths = int(t.split("/")[1])
        elif t.startswith("KEY_MODE/"):
            ky_mode = t.split("/")[1]
            cur_measure.append(key.KeySignature(ky_fifths))
        elif t == "MEASURE_START":
            cur_measure = stream.Measure()
        elif t == "MEASURE_END":
            if len(cur_voice):
                cur_measure.append(cur_voice)
                cur_voice = stream.Voice()
            part.append(cur_measure)
        elif t.startswith("PITCH/"):
            step, octv = t.split("/")[1][0], int(t.split("/")[1][1:])
            # expect ACC and DUR next
            acc = 0
            dur_tok = "DUR/1/4"
            if i+1 < len(tokens) and tokens[i+1].startswith("ACC/"):
                acc = int(tokens[i+1].split("/")[1]); i += 1
            if i+1 < len(tokens) and tokens[i+1].startswith("DUR/"):
                dur_tok = tokens[i+1]; i += 1
            n = note.Note(f"{step}{octv}")
            if acc != 0: n.pitch.accidental = acc
            n.duration = duration.Duration(_frac_to_quarter(dur_tok.split('/')[1]))
            cur_voice.append(n)
        elif t == "REST":
            # expect REST_DUR next
            dur_tok = "REST_DUR/1/4"
            if i+1 < len(tokens) and tokens[i+1].startswith("REST_DUR/"):
                dur_tok = tokens[i+1]; i += 1
            r = note.Rest()
            r.duration = duration.Duration(_frac_to_quarter(dur_tok.split('/')[1]))
            cur_voice.append(r)
        elif t == "CHORD":
            # next PITCH token -> addNote to previous chord via tie-voice approach
            pass  # left as simple; extend as needed
        i += 1
    s.insert(0, part)
    s.write('musicxml', out_path)

def _dur_to_frac(q):
    # maps common quarter lengths to string fractions
    mapping = {4.0:"1", 2.0:"1/2", 1.0:"1/4", 0.5:"1/8", 0.25:"1/16", 0.125:"1/32"}
    return mapping.get(float(q), "1/4")

def _frac_to_quarter(frac: str) -> float:
    if frac == "1": return 4.0
    num, den = frac.split("/")
    return 4.0 * (int(num) / int(den))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--to-tokens", help="Input MusicXML -> tokens.json")
    ap.add_argument("--to-musicxml", help="Input tokens.json -> out.musicxml")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if args.to_tokens:
        toks = musicxml_to_tokens(args.to_tokens)
        with open(args.out, "w") as f: json.dump(toks, f, indent=2)
    else:
        toks = json.load(open(args.to_musicxml))
        tokens_to_musicxml(toks, args.out)
