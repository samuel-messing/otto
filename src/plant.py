from google.protobuf import text_format


class Plant(object):
    def __init__(self, proto_plant, pump):
        self.pump = pump
        self.name = proto_plant.name

    def __repr__(self):
        return self.name + " - (PUMP=" + str(self.pump) + ")"
