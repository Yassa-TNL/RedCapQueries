import json
from copy import deepcopy

class Record():
	'''
	This is a class that defines a single 'record' in the final spreadsheet
	It will include all fields of all forms of every project
	Includes date, master_id, and project for sorting and identification of records
	'''

	# Static variable for class, updated after building data_template
	data_template = {}	
	form_dict = None

	def __init__(self, proj_name: str, raw_record: dict):
		'''
		proj_name: the project this record belongs to
		raw_record: a single record that is returned from RedCap in a 'record' query
		'''
		self._date = raw_record['date_stamp']
		self._master_id = int(raw_record['master_id'])
		self._proj_name = proj_name


		self._data = deepcopy(Record.data_template)
		for key in raw_record.keys():
			#print()
			#print("Key: {}".format(key))
			#print("Form: {}".format(Record.form_dict[key]))
	
			# There are some values that are not in any forms...
			if key not in Record.form_dict.keys():
				continue
			form = Record.form_dict[key]	
			self._data[form][key] = raw_record[key]


	def data_to_list(self, label_order: [tuple]) -> list:
		'''	
		Return the data stored in this record, using the order of (form, key) that is used in label_order
		
		Params:
			label_order: a list of tuples that contain the form key values in the order we want
		Return:	
			list: a list of the 'values' corresponding to the form, key in this record
		'''
	
		# Initialize res with some values that we want that are not related to any of the labels
		res = [self._master_id, self._date, self._proj_name]
		for form, key in label_order:
			res.append(self._data[form][key])
		return res
