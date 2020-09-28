from action_pb2 import Action as PbAction, WATER
from google.protobuf import text_format
import config
import logging
import schedule
import time


class Action(object):
    @staticmethod
    def get_time_string(hour, minute):
        return ":".join([str(hour), str(minute)])

    def __init__(self, proto):
        self.plant_name = proto.plant_name
        self.action = proto.action
        self.hourly = None
        self.daily = None
        self.weekly = None
        if proto.tick.HasField("hourly"):
            self.hourly = proto.tick.hourly
        elif proto.tick.HasField("daily"):
            self.daily = proto.tick.daily
        elif proto.tick.HasField("weekly"):
            self.weekly = proto.tick.weekly
        self.duration_secs = proto.duration_secs
        self.logger = logging.getLogger()

    def execute(self):
        self.logger.info("START EXECUTING " + self.plant_name +
                         " action: " + str(self.action))
        if self.action == WATER:
            plant = config.CONFIG.plants[self.plant_name]
            plant.pump.on()
            time.sleep(self.duration_secs)
            plant.pump.off()
        if self.action == CAMERA:
            camera = config.CONFIG.camera
            camera.snapshot(plant_name)
        self.logger.info("END EXECUTING " + self.plant_name +
                         " action: " + str(self.action))

    def schedule(self):
        if self.hourly is not None:
            self.__schedule_hourly()
        elif self.daily is not None:
            self.__schedule_daily()
        elif self.weekly is not None:
            self.__schedule_weekly()

    def __schedule_hourly(self):
        schedule.every(self.hourly.hours_to_count).hour.do(self.execute)

    def __schedule_daily(self):
        schedule \
            .every(self.daily.days_to_count) \
            .days.at(Action.get_time_string(self.daily.hour, self.daily.min)) \
            .do(self.execute)

    def __schedule_weekly(self):
        time_string = Action.get_time_string(self.weekly.hour, self.weekly.min)
        for day in self.weekly.day_of_week:
            if day == 0:
                schedule.every().monday.at(time_string).do(self.execute)
            elif day == 1:
                schedule.every().tuesday.at(time_string).do(self.execute)
            elif day == 2:
                schedule.every().wednesday.at(time_string).do(self.execute)
            elif day == 3:
                schedule.every().thursday.at(time_string).do(self.execute)
            elif day == 4:
                schedule.every().friday.at(time_string).do(self.execute)
            elif day == 5:
                schedule.every().saturday.at(time_string).do(self.execute)
            elif day == 6:
                schedule.every().sunday.at(time_string).do(self.execute)
            else:
                print("invalid day of week:", day)
