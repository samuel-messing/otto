from flask import Flask, redirect, render_template, send_from_directory
from optparse import OptionParser
import RPi.GPIO as GPIO
import atexit
import config
import sys
import threading
import time

APP = Flask(__name__)


@APP.route('/')
def index():
    return render_template(
        'index.html',
        config=config.CONFIG)


@APP.route('/js/<path>/')
def js(path):
    return send_from_directory('js', path)


@APP.route('/css/<path>/')
def css(path):
    return send_from_directory('css', path)


@APP.route('/v1/pump/<name>/<action>')
def pump(name, action):
    pump = config.CONFIG.pumps[name]
    if pump is not None:
        pump.on() if action == 'on' else pump.off()
    else:
        print("ERROR: No pump with name", name, "exists.", sep=" ")
    return redirect('/', code=302)


def run_scheduler():
    import schedule
    while True:
        schedule.run_pending()
        time.sleep(1)


def gpio_cleanup():
    GPIO.cleanup()


if __name__ == "__main__":
    import logging
    import logging.config
    import yaml

    parser = OptionParser()
    parser.add_option("-c", "--config_file", dest="config_file",
                      help="path to config file for pumps", metavar="FILE")
    parser.add_option("-l", "--logging_config_file", dest="logging_config_file",
                      help="path to config file for logging", metavar="FILE")
    (options, args) = parser.parse_args()

    with open(options.logging_config_file, 'r') as logging_config:
        logging.config.dictConfig(yaml.load(logging_config))
        logger = logging.getLogger()
        logger.debug("Running with Logging config: " +
                     options.logging_config_file)

    logger = logging.getLogger()

    logger.info("Loading CONFIG...")
    config.load_from_file(options.config_file)
    if config.CONFIG is None:
        logger.error("Failed to parse config file: " +
                     options.config_file + " (empty?)")
        sys.exit(1)
    logger.debug("Loaded CONFIG:\n" + str(config.CONFIG))
    logger.info("...done!")

    logger.info("Initiating GPIO setup...")
    GPIO.setmode(GPIO.BCM)
    atexit.register(gpio_cleanup)
    [pump.init() for pump in config.CONFIG.pumps.values()]
    logger.info("...done!")

    logger.debug("Scheduling actions...")
    for action in config.CONFIG.actions:
        action.schedule()
    logger.debug("...done!")

    logger.info("Starting scheduler executor thread...")
    scheduler = threading.Thread(target=run_scheduler)
    scheduler.daemon = True
    scheduler.start()
    logger.debug("...done!")

    logger.info("Starting server...")
    APP.run(host="0.0.0.0")
    logger.warn("...server shutdown!")
