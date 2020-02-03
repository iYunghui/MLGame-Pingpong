"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
import pingpong.communication as comm
from pingpong.communication import (
	SceneInfo, GameInstruction, GameStatus, PlatformAction
)

def ml_loop(side: str):
	"""
	The main loop for the machine learning process

	The `side` parameter can be used for switch the code for either of both sides,
	so you can write the code for both sides in the same script. Such as:
	```python
	if side == "1P":
		ml_loop_for_1P()
	else:
		ml_loop_for_2P()
	```

	@param side The side which this script is executed for. Either "1P" or "2P".
	"""

	# === Here is the execution order of the loop === #
	# 1. Put the initialization code here
	x = 90
	y = 50
	flag = 2
	lastx = 75
	lasty = 100
	speed = 7
	# 2. Inform the game process that ml process is ready
	comm.ml_ready()
	
	# 3. Start an endless loop
	while True:
		# 3.1. Receive the scene information sent from the game process
		scene_info = comm.get_scene_info()

		# 3.2. If either of two sides wins the game, do the updating or
		#      reseting stuff and inform the game process when the ml process
		#      is ready.
		
		if scene_info.status == GameStatus.GAME_1P_WIN or \
		   scene_info.status == GameStatus.GAME_2P_WIN:
			# Do something updating or reseting stuff

			# 3.2.1 Inform the game process that
			#       the ml process is ready for the next round
			comm.ml_ready()
			continue

		# 3.3 Put the code here to handle the scene information
		
		x = scene_info.ball[0]
		y = scene_info.ball[1]	
		
		if lastx <= scene_info.ball[0] and lasty <= scene_info.ball[1]:
			flag = 1;
		elif lastx <= scene_info.ball[0] and lasty >= scene_info.ball[1]:
			flag = 2;
		elif lastx >= scene_info.ball[0] and lasty >= scene_info.ball[1]:
			flag = 3;
		elif lastx >= scene_info.ball[0] and lasty <= scene_info.ball[1]:
			flag = 4;
		speed = scene_info.ball_speed
		
		if flag==2 or flag==3:
			while y > 80:
				if x==0:
					if y-80<=195: 
						x = (y-80)//speed*speed
						y = y-(y-80)//speed*speed
						x = (x+speed) if (y>80) else x
						y = 80
					else:
						x = 195//speed*speed
						y = y-195//speed*speed
						y = (y-speed) if (x<195) else y
						x = 195
				elif x==195:
					if 195-(y-80)>=0:
						x = 195-(y-80)//speed*speed
						y = y-(y-80)//speed*speed
						x = (x-speed) if (y>80) else x
						y = 80
					else: 
						x = 195-195//speed*speed
						y = y-195//speed*speed
						y = (y-speed) if (x>0) else y
						x = 0
				elif flag == 2:
					if x+(y-80)<=195:
						x = x+(y-80)//speed*speed
						y = y-(y-80)//speed*speed
						x = (x+speed) if (y>80) else x
						y = 80
					else: 
						y = y-(195-x)//speed*speed
						x = x+(195-x)//speed*speed
						y = (y-speed) if (x<195) else y
						x = 195
				elif flag == 3:
					if y-80<=x:
						x = x-(y-80)//speed*speed
						y = y-(y-80)//speed*speed
						x = (x-speed) if (y>80) else x
						y = 80
					else: 
						y = y-x//speed*speed
						x = x-x//speed*speed
						y = (y-speed) if (x>0) else y
						x = 0
			x = x-(x%5)

		# 3.4 Send the instruction for this frame to the game process
		if scene_info.platform_1P[0]<x:
			comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
		elif scene_info.platform_1P[0]>x:
			comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
		elif scene_info.platform_1P[0]==x:
			comm.send_instruction(scene_info.frame, PlatformAction.NONE)
		#print(scene_info.ball[0], scene_info.ball[1], x, flag, speed, scene_info.platform_1P[0])
		lastx = scene_info.ball[0]
		lasty = scene_info.ball[1]