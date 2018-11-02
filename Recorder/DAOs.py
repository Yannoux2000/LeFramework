from collections import namedtuple

#for json
import json

#for xml
from lxml import etree
from lxml import objectify

#for bin
import pickle

class BaseDao():
	def read(data_str):
		"""
		convert the string into a object
		"""
		raise "{}Read method : not implemented yet".format(__name__)

	def write(data_obj):
		"""
		convert the tick object into a formated string
		"""
		raise "{}Write method : not implemented yet".format(__name__)

	def ext():
		"""
		Return a string containing the file extention
		"""
		raise "{}Ext method : not implemented yet".format(__name__)


class JSONDao(BaseDao):
	def _json_object_hook(data):
		return namedtuple('X', data.keys())(*data.values())

	def read(data_str):
		return json.loads(data_str, object_hook=JSONDao._json_object_hook)

	def write(data_obj):
		return json.dumps(data_obj, default=lambda data_obj: data_obj.__dict__)

	def ext():
		return "json"

class BINDao(BaseDao):
	def read(data_str):
		return pickle.loads(data_str)

	def write(data_obj):
		return pickle.dumps(data_obj)

	def ext():
		return "bin"

#deprecated : does not write correctly
class XMLDao(BaseDao):
	def _xml_object_hook(data):
		return namedtuple('X', data.keys())(*data.values())

	def read(data_str):
		return objectify.fromstring(data_str)

	def write(data_obj):
		etree.tostring(data_obj)

	def ext():
		return "xml"

### CUSTOMIZED DAO

#############################################

   ####### #######  #####  #######  #####
      #    #       #          #    #
      #    ###      #####     #     #####
      #    #             #    #          #
      #    #######  #####     #     #####

#############################################

def test_DAO(dao_class):
	real_gtp = GameTickPacket(game_cars=[PlayerInfo()])
	real_controller = SimpleControllerState()

	data = dao_class.write(Tick(real_gtp, real_controller, 0))
	read_gtp = dao_class.read(data)

	assert real_controller.boost == real_controller.boost
	assert real_controller.steer == real_controller.steer
	assert real_controller.pitch == real_controller.pitch

	read_gtp = read_gtp.game_tick_packet

	cara = real_gtp.game_cars[0]
	carb = read_gtp.game_cars[0]
	assert cara.physics.location.x == carb.physics.location.x
	
if __name__ == '__main__':
	from Tick import Tick
	from GameStructs import *
	test_DAO(JSONDao)
	test_DAO(BINDao)
	# test_DAO(XMLDao)
