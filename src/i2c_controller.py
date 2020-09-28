import smbus
from functools import reduce


class I2cController(object):
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.on_pins = set()
        self.off_pins = {0, 1, 2, 3, 4, 5}
        self._update()

    def on(self, decimal_pin_number):
        self.off_pins.remove(decimal_pin_number)
        self.on_pins.add(decimal_pin_number)
        self._update()

    def off(self, decimal_pin_number):
        self.on_pins.remove(decimal_pin_number)
        self.off_pins.add(decimal_pin_number)
        self._update()

    def _update(self):
        # Note: weirdly you specify which pins are _off_, not which ones
        # are _on_.
        self.bus.write_byte(0x20, reduce(lambda x, y: x + y,
                                         map(lambda x: 2**x, self.off_pins)))
