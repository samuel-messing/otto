from flask import Flask
from pump import Pump

app = Flask(__name__)

@app.route('/v1/pump/<pump_no>/<action>')
def pump(pump_no, action):
  print pump_no + " action: " + action
  return pump_no

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    pump =  Pump(1)
    print "Pump state: " + pump.state
