from google.protobuf import text_format


class Pump(object):
    def __init__(self, proto_pump, db, i2c):
        self.db = db
        self.name = proto_pump.name
        self.is_running = proto_pump.is_running
        self.i2c = i2c
        self.i2c_pin_number = proto_pump.i2c_pin_number

    def __repr__(self):
        return self.name + " - (i2c=" + str(self.i2c_pin_number) + ")"

    def on(self):
        self.is_running = True
        self.i2c.on(self.i2c_pin_number)

    def off(self):
        self.is_running = False
        self.i2c.off(self.i2c_pin_number)

    def state(self):
        return 'on' if self.is_running else 'off'

    @staticmethod
    def to_proto(pumps):
        '''Converts a list of pump objects into a Pumps protobuf.'''
        pumps_pb = Pumps()
        for pump in pumps:
            pump_pb = pumps_pb.pumps.add()
            pump_pb.name = pump.name
            pump_pb.gpio_pin_number = pump.gpio_pin
            pump_pb.is_running = pump.is_running
        return pumps_pb
