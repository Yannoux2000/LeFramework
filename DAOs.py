from collections import namedtuple

#for json
import json

#for bin
import pickle

#for xml
from lxml.etree import tostring
from lxml import objectify

import re
def select(dirty_name):
	"""
	select a DAO class that correspond to the name
	:param dirty_name: string containing name of a dao
	:return: the dao class that name corresponds to
	"""
	dao_name = re.sub('[^A-Za-z0-9]+', '', dirty_name).upper()
	if dao_name in ["JSON", "JSONDAO", "DAOJSON", "JS"]:
		return JSONDao
	if dao_name in ["BIN", "BINDAO", "DAOBIN", "PICKLE"]:
		return BINDao
	if dao_name in ["XML", "XMLDAO", "DAOXML", "LXML"]:
		return XMLDao

	raise NameError("DAO's name is not defined")

class BaseDao():
	r_mode = "r"
	w_mode = "w"
	ext = None

	def read(origin = None):
		"""
		convert the string into a object
		:param : object to deserialize
		:param : origin from where the data comes
		:return: object
		"""
		raise NotImplementedError("{}.read method".format(__class__))

	@classmethod
	def f_read(cls, file_name):
		f = cls.file(file_name, cls.r_mode)
		data = cls.read(f)
		f.close()
		return data

	def write(data_obj, origin = None):
		"""
		convert the tick object into a formated string
		:param : object to serialize
		:param : origin where the data goes
		"""
		raise NotImplementedError("{}.write method".format(__class__))

	@classmethod
	def f_write(cls, data, file_name):
		f = cls.file(file_name, cls.w_mode)
		cls.write(data, f)
		f.close()

	@classmethod
	def getext(cls):
		"""
		Return a string containing the file extention
		"""
		return cls.ext

	@classmethod
	def is_format(cls, file_name):
		"""
		Return a bool checking if the file is of format
		"""
		extlen = -len(cls.getext())
		return file_name[extlen:] == cls.getext()

	@classmethod
	def file(cls, file_name, mode):
		"""
		Return a file containing the file extention, with the correct mode
		"""
		return open(cls._f_name(file_name), mode)

	@classmethod
	def filter(cls, file_list):
		"""
		will remove names that are not of dao format
		"""
		return [f for f in file_list if cls.is_format(f)]

	#sets the correct extention
	@classmethod
	def _f_name(cls, file_name):
		if cls.is_format(file_name):
			return file_name
		else:
			return "{0}.{1}".format(file_name, cls.getext())

#STRONGLY ADVISED
class BINDao(BaseDao):
	r_mode = "rb"
	w_mode = "wb"
	ext = "bin"
	def read(origin = None):
		return pickle.load(origin)

	def write(data_obj, origin = None):
		return pickle.dump(data_obj, origin)

#Working fine
class JSONDao(BaseDao):
	ext = "json"
	def read(origin = None):
		return json.load(origin, object_hook=JSONDao._json_object_hook)

	def write(data_obj, origin = None):
		return json.dump(data_obj, origin, default=lambda data_obj: data_obj.__dict__)

	def _json_object_hook(data):
		return namedtuple('X', data.keys())(*data.values())

#Not Ready yet
class XMLDao(BaseDao):
	ext = "xml"
	def read(origin = None):
		return objectify.fromstring(origin)

	def write(data_obj, origin = None):
		return XMLDao._pyobj2XML(data_obj)

	def build_child_str(k, v):
			if isinstance(v, list):
				return XMLDao._pyobj2XML(v, k)

			if not isinstance(v, (int, float, str, bool, complex)):
				return XMLDao._pyobj2XML(v, k)

			elif isinstance(v, bool):
				#on read, mistakes 'False' for a string, not with a int because of c property
				return "<{0}>{1}</{0}>".format(k, int(v))

			else:
				return "<{0}>{1}</{0}>".format(k, v)

	def _pyobj2XML(data_obj, obj_name = None):
		'''
		process Python objects
		They can store XML attributes and/or children
		'''
		tagStr = ""		# XML string for this level
		childStr = ""	# XML string of this level's children
		if isinstance(data_obj, list):
			for k, v in enumerate(data_obj):
				childStr += XMLDao.build_child_str(k, v)

		else:
			data_dict = data_obj.__dict__
			for k, v in data_dict.items():
				childStr += XMLDao.build_child_str(k, v)

		if obj_name == None:
			return "<root>{0}</root>".format(childStr)

		if childStr == "":
			tagStr += "<{0}></{0}>".format(obj_name)
		else:
			tagStr += "<{0}>{1}</{0}>".format(obj_name, childStr)

		return tagStr

### CUSTOMIZED DAO
#you can implement your own DAOs if you feel like it, make sure that other users can access it tho. otherwise it's pointless
