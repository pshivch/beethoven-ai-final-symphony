# tokenization/musicxml_tokens.py
# Compact token spec used by the OMR seq2seq model.
# You can extend this list or swap to a BPE-based approach later.
from typing import List, Tuple

STEPS = list("CDEFGAB")
OCTS = list(range(0, 9))
DURS = ["1","1/2","1/4","1/8","1/16","1/32"]
ACCS = [-2,-1,0,1,2]

BASE = [
    "PAD","SOS","EOS","NEW_PAGE","NEW_SYSTEM",
    "MEASURE_START","MEASURE_END",
    "VOICE/1","VOICE/2","VOICE/3","VOICE/4",
    "STAFF/1","STAFF/2","STAFF/3","STAFF/4",
    "BAR/norm","BAR/repeat_start","BAR/repeat_stop",
    "TIME_NUM/1","TIME_NUM/2","TIME_NUM/3","TIME_NUM/4","TIME_NUM/6","TIME_NUM/8","TIME_NUM/12","TIME_NUM/16",
    "TIME_DEN/1","TIME_DEN/2","TIME_DEN/3","TIME_DEN/4","TIME_DEN/6","TIME_DEN/8","TIME_DEN/12","TIME_DEN/16",
    "KEY_MODE/major","KEY_MODE/minor",
    "KEY_FIFTHS/-7","KEY_FIFTHS/-6","KEY_FIFTHS/-5","KEY_FIFTHS/-4","KEY_FIFTHS/-3","KEY_FIFTHS/-2","KEY_FIFTHS/-1",
    "KEY_FIFTHS/0",
    "KEY_FIFTHS/1","KEY_FIFTHS/2","KEY_FIFTHS/3","KEY_FIFTHS/4","KEY_FIFTHS/5","KEY_FIFTHS/6","KEY_FIFTHS/7",
    "CLEF/G","CLEF/F","CLEF/C",
    "REST","DOT","CHORD","SLUR_START","SLUR_STOP","TIE_START","TIE_STOP",
    "DYN/ppp","DYN/pp","DYN/p","DYN/mp","DYN/mf","DYN/f","DYN/ff","DYN/fff",
    "CRESC_START","CRESC_STOP","DIM_START","DIM_STOP",
    "FERMATA",
]

VOCAB = BASE +     [f"PITCH/{s}{o}" for s in STEPS for o in OCTS] +     [f"ACC/{a}" for a in ACCS] +     [f"DUR/{d}" for d in DURS]

tok2id = {t:i for i,t in enumerate(VOCAB)}
id2tok = {i:t for t,i in tok2id.items()}

def encode_tokens(tokens: List[str], max_len: int) -> Tuple[list, list]:
    ids = [tok2id["SOS"]] + [tok2id[t] for t in tokens] + [tok2id["EOS"]]
    ids = ids[:max_len] + [tok2id["PAD"]] * max(0, max_len - len(ids))
    attn = [1 if x != tok2id["PAD"] else 0 for x in ids]
    return ids, attn

def decode_ids(ids: List[int]) -> List[str]:
    out = []
    for i in ids:
        t = id2tok.get(int(i), "UNK")
        if t in ("SOS","EOS","PAD"): continue
        out.append(t)
    return out
