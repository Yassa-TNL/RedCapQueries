from config import *
from lib.query import *
from lib.Record import Record
from  urllib.request import urlopen, Request
from urllib.parse import urlencode
import sys
from collections import defaultdict
import json
import time

import csv


def build_form_dict(data_dictionary_records) -> dict:
	'''
	For a project, build a dictionary that maps the keys to each form	
	
	Params:
		data_dictionary_records: json object | this should be a list of json objects representing the rows in the data dictionary
	Return:
		dict: a dictionary that maps keys/columns -> form
	'''
	result = {}

	for i, record in enumerate(data_dictionary_records):
		# If the field is a checkbox, we have to add more fields than just 1
		if record['field_type'] == 'checkbox':
			num_checkboxes = len(record['select_choices_or_calculations'].split("|"))
			for j in range(num_checkboxes):
				result[record['field_name'] + '___' + str(j+1)] = record['form_name']
		else:
			result[record['field_name']] = record['form_name'] 
	return result		

def combine_form_dicts(form_dicts: [dict]) -> dict:
	'''
	Takes in a list of form_dicts that show the form->key of each form for all projects.
	We need a union of these dicts to get every form and every field for every form.
	
	Params:
		form_dicts: list of dict
	Return:
		a single dictionary containing all the combined data
	'''
	form_dict = {}
	for fd in form_dicts:
		for key,value in fd.items():
			form_dict[key] = value	
	return form_dict

def build_data_template(form_dict: dict) -> {dict: str}:
	'''	
	Build a 'data_template', is a dict that has the structure form->key->value	
	This will store all values for a single record in the final matrix
	
	Params: 
		form_dict: the form dict (key->form)
	Return:
		data_template: a template for a record in the final matrix
			(form->key->value)
	'''
	if DEBUG:
		start = time.time()
		print("  * Building ... ",end="")
	data_template = defaultdict(dict) 
	for key, form in form_dict.items():
		data_template[form][key] = ""	
	if DEBUG:
		print("Done. ({:.2f} seconds)".format(time.time() - start))
	return data_template


def format_project_records(proj_name: str, proj_records: json) -> [Record]:
	'''
	Process a list of records from a project and return a list of Records
	
	Params:
		proj_name: str
		proj_records: json list of raw records

	Return:
		list of Record objects
	'''
	records = []
	if DEBUG:
		start = time.time()
		print("  * Formatting {} raw records ... ".format(proj_name),end="")

	for raw_record in proj_records:	
		record = Record(proj_name, raw_record)	
		records.append(record)
		



	if DEBUG:
		print("Done. ({} records in {:.2f} seconds)".format(len(proj_records), time.time() - start))
	return records


def build_order_of_cols(data_template: {dict: str}) -> [tuple]:
	'''
	Build the order of the labels in the final matrix given the data template
	
	Params:
		data_template: dict->dict->str
			form -> key -> value
	Return:
		label_order: list of tuple
			List containing (form, key) that correspond to each column
	'''
	form_order = sorted(data_template.keys())
	label_order = []
	for form in form_order:
		for key in sorted(data_template[form].keys()):
			label_order.append((form,key))
	return label_order

def main():
	output_file = 'out.csv'
	if DEBUG:
		if len(sys.argv) < 2:
			print("I: No output file in argument. Using 'out.csv' ...")
		else:
			print("I: Using output file: '{}' ... ".format(sys.argv[1]))
			output_file = sys.argv[1]
	
	'''
	Phase 1
	'''
	form_dicts = []
	if DEBUG:
		print("*** (1/6) Building form_dict ...")
	for proj in PROJECTS:
		data_dict = query_data_dict(proj)
		this_proj_form_dict = build_form_dict(data_dict)
		form_dicts.append(this_proj_form_dict)
	form_dict = combine_form_dicts(form_dicts)
	Record.form_dict = form_dict



	'''
	Phase 2
	'''
	if DEBUG:
		print("*** (2/6) Building data template ...")
	# A 'data template' that will store be a template for every row the contents of every single 'row' in the final matrix
	data_template = build_data_template(form_dict)		
	Record.data_template = data_template
	

	'''
	Phase 3
	'''
	# Query for the actual data
	if DEBUG:
		print("*** (3/6) Querying projects for data records ... ")

	# Store the results for now
	proj_results = {}
	for proj in PROJECTS:
		proj_records = query_records(proj)	
		proj_results[proj] = proj_records	


	'''
	Phase 4
	'''
	if DEBUG:
		print("*** (4/6) Formatting project data records ...")
	final_data_records = []
	for proj, proj_results in proj_results.items():
		proj_data_records = format_project_records(proj, proj_results)	
		final_data_records += proj_data_records	



	'''
	Phase 5
	'''
	if DEBUG:
		print("*** (5/6) Sorting formatted data records ...")
		start = time.time()
		print("  * Sorting... ",end="")
	s = sorted(final_data_records, key=lambda x: x._master_id)
	if DEBUG:
		print("Done. ({} records sorted in {:.2f} seconds)".format(len(s), time.time() - start))

	'''
	Phase 6
	'''
	if DEBUG:
		print("*** (6/6) Writing result to '{}'...".format(output_file))	
		start = time.time()	
		print("  * Writing to file... ", end="")

	with open(output_file, 'w') as f:
		o_f = csv.writer(f)
		# write the first line

		# get_labels
		label_order = build_order_of_cols(data_template)
		# write the labels...
		# write_labels()
		pure_labels = [form_key[1] for form_key in label_order]
		pure_labels = ['master_id', 'date', 'proj_id'] + pure_labels
		o_f.writerow(pure_labels)
		
		for record in s:
			this_row = record.data_to_list(label_order)
			o_f.writerow(this_row)
	if DEBUG:
		print("Done. ({} records written in {:.2f} seconds)".format(len(s), time.time() - start))

	
if __name__ == '__main__':
	main()

