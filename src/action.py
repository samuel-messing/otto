from action_pb2 import Action as PbAction, WATER
from google.protobuf import text_format
import config
import schedule
import time

class Action(object):
  def __init__(self, proto):
    self.plant_name = proto.plant_name
    self.action = proto.action
    self.tick = proto.tick
    self.duration_secs = proto.duration_secs

  def execute(self):
    if self.action == WATER:
      plant = config.CONFIG.plants[self.plant_name]
      plant.pump.on()
      time.sleep(self.duration_secs)
      plant.pump.off()

  def schedule(self):
    job = schedule.every(self.tick.ticks_to_count)
    if self.tick.HasField("hourly"):
      job = job.hour
    elif self.tick.HasField("daily"):
      job = job.days.at(str(self.tick.daily.hour_of_day) + ":00")
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
