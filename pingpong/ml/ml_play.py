"""The template of the main script of the machine learning process
"""

import pingpong.communication as comm
from pingpong.communication import (
	SceneInfo, GameInstruction, GameStatus, PlatformAction
)
import pickle
import numpy as np
import os.path
import zipfile

def ml_loop(side: str):
	"""The main loop of the machine learning process

	This loop is run in a seperate process, and communicates with the game process.

	Note that the game process won't wait for the ml process to generate the
	GameInstrcution. It is possible that the frame of the GameInstruction
	is behind of the current frame in the game process. Try to decrease the fps
	to avoid this situation.
	"""

	# === Here is the execution order of the loop === #
	# 1. Put the initialization code here.
	lastx = 75
	lasty = 100
	flag = 1
	speed = 7
	# 2. Inform the game process that ml process is ready before start the loop.
	zipname='Model.zip'
	filepath = os.path.join(os.path.dirname(__file__), zipname)
	z = zipfile.ZipFile(filepath, 'r')
	P1_path = z.extract('model_1.sav')
	P2_path = z.extract('model_2.sav')
	z.close()
	if side == "1P":
		load_model = pickle.load(open(P1_path, 'rb'))
	else:
		load_model = pickle.load(open(P2_path, 'rb'))
	comm.ml_ready()
	# 3. Start an endless loop.
	while True:
		# 3.1. Receive the scene information sent from the game process.
		scene_info = comm.get_scene_info()
		
		# 3.2. If the game is over or passed, the game process will reset
		#      the scene immediately and send the scene information again.
		#      Therefore, receive the reset scene information.
		#      You can do proper actions, when the game is over or passed.
		if scene_info.status == GameStatus.GAME_1P_WIN or \
		   scene_info.status == GameStatus.GAME_2P_WIN:
			# Do something updating or reseting stuff

			# 3.2.1 Inform the game process that
			#       the ml process is ready for the next round
			comm.ml_ready()
			continue

		# 3.3. Put the code here to handle the scene information
		if lastx <= scene_info.ball[0] and lasty <= scene_info.ball[1]:
			flag = 1;
		elif lastx <= scene_info.ball[0] and lasty >= scene_info.ball[1]:
			flag = 2;
		elif lastx >= scene_info.ball[0] and lasty >= scene_info.ball[1]:
			flag = 3;
		elif lastx >= scene_info.ball[0] and lasty <= scene_info.ball[1]:
			flag = 4;
		speed = scene_info.ball_speed
		inp_temp = np.array([lastx, lasty, scene_info.ball[0], scene_info.ball[1], flag, speed])
		input = inp_temp[np.newaxis, :]
		instr = load_model.predict(input)
		instr = instr-(instr%5)
		# 3.4. Send the instruction for this frame to the game process
		if side == "1P":
			if scene_info.platform_1P[0]<instr:
				comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
			elif scene_info.platform_1P[0]>instr:
				comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
			elif scene_info.platform_1P[0]==instr:
				comm.send_instruction(scene_info.frame, PlatformAction.NONE)
		else:
			if scene_info.platform_2P[0]<instr:
				comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
			elif scene_info.platform_2P[0]>instr:
				comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
			elif scene_info.platform_2P[0]==instr:
				comm.send_instruction(scene_info.frame, PlatformAction.NONE)
			
		lastx = scene_info.ball[0]
		lasty = scene_info.ball[1]