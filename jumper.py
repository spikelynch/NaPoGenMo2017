#!/usr/bin/env python3

from nltk.corpus import framenet as fn
import random

MAX = 3;

seen = {}

def explode_frames(n, lu):
    print('  ' * n, lu.name)
    if n < MAX:
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
                for ln in fr.lexUnit:
                    if ln not in seen:
                        seen[ln] = 1
                        explode_frames(n + 1, fr.lexUnit[ln])


lus = fn.lus()

l0 = random.choice(lus)

#print(l0)
explode_frames(0, l0)

