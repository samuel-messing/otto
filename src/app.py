from db import Db
from flask import Flask, redirect, render_template, send_from_directory, send_file
from optparse import OptionParser
import RPi.GPIO as GPIO
import atexit
import config
import sys
import threading
import time
import glob

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
    if (action == 'state'):
        return pump.state()
    if pump is not None:
        pump.on() if action == 'on' else pump.off()
    else:
        print("ERROR: No pump with name", name, "exists.", sep=" ")
    return redirect('/', code=302)


@APP.route('/v1/camera/latest')
def picture():
    images = glob.glob("imgs/*.png")
    images.sort()
    logger.info('Serving image at: %s' % images[0])
    return send_file('../' + images[0], mimetype='image/png')


def run_scheduler():
    import schedule
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    import logging
    import logging.config
    import yaml

    parser = OptionParser()
    parser.add_option("-c", "--config_file", dest="config_file",
                      help="path to config file", metavar="FILE")
    parser.add_option("-l", "--logging_config_file", dest="logging_config_file",
                      help="path to logging config file", metavar="FILE")
    parser.add_option("-d", "--db_file", dest="db_file",
                      help="path to database file", metavar="FILE")
    (options, args) = parser.parse_args()

    with open(options.logging_config_file, 'r') as logging_config:
        logging.config.dictConfig(yaml.load(logging_config))
        logger = logging.getLogger()
        logger.debug("Running with Logging config: " +
                     options.logging_config_file)

    logger = logging.getLogger()

    logger.info("Initializing DB...")
    if options.db_file is None:
        logger.error("Need to specify db file!")
        sys.exit(1)
    db = Db(options.db_file)
    logger.info("...done!")

    logger.info("Loading CONFIG...")
    config.load_from_file(options.config_file, db)
    if config.CONFIG is None:
        logger.error("Failed to parse config file: " +
                     options.config_file + " (empty?)")
        sys.exit(1)
    logger.info("...done!")

    logger.info("Initiating GPIO setup...")
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
