# python3

import os
import time
from collections import namedtuple
import logging
from ctypes import CDLL, byref, POINTER
from ctypes import c_int, c_ubyte, c_ushort
from ctypes import c_char_p, c_void_p
from ctypes.util import find_library


__all__ = ("libblink1", "Blink1")


__version_info__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_info__))


def choose(*args):
    for arg in args:
        if arg is not None:
            return arg

    raise ValueError("all args is None")


class cached_property(object):

    def __init__(self, function):
        super(cached_property, self).__init__()
        self.__function = function

    def __get__(self, instance, cls=None):
        value = self.__function(instance)
        setattr(instance, self.__function.__name__, value)
        return value


c_ubyte_p = POINTER(c_ubyte)
c_ushort_p = POINTER(c_ushort)


def _load():
    name = find_library("blink1")

    if not name:
        name = os.path.abspath("libblink1.so")

        if not os.access(name, os.R_OK):
            raise ImportError("no blink(1) shared library found")

    return CDLL(name)

_libblink1 = _load()

_libblink1.blink1_enumerate.restype = c_int
_libblink1.blink1_enumerate.argtypes = ()

# blink1_enumerateByVidPid
# blink1_openByPath

_libblink1.blink1_openBySerial.restype = c_void_p
_libblink1.blink1_openBySerial.argtypes = (c_char_p, )

# blink1_openById
# blink1_open

_libblink1.blink1_close.restype = None
_libblink1.blink1_close.argtypes = (c_void_p, )

# blink1_write
# blink1_read

_libblink1.blink1_getVersion.restype = c_int
_libblink1.blink1_getVersion.argtypes = (c_void_p, )

_libblink1.blink1_fadeToRGB.restype = c_int
_libblink1.blink1_fadeToRGB.argtypes = (c_void_p, c_ushort, c_ubyte, c_ubyte, c_ubyte)

_libblink1.blink1_fadeToRGBN.restype = c_int
_libblink1.blink1_fadeToRGBN.argtypes = (c_void_p, c_ushort, c_ubyte, c_ubyte, c_ubyte, c_ubyte)

# blink1_setRGB
# blink1_readRGB
# blink1_readRGB_mk1
# blink1_eeread
# blink1_eewrite
# blink1_serialnumread
# blink1_serialnumwrite
# blink1_serverdown
# blink1_play

_libblink1.blink1_playloop.restype = c_int
_libblink1.blink1_playloop.argtypes = (c_void_p, c_ubyte, c_ubyte, c_ubyte, c_ubyte)

_libblink1.blink1_readPlayState.restype = c_int
_libblink1.blink1_readPlayState.argtypes = (c_void_p, c_ubyte_p, c_ubyte_p, c_ubyte_p, c_ubyte_p, c_ubyte_p)

_libblink1.blink1_writePatternLine.restype = c_int
_libblink1.blink1_writePatternLine.argtypes = (c_void_p, c_ushort, c_ubyte, c_ubyte, c_ubyte, c_ubyte)

_libblink1.blink1_readPatternLine.restype = c_int
_libblink1.blink1_readPatternLine.argtypes = (c_void_p, c_ushort_p, c_ubyte_p, c_ubyte_p, c_ubyte_p, c_ubyte)

_libblink1.blink1_savePattern.restype = c_int
_libblink1.blink1_savePattern.argtypes = (c_void_p, )

# blink1_testtest
# blink1_enableDegamma
# blink1_disableDegamma
# blink1_degamma
# blink1_sleep
# blink1_vid
# blink1_pid
# blink1_getCachedPath

_libblink1.blink1_getCachedSerial.restype = c_char_p
_libblink1.blink1_getCachedSerial.argtypes = (c_int, )

# blink1_getCacheIndexByPath
# blink1_getCacheIndexBySerial
# blink1_getCacheIndexByDev
# blink1_clearCacheDev
# blink1_getSerialForDev
# blink1_getCachedCount

