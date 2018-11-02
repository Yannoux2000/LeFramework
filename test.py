"""
This file is only used for debuging and testing
"""
import os

# from DAOs import BINDao as dao
from DAOs import JSONDao as dao
from test_GameStructs import *

#############################################

   ####### #######  #####  #######  #####
      #    #       #          #    #
      #    ###      #####     #     #####
      #    #             #    #          #
      #    #######  #####     #     #####

#############################################

def test_data_integrity():
	real_gtp = GameTickPacket(game_cars = [PlayerInfo(name = "Salut_1"),PlayerInfo(name = "Salut_2")])
	real_controller = SimpleControllerState()
	data = dao.write(Tick(real_gtp, real_controller, 0))

	read_gtp = dao.read(data)

	assert real_controller.boost == real_controller.boost
	assert real_controller.steer == real_controller.steer
	assert real_controller.pitch == real_controller.pitch

	read_gtp = read_gtp.game_tick_packet

	cara = real_gtp.game_cars[0]
	carb = read_gtp.game_cars[0]
	assert cara.physics.location.x == carb.physics.location.x

def test_read_write_in_file():
	path = "./testa/salut.{}".format(dao.ext())

	if not os.path.exists(path):
		try:
			os.makedirs( '/'.join(path.split('/')[:-1]))
		except:	pass
		os.mknod(path)
		print("file got created")
	else:
		#Overwrite
		os.system('rm ' + path)
		os.mknod(path)

	print("writing")
	for i in range(300):
		print(i)

		data = Tick(GameTickPacket(game_cars = [PlayerInfo(name = "Salut_1"),PlayerInfo(name = "Salut_2")]),
					SimpleControllerState(),i)

		file = open(path,"a")
		file.write("{}\n".format(dao.write(data)))
		file.close()

	print("reading")
	for line in open(path,"r+"):
		data = dao.read(line)
		print(data.index)

if __name__ == '__main__':
	test_data_integrity()
	test_read_write_in_file()
