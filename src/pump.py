from google.protobuf import text_format
from pump_pb2 import Pumps
import RPi.GPIO as GPIO

class Pump(object):
  def __init__(self, proto_pump):
    self.name = proto_pump.name
    self.is_running = proto_pump.is_running
    self.gpio_pin = proto_pump.gpio_pin_number

  def __repr__(self):
    return self.name + " - (GPIO=" + str(self.gpio_pin) + ")"

  def init(self):
    GPIO.setup(self.gpio_pin, GPIO.OUT)
    GPIO.output(self.gpio_pin, GPIO.HIGH)

  def on(self):
    self.is_running = True
    GPIO.output(self.gpio_pin, GPIO.LOW)

  def off(self):
    self.is_running = False
    GPIO.output(self.gpio_pin, GPIO.HIGH)

  @staticmethod
  def load_from_file(filename):
    pumps = Pumps()
    with open(filename, 'r') as f:
      content = f.read()
      text_format.Merge(content, pumps)
      return Pump.load_from_proto(pumps)
    return None

  @staticmethod
  def load_from_proto(proto_pumps):
    return { proto_pump.name: Pump(proto_pump) for proto_pump in proto_pumps.pumps }

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
