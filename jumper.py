#!/usr/bin/env python3

from nltk.corpus import framenet as fn
import random, re, argparse, sys

MAX = 3

QUOTES_RE = re.compile("'([^']*)'")

seen = {}
lines = {}

def frame_to_sentence(frame):
    for en, elt in frame.FE.items():
        for sentence in QUOTES_RE.findall(elt.definition):
            if sentence not in lines:
                print(sentence)
                lines[sentence] = 1
    


def explode_frames(depth, lu):
    if depth:
        f = lu.frame
        frames = [ f ]
        for fr in f.frameRelations:
            if "superFrame" in fr:
                frames.append(fr.superFrame)
            if "subFrame" in fr:
                frames.append(fr.subFrame)
        fr_seen = {}
        for fr in frames:
            if fr.name not in fr_seen:
                fr_seen[fr.name] = 1
                frame_to_sentence(fr)
                for ln in fr.lexUnit:
                    if ln not in seen:
                        seen[ln] = 1   
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

