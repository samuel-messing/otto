from flask import Flask, render_template
from google.protobuf import text_format
from optparse import OptionParser
from pump import Pump
from pump_pb2 import Pumps
import sys

APP = Flask(__name__)
PUMPS = Pumps()

@APP.route('/v1/pump/<pump_no>/<action>')
def pump(pump_no, action):
  print pump_no + " action: " + action
  return pump_no

@APP.route('/')
def index():
  return render_template('index.html', pumps = PUMPS)

if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("-c", "--config_file", dest="config_file",
                    help="path to config_file for pumps", metavar="FILE")
  (options, args) = parser.parse_args()
  with open(options.config_file, 'r') as f:
    content = f.read()
    text_format.Merge(content, PUMPS)

  if len(PUMPS.pumps) == 0:
    print "Failed to parse config file (empty?)"
    sys.exit(1)

  print "Running with config:"
  print PUMPS
  APP.run(host="0.0.0.0")
