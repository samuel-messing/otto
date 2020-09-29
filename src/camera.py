from picamera import PiCamera
from datetime import datetime
import time
import logging


class Camera(object):
    def __init__(self):
        self._camera = PiCamera()
        self._camera.resolution = (2592, 1944)
        self._camera.rotation = 180
        self._camera.start_preview()
        self.snapshot('TEST')

    def __repr__(self):
        return 'camera'

    def snapshot(self, plant_name):
        now = datetime.now().strftime("%m-%d-%Y.%H:%M:%S")
        self._camera.annotate_text = now
        start = time.time()
        self._camera.capture('imgs/%s_%s.jpg' % (plant_name, now))
        end = time.time()
        logging.getLogger().info("Camera snapshot took: %.3f seconds" % (end - start))
