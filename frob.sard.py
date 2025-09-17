# type: ignore

output_one = OSCHandler(
    ip="127.0.0.1", port=9000,
    name="A first test connexion",
    ahead_amount=0.0, loop=osc_loop, # The default OSC loop, don't ask why!
)

bowl.add_handler(output_one)

one = output_one.send

@swim
def one_two_test(p=0.5, i=0):
    """This is a dummy swimming function sending OSC."""
    one('random/address', value='1 2 3')
    again(one_two_test, p=0.5, i=i+1)

silence()


def osc_player(*args, **kwargs):
    """Partial function to add a new OSC player :)"""
    return play(
        output_one,
        output_one.send,
        *args, **kwargs
    )

Pa >> osc_player('random/address', value='1 2 3')

Pa * d('supermandolin', n='40 52 64 52')
Pa * d('supersaw', n='', lpf=2000, p=0.5)
# superdirt  synths:
# https://github.com/musikinformatik/SuperDirt/blob/develop/synths/default-synths.scd
Pb * d('psin', n='60.156412870005525 61.350840952616494 61.98044999134613 63.31282574001105 64.01955000865388', p=0.5)


mid = [60.156412870005525,
 72.15641287000552,
 67.1759628786594,
 65.13686286135166,
 69.0,
 64.01955000865388,
 63.26905241582932,
 69.84467193469678,
 65.95340751042883,
 68.2768737021903,
 62.8251219260429,
 74.8251219260429,
 77.13686286135166,
 79.1759628786594,
 81.84467193469678,
 84.15641287000552,
 88.01955000865388,
 93.84467193469678,
 96.15641287000552,
 74.19551288731327]

nts = " ".join([str(x) for x in mid])
nts

Pb * d('psin', n='60.156412870005525 61.350840952616494 61.98044999134613 63.31282574001105 64.01955000865388', p=0.5)
Pb * d('superpiano', n=nts, p=0.5, room=0.8)

silence(Pc)

Pc * d('superpiano', n='60 62 63 67', room=0.8)
silence()


@swim
def z(p=0.5, i=0):
    ZD('superpiano','0 1 2 3', i=i)
    again(z, p=1, i=i+1)

@swim
def z(p=0.5, i=0):
    ZD('superpiano','0 1 2 3', i=i)
    again(z, p=1, i=i+1)



#
SC('s.recHeaderFormat = "wav";')
SC('s.recSampleFormat = "int24";')
SC('s.prepareForRecord("/Users/dandante/Music/Sardine-sc/001.wav");')


SC('s.record;')
Pc * d('superpiano', n='60 62 63 67', room=0.8)

silence()
SC('s.stopRecording;') # this closes the file and deallocates the buffer recording node, etc.


SC('s.pauseRecording;') # pausable
SC('s.record;') # start again

SC('s.stopRecording;') # this closes the file and deallocates the buffer recording node, etc.


#fn =
sc_record("superpiano")   # start

# ... play patterns ...
Pc * d('superpiano', n='60 62 63 67', room=0.8)


silence()
sc_stop()

SC('("d1 outBus: " ++ ~d1.outBus).postln;')  # should print 2 if mapped to 3/4
SC('("outdevice: " ++ s.options.outDevice_).postln;')  # should print 2 if mapped to 3/4

SC('("outDevice option: " ++ Server.default.options.outDevice.asString).postln;')
SC('("inDevice  option: " ++ Server.default.options.inDevice.asString).postln;')

SC('Server.default.options.dump;')

# print("Saved:", fn)
#

####
fn = sc_record("superpiano")
Pc * d('superpiano', n='60 62 63 67', room=0.8)


# ... play for a bit ...

silence()      # stop your patterns
sc_stop(1.2)      # stop and close the file
print("Saved:", fn)

SC('~dirt.stop; ~dirt.start(57120, 0 ! 12);')  # all 12 orbits -> bus 0 (outs 1–2)
SC('("d1 outBus: " ++ ~dirt.orbits[0].outBus).postln;')  # should print 0

import time

SC('s.recHeaderFormat = "wav";')
SC('s.recSampleFormat = "int24";')
SC('s.prepareForRecord("/Users/dandante/Music/Sardine-sc/001.wav");')
time.sleep(0.1)
SC('s.record;')

Pc * d('superpiano', n='60 62 63 67', room=0.8)


silence()
SC('s.stopRecording;')
