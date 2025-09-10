#!/usr/bin/env python3


import sf2utils
import scamp
s = scamp.Session()
part = s.new_part(preset="Oboe",soundfont="/Users/dandante/Downloads/Oboe.sf2")
for pitch in range(60, 70):
    part.play_note(pitch, 1, 0.5)
