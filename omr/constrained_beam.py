# omr/constrained_beam.py
# Generic constrained beam search for OMR decoding.
# Plug this into your seq2seq model's logits step.

from typing import List, Tuple, Dict
import math

class DecodeState:
    def __init__(self):
        self.in_measure = False
        self.open_slurs = 0
        self.open_ties = 0
        self.time_num = None
        self.time_den = None
        self.beats_accum = 0.0   # in quarter lengths

def allowed_next(prev_tokens: List[str], state: DecodeState, cand: str) -> bool:
    # Hard rules to reduce illegal sequences.
    if not prev_tokens and cand != "SOS":
        return False
    if cand == "MEASURE_END" and not state.in_measure:
        return False
    if cand == "MEASURE_START" and state.in_measure:
        return False
    if cand.startswith("TIME_DEN/") and state.time_num is None:
        # require TIME_NUM before DEN
        return False
    # prevent closing slurs/ties negative
    if cand == "SLUR_STOP" and state.open_slurs == 0:
        return False
    if cand == "TIE_STOP" and state.open_ties == 0:
        return False
    return True

def update_state(state: DecodeState, tok: str) -> None:
    if tok == "MEASURE_START":
        state.in_measure = True; state.beats_accum = 0.0
    elif tok == "MEASURE_END":
        state.in_measure = False
    elif tok.startswith("TIME_NUM/"):
        state.time_num = int(tok.split("/")[1])
    elif tok.startswith("TIME_DEN/"):
        state.time_den = int(tok.split("/")[1])
    elif tok == "SLUR_START":
        state.open_slurs += 1
    elif tok == "SLUR_STOP" and state.open_slurs > 0:
        state.open_slurs -= 1
    elif tok == "TIE_START":
        state.open_ties += 1
    elif tok == "TIE_STOP" and state.open_ties > 0:
        state.open_ties -= 1
    elif tok.startswith("DUR/"):
        q = _frac_to_quarter(tok.split("/")[1])
        state.beats_accum += q
    elif tok.startswith("REST_DUR/"):
        q = _frac_to_quarter(tok.split("/")[1])
        state.beats_accum += q

def _frac_to_quarter(frac: str) -> float:
    if frac == "1": return 4.0
    num, den = frac.split("/")
    return 4.0 * (int(num) / int(den))

def beam_search(step_fn, start_tok_id: int, eos_tok_id: int, id2tok, beam_size=5, max_len=1024):
    Beams = [([start_tok_id], 0.0, DecodeState())]  # (ids, logp, state)
    for t in range(max_len):
        new_beams = []
        for ids, logp, st in Beams:
            if ids[-1] == eos_tok_id:
                new_beams.append((ids, logp, st)); continue
            logits = step_fn(ids)  # returns log-probs over vocab at next step
            for cand_id, lp in topk_logits(logits, k=beam_size):
                tok = id2tok[cand_id]
                st2 = deepcopy_state(st)
                if allowed_next([id2tok[i] for i in ids], st2, tok):
                    update_state(st2, tok)
                    new_beams.append((ids+[cand_id], logp + lp, st2))
        # prune
        new_beams.sort(key=lambda x: x[1], reverse=True)
        Beams = new_beams[:beam_size]
        # optional early stop if all beams ended
        if all(b[0][-1] == eos_tok_id for b in Beams): break
    return max(Beams, key=lambda x: x[1])[0]

def topk_logits(logits, k=5):
    # logits: List[(id, logp)] OR tensor; here assume list
    # For illustration; replace with tensor ops.
    return logits[:k]

def deepcopy_state(st: DecodeState) -> DecodeState:
    s = DecodeState()
    s.in_measure = st.in_measure
    s.open_slurs = st.open_slurs
    s.open_ties = st.open_ties
    s.time_num = st.time_num
    s.time_den = st.time_den
    s.beats_accum = st.beats_accum
    return s
