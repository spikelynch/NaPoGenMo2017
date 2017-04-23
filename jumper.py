#!/usr/bin/env python3

from nltk.corpus import framenet as fn
import random, re, argparse, sys

MAX = 3

QUOTES_RE = re.compile("'([^']*)'")

seen_lu = {}
seen_frame = {}
lines = {}


def extract_examples(text):
    text = re.sub(r"<fex[^>]+>", "", text)   
    bits = text.split("'")
    qs = []
    in_q = False
    q = ''
    for b in bits:
        if in_q:
            if not b or b[0] == ' ':
                # end a quote
                in_q = False
                if q:
                    qs.append(q)
                q = ''
            else:
                if q:
                    q += "'" + b
                else:
                    q = b
        if not in_q:
            if b and b[-1] == ' ':
                # start a quote
                in_q = True
                q = ''
    if q:
        qs.append(q)
    return qs
                
                    


def frame_to_sentence(frame):
    any_lines = False
    ens = frame.FE.keys()
    en = random.choice(list(ens))
    elt = frame.FE[en]
    s = []
    #print("__FRAME__ {}".format(frame.name))
    examples = extract_examples(elt.definition)
    for sentence in examples:
        if sentence not in lines:
            s.append(sentence)
    if s:
        s0 = random.choice(s)
        print(s0)
        lines[s0] = 1
        any_lines = True
    


def explode_frames(depth, lu):
    if depth:
        f = lu.frame
        frames = {}
        for fr in f.frameRelations:
            for k in [ 'Parent', 'Child', 'superFrame', 'subFrame' ]:
                if k in fr:
                    if fr[k].ID not in frames:
                        frames[fr[k].ID] = fr[k]
            
        for k in frames:
            fr = frames[k]
            frame_to_sentence(fr)
            for ln in fr.lexUnit:
                if ln not in seen_lu:
                    seen_lu[ln] = 1   
                    explode_frames(depth - 1, fr.lexUnit[ln])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--start', type=str, help="Seed word")
    ap.add_argument('-d', '--depth', type=int, default=MAX, help="Maximum recursion depth")
    args = ap.parse_args()
    l0 = ''
    if args.start:
        r = re.compile(args.start)
        lus = fn.lus(r)
        if lus:
            l0 = random.choice(lus)
        else:
            print("No matches found for {}".format(args.start))
            sys.exit(-1)
    else:
        lus = fn.lus()
        l0 = random.choice(lus)

    print(l0.name)
    explode_frames(args.depth, l0)

