blink(1) python 3 library
=========================

This python 3 module wraps [libblink1.so](https://github.com/todbot/blink1) and provides interface to call the library functions.
Also extended functions are provided.

Usage
-----

```python
>>> from blink1lib import Blink1
>>>
>>> Blink1.devices()
[(0, '2000212B', 'mk2'), (1, '20002253', 'mk2')]
>>> b1 = Blink1(serial='2000212B')  # select device by serial
>>> b2 = Blink1(dev_id=1)  # select device by id
>>>
>>> b1.on()
>>> b1.off()
>>>
>>> b2.on(rgb=(255, 0, 0), fading=5000)  # device changes color slowly
>>> b2.off()
>>>
>>> b1.on(rgb=(0, 255, 0), led=1)
>>> b1.on(rgb=(0, 0, 255), led=2)
>>> # now leds have different colors
>>> b1.off()
>>>
>>> b1.blink(rgb=(0, 0, 255), fading=500, delay=1000, count=5)
>>> # both leds blink with blue color 5 times changing state once per second and
>>> # spending half second to change color
>>> # ATTENTION! This call blocks program execution when device is blinking!
>>> # That is why it is not support infinity blinking.
>>>
>>> b1.set_pattern(0, rgb=(128, 0, 128), fading=500)
>>> b1.get_pattern(0)
Blink1Pattern(red=55, green=0, blue=55, fadding=500)
>>> # colors has different values because of gamma correction applies by libblink1.so
>>>
>>> # b1.capacity  # how many patterns can you store in the device
32
>>> b1.set_pattern(0, rgb=(255, 0, 0))
>>> b1.set_pattern(1, rgb=(0, 255, 0))
>>> b1.set_pattern(2, rgb=(0, 0, 255))
>>> b1.play(start=0, stop=2, count=3)
>>> # change colors red -> green -> blue -> ... three times
>>> # spending 300 ms for color transformation
>>>
>>> b1.play(0, 2)  # do the last operation infinitely
>>> b1.stop()  # interrupt anything started by calling play*
>>>
>>> seq = [(255, 0, 0, 300), (0, 255, 0, 2000), (0, 0, 255, 300)]
>>> b1.play_seq(seq, count=3, pos=5)  # save the sequence in the device memory
>>> # using 5, 6 and 7 slots and play it three times
>>>
>>> b1.play_blink()  # it implements Blink1.blink() using Blink1.play_seq()
>>> # You do not block you program calling this method.
>>> # Also it can blink infinitely, but does not support led selection.
>>>
>>> b1.play_state()
Blink1PlayState(playing=1, start=0, stop=32, count=0, pos=3)
>>> b1.play_state()
Blink1PlayState(playing=1, start=0, stop=32, count=0, pos=2)
>>> # same as blink1-tool --playstate
>>> b1.stop()
>>>
>>> b1.fw_version
203
>>> b1.mk_version
'mk2'
```
