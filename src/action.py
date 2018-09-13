from action_pb2 import Action as PbAction, WATER
from google.protobuf import text_format
import config
import logging
import schedule
import time

class Action(object):
  def __init__(self, proto):
    self.plant_name = proto.plant_name
    self.action = proto.action
    self.tick = proto.tick
    self.duration_secs = proto.duration_secs
    self.logger = logging.getLogger()

  def execute(self):
    self.logger.info("START EXECUTING " + self.plant_name + " action: " + str(self.action))
    if self.action == WATER:
      plant = config.CONFIG.plants[self.plant_name]
      plant.pump.on()
      time.sleep(self.duration_secs)
      plant.pump.off()
    self.logger.info("END EXECUTING " + self.plant_name + " action: " + str(self.action))

  def schedule(self):
    min_string = ":16"
    self.logger.info("SCHEDULING " + self.plant_name + " action: " + str(self.action) + \
        " at: " + str(self.tick) + "min_string: " + min_string)
    job = schedule.every(self.tick.ticks_to_count)
    if self.tick.HasField("hourly"):
      job = job.hour
    elif self.tick.HasField("daily"):
      job = job.days.at(str(self.tick.daily.hour_of_day) + min_string)
    elif self.tick.HasField("weekly"):
      job = {
        'MONDAY': job.monday,
        'TUESDAY': job.tuesday,
        'WEDNESDAY': job.wednesday,
        'THURSDAY': job.thursday,
        'FRIDAY': job.friday,
        'SATURDAY': job.saturday,
        'SUNDAY': job.sunday
      }.get(self.tick.weekly.day_of_week, job.tuesday)
    job.do(self.execute)
