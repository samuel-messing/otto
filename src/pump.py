import pump_pb2

class Pump(object):
  OFF = 1
  ON = 2

  def __init__(self, id):
    self.id = id
    self.state = Pump.OFF
