from flask import Flask, redirect, render_template, send_from_directory
from optparse import OptionParser
from pump import Pump
import sys

APP = Flask(__name__)
# A dictionary of pump_name: Pump
PUMPS = None

@APP.route('/')
def index():
  return render_template('index.html', pumps = Pump.to_proto(PUMPS.values()))

@APP.route('/js/<path>/')
def js(path):
  return send_from_directory('js', path)

@APP.route('/css/<path>/')
def css(path):
  return send_from_directory('css', path)

@APP.route('/v1/pump/<name>/<action>')
def pump(name, action):
  pump = PUMPS[name]
  if pump is not None:
    pump.on() if action == 'on' else pump.off()
  else:
    print "ERROR: No pump with name " + name + " exists."
  return redirect('/', code=302)

if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("-c", "--config_file", dest="config_file",
                    help="path to config_file for pumps", metavar="FILE")
  (options, args) = parser.parse_args()
  PUMPS = Pump.load_from_file(options.config_file)

  if PUMPS is None or len(PUMPS) == 0:
    print "Failed to parse config file: " + options.config_file + " (empty?)"
    sys.exit(1)

  print "Running with config:"
  print PUMPS
  APP.run(host="0.0.0.0")
