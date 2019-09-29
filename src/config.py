from action import Action
from config_pb2 import Config as PbConfig
from google.protobuf import text_format
from action import Action
from plant import Plant
from pump import Pump
from i2c_controller import I2cController
import logging
import sys


class Config(object):
    def __init__(self, plants, pumps, actions, db, i2c):
        # List, Action
        self.actions = actions
        # Dictionary, plant_name: Plant
        self.plants = plants
        # Dictionary, pump_name: Pump
        self.pumps = pumps
        self.i2c = I2cController()
        self.db = db

    def __repr__(self):
        return '\n'.join([str(plant) for plant in self.plants.values()])

    @staticmethod
    def load_from_proto(proto, db):
        logger = logging.getLogger()
        i2c = I2cController()
        pumps = {proto_pump.name: Pump(proto_pump, db, i2c)
                 for proto_pump in proto.pumps}
        plants = {}
        for proto_plant in proto.plants:
            if proto_plant.pump_name not in pumps:
                logger.error("No pump found with name: " +
                             proto_plant.pump_name)
                sys.exit(1)
            plants[proto_plant.name] = Plant(
                proto_plant, pumps[proto_plant.pump_name])
        actions = [Action(action) for action in proto.actions]
        return Config(plants, pumps, actions, db, i2c)


def load_from_file(filename, db):
    config = PbConfig()
    with open(filename, 'r') as f:
        logger = logging.getLogger()
        content = f.read()
        logger.debug("Loading config: " + content)
        text_format.Merge(content, config)
        global CONFIG
        CONFIG = Config.load_from_proto(config, db)
