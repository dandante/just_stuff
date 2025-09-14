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

Pa * d('supersaw', n='40 52 64 52', vowel='o')
Pa * d('supersaw', n='', lpf=2000, p=0.5)
# superdirt  synths:
# https://github.com/musikinformatik/SuperDirt/blob/develop/synths/default-synths.scd
Pb * d('psin', n='60.156412870005525 61.350840952616494 61.98044999134613 63.31282574001105 64.01955000865388', p=0.5)
silence()
