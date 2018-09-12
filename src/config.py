from google.protobuf import text_format
from config_pb2 import Config as PbConfig
from plant import Plant
from pump import Pump
import logging
import sys

class Config(object):
  def __init__(self, plants):
    self.plants = plants
    self.pumps = {pump.name: pump for pump in [plant.pump for plant in plants.values()]}
    pass

  def __repr__(self):
    return '\n'.join([str(plant) for plant in self.plants.values()])

  @staticmethod
  def load_from_proto(proto):
    logger = logging.getLogger()
    pumps = {proto_pump.name: Pump(proto_pump) for proto_pump in proto.pumps}
    plants = {}
    for proto_plant in proto.plants:
      if proto_plant.pump_name not in pumps:
        logger.error("No pump found with name: " + proto_plant.pump_name)
        sys.exit(1)
      plants[proto_plant.name] = Plant(proto_plant, pumps[proto_plant.pump_name])
    return Config(plants)

  @staticmethod
  def load_from_file(filename):
    config = PbConfig()
    with open(filename, 'r') as f:
      content = f.read()
      text_format.Merge(content, config)
      return Config.load_from_proto(config)
    return None

