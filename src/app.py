from flask import Flask, redirect, render_template, send_from_directory
from optparse import OptionParser
from config import Config
from pump import Pump
import RPi.GPIO as GPIO
import sys

APP = Flask(__name__)
CONFIG = None

@APP.route('/')
def index():
  return render_template(
      'index.html',
      config = CONFIG)

@APP.route('/js/<path>/')
def js(path):
  return send_from_directory('js', path)

@APP.route('/css/<path>/')
def css(path):
  return send_from_directory('css', path)

@APP.route('/v1/pump/<name>/<action>')
def pump(name, action):
  pump = CONFIG.pumps[name]
  if pump is not None:
    pump.on() if action == 'on' else pump.off()
  else:
    print "ERROR: No pump with name " + name + " exists."
  return redirect('/', code=302)

if __name__ == "__main__":
  import logging, logging.config, yaml

  parser = OptionParser()
  parser.add_option("-c", "--config_file", dest="config_file",
                    help="path to config file for pumps", metavar="FILE")
  parser.add_option("-l", "--logging_config_file", dest="logging_config_file",
                    help="path to config file for logging", metavar="FILE")
  (options, args) = parser.parse_args()

  with open(options.logging_config_file, 'r') as logging_config:
      logging.config.dictConfig(yaml.load(logging_config))
      logger = logging.getLogger()
      logger.debug("Running with Logging config: " + options.logging_config_file)

  logger = logging.getLogger()

  logger.info("Loading CONFIG...")
  CONFIG = Config.load_from_file(options.config_file)
  if CONFIG is None:
    logger.error("Failed to parse config file: " + options.config_file + " (empty?)")
    sys.exit(1)
  logger.info("...CONFIG loaded!")
  logger.debug("Running CONFIG:\n" + str(CONFIG))

  logger.info("Initiating GPIO setup...")
  GPIO.setmode(GPIO.BCM)
  [pump.init() for pump in CONFIG.pumps.values()]
  logger.info("...GPIO setup complete!")

  logger.info("Starting server...")
  APP.run(host="0.0.0.0")
  logger.warn("...server shutdown!")
