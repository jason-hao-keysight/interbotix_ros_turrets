'''
    File name: RPiServoDriver.py
    Author: Jason Hao
    Date created: November 8, 2022
    Date last modified: November 10, 2022
'''

from flask import Flask, request
from interbotix_xs_modules.turret import InterbotixTurretXS

DEG_TO_RAD = 0.01745329251994329576923690768489

robot = InterbotixTurretXS(
    robot_model="wxxms",
    pan_profile_type="time",
    tilt_profile_type="time"
)

app = Flask(__name__)

@app.post('/pantilt')
def func():
	content_type = request.headers.get('Content-Type')
	if (content_type == 'application/json'):
		json = request.json
		pan = json['pan']
		tilt = json['tilt']
		robot.turret.pan_tilt_move(
				pan_position=pan*DEG_TO_RAD,
				tilt_position=tilt*DEG_TO_RAD,
				pan_profile_velocity=1,
				pan_profile_acceleration=.1,
				tilt_profile_velocity=1,
				tilt_profile_acceleration=.1,
				blocking=True)
		return json
	else:
		return 'Content-Type not supported!'

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)