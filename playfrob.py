#!/usr/bin/env python3

import random
from numbers import Real


import interval as ji
import vo

import scamp
import scamp_extensions.pitch.utilities as pitchutils

def main():
    s = scamp.Session()
    # part = s.new_part("Organ")
    # part = s.new_part(soundfont="/Users/dandante/Downloads/ZURNA.sf2")
    # part = s.new_part(preset="Oboe",soundfont="/Users/dandante/Downloads/Oboe.sf2")
    # 7001 vcv
    # oscdump "osc.udp://:9000"
    opart = s.new_osc_part("bla", 7001, "127.0.0.1", "scamp")

    i = ji.Interval.octave.divide(4, 5)
    # interval = ji.Interval(3, 2)
    # i = interval.divide(9,7)
    # print(i)
    while True:
        random.shuffle(i)
        steps = ji.steps_to_sequence(i)
        notes = [float(pitchutils.hertz_to_midi(x)) for x in steps]
        woltage = [vo.hz_to_vpo(x) for x in steps]
        for _, pitch in enumerate(woltage):
            # print(pitch)
            opart.play_note(pitch,
                random.choice([0.6, 0.7, 0.8, 0.9, 1.0]),
                0.3 + random.choice([0.09, 0.088, 0.092, 0.087, 0.084]))



if __name__ == "__main__":
    main()