_libblink1.blink1_isMk2ById.restype = c_int
_libblink1.blink1_isMk2ById.argtypes = (c_int, )

_libblink1.blink1_isMk2.restype = c_int
_libblink1.blink1_isMk2.argtypes = (c_void_p, )


class libblink1Type(object):

    __no_check_retcode = ("close", "enumerate", "getCachedSerial")

    __instance = None

    def __new__(cls):
        if cls.__instance is not None:
            return cls.__instance

        cls.__instance = super().__new__(cls)
        return cls.__instance

    def __getattr__(self, name):
        if name.startswith("_"):
            return super().__getattr__(name)

        func_name = "blink1_{}".format(name)

        if not hasattr(_libblink1, func_name):
            return getattr(_libblink1, name)

        if name.startswith("open"):
            self.__wrap_open(name, func_name)

        elif name in self.__no_check_retcode:
            self.__wrap_no_check(name, func_name)

        else:
            self.__wrap(name, func_name)

        return getattr(self, name)

    def __wrap_open(self, name, func_name):
        def wrapper(self, *args):
            func = getattr(self, func_name)
            dev = func(*args)

            logging.debug("libblink1.{}({}) -> {!r}".format(
                name, ", ".join("{!r}".format(x) for x in args), dev))

            if not dev:
                raise RuntimeError("cannot open blink(1)")

            return dev

        wrapper.__name__ = name
        setattr(self.__class__, name, wrapper)

    def __wrap_no_check(self, name, func_name):
        def wrapper(self, *args):
            func = getattr(self, func_name)
            retval = func(*args)

            logging.debug("libblink1.{}({}) -> {!r}".format(
                name, ", ".join("{!r}".format(x) for x in args), retval))

            return retval

        wrapper.__name__ = name
        setattr(self.__class__, name, wrapper)

    def __wrap(self, name, func_name):
        def wrapper(self, *args):
            func = getattr(self, func_name)
            retval = func(*args)

            logging.debug("libblink1.{}({}) -> {!r}".format(
                name, ", ".join("{!r}".format(x) for x in args), retval))

            if retval == -1:
                raise RuntimeError("error on {}".format(name))

            return retval

        wrapper.__name__ = name
        setattr(self.__class__, name, wrapper)

libblink1 = libblink1Type()


class Blink1Device(object):

    def __init__(self, serial):
        super(Blink1Device, self).__init__()

        if isinstance(serial, int):
            serial = str(serial)

        if isinstance(serial, str):
            serial = serial.encode("ascii")

        self.serial = serial

        self.dev = None
        self.count = 0

    def open(self):
        if self.count == 0:
            self.dev = libblink1.openBySerial(self.serial)

        self.count += 1

        return self.dev

    def close(self):
        if self.count == 0:
            return

        self.count -= 1

        if self.count == 0:
            libblink1.close(self.dev)
            self.dev = None

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


Blink1Pattern = namedtuple("Blink1Pattern", ("red", "green", "blue", "fadding"))
Blink1PlayState = namedtuple("Blink1PlayState", ("playing", "start", "stop", "count", "pos"))


