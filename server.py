from flask import Flask, render_template, request, jsonify
import garage
app = Flask(__name__)

@app.route('/trigger', methods=['POST'])
def triggerDoor():

	status = {
		'doorState' : "Closing..." if garage.isDoorOpen() else "Opening..."
	}
	garage.sendDoorSignal()

	return jsonify(status)

@app.route('/status')
def getStatus():
	status = {
		'isDoorOpen': garage.isDoorOpen()
      	}

	return jsonify(status)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
