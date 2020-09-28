from picamera import PiCamera
from datetime import datetime


class Camera(object):
    def __init__(self):
        self._camera = PiCamera()
        self._camera.resolution = (2592, 1944)
        now = datetime.now().strftime("%m-%d-%Y.%H:%M:%S")
        self._camera.annotate_text = now
        self._camera.capture('imgs/TEST_%s.png' % (now))

    def __repr__(self):
        return 'camera'

    def snapshot(self, plant_name):
        now = datetime.now().strftime("%m-%d-%Y.%H:%M:%S")
        self._camera.annotate_text = now
        self._camera.capture('imgs/%s_%s.png' % (plant_name, now))
        pass