class Blink1(object):

    _memory_slot_count = {
        "mk1": 12,
        "mk2": 32,
    }

    def __init__(self, dev_id=None, serial=None):
        super(Blink1, self).__init__()

        self.default_rgb = (255, 255, 255)
        self.default_fading = 300
        self.default_delay = 500
        self.default_count = 3

        if serial is None:
            if libblink1.enumerate() == 0:
                raise RuntimeError("no blink(1) devices found")

            serial = libblink1.getCachedSerial(dev_id or 0)

        self._blink1 = Blink1Device(serial)

    @classmethod
    def devices(cls):
        result = []

        for i in range(libblink1.enumerate()):
            serial = libblink1.getCachedSerial(i)
            is_mk2 = libblink1.isMk2ById(i)
            result.append((i, serial.decode("ascii"), "mk2" if is_mk2 else "mk1"))

        return result

    def on(self, rgb=None, fading=None, led=None):
        rgb = choose(rgb, self.default_rgb)
        fading = choose(fading, self.default_fading)

        with self._blink1 as dev:
            self._fade(dev, rgb, fading, led)

    def off(self, fading=None, led=None):
        self.on(rgb=(0, 0, 0), fading=fading, led=led)

    def blink(self, rgb=None, fading=None, delay=None, led=None, count=3):
        rgb = choose(rgb, self.default_rgb)
        fading = choose(fading, self.default_fading)
        delay = choose(delay, self.default_delay)

        delay /= 1000

        with self._blink1 as dev:
            for _ in range(count):
                self._fade(dev, rgb, fading, led)
                time.sleep(delay)
                self._fade(dev, (0, 0, 0), fading, led)
                time.sleep(delay)

    @staticmethod
    def _fade(dev, rgb, fading, led):
        red, green, blue = rgb

        if led is None:
            libblink1.fadeToRGB(dev, fading, red, green, blue)
        else:
            libblink1.fadeToRGBN(dev, fading, red, green, blue, led)

    def get_pattern(self, pos):
        fading = c_ushort()
        red = c_ubyte()
        green = c_ubyte()
        blue = c_ubyte()

        with self._blink1 as dev:
            libblink1.readPatternLine(dev, byref(fading), byref(red), byref(green),
                                      byref(blue), pos)

        return Blink1Pattern(red.value, green.value, blue.value, fading.value)

    def set_pattern(self, pos, rgb, fading=None):
        fading = choose(fading, self.default_fading)

        red, green, blue = rgb

        with self._blink1 as dev:
            libblink1.writePatternLine(dev, fading, red, green, blue, pos)

    @cached_property
    def capacity(self):
        return self._memory_slot_count[self.mk_version]

    def play(self, start=0, stop=0, count=0):
        with self._blink1 as dev:
            libblink1.playloop(dev, 1, start, stop, count)

    def stop(self):
        with self._blink1 as dev:
            libblink1.playloop(dev, 0, 0, 0, 0)

    def play_seq(self, seq, count=0, pos=0):
        if not seq:
            return

        if len(seq) + pos > self.capacity:
            raise ValueError("sequence too long")

        if len(seq) == 1:
            r, g, b, fading = seq[0]
            self.on(rgb=(r, g, b), fading=fading)
            return

        if self.mk_version == "mk1":
            seq = list(seq)

            while len(seq) < self.capacity:
                seq.append((0, 0, 0, 0))

            stop, count = 0, 0

        else:
            stop = pos + len(seq) - 1

        with self._blink1 as dev:
            for n, pattern in enumerate(seq, pos):
                r, g, b, fading = pattern
                libblink1.writePatternLine(dev, fading, r, g, b, n)

            libblink1.playloop(dev, 1, pos, stop, count)

    def play_blink(self, rgb=None, fading=None, delay=None, count=3, pos=0):
        rgb = choose(rgb, self.default_rgb)
        fading = choose(fading, self.default_fading)
        delay = choose(delay, self.default_delay)

        red, green, blue = rgb
        seq = (
            (red, green, blue, fading),
            (red, green, blue, delay - fading),
            (0, 0, 0, fading),
            (0, 0, 0, delay - fading),
        )
        self.play_seq(seq=seq, count=count, pos=pos)

    def play_state(self):
        playing = c_ubyte()
        start = c_ubyte()
        stop = c_ubyte()
        count = c_ubyte()
        pos = c_ubyte()

        with self._blink1 as dev:
            libblink1.readPlayState(dev, byref(playing), byref(start), byref(stop),
                                    byref(count), byref(pos))

        return Blink1PlayState(playing.value, start.value, stop.value, count.value, pos.value)

    @cached_property
    def fw_version(self):
        with self._blink1 as dev:
            return libblink1.getVersion(dev)

    @cached_property
    def mk_version(self):
        libblink1.enumerate()  # fill the library cache

        with self._blink1 as dev:
            if libblink1.isMk2(dev):
                return "mk2"

            return "mk1"
