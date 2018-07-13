import json
import time
from config import *
from  urllib.request import urlopen, Request
from urllib.parse import urlencode
import urllib




def query_redcap(values: dict) -> json:
	'''
	A simple function meant to implement the HTTP query to redcap
	
	Params:
		values: a dictionary of the value pairs needed for the redcap API	
	'''

	data = urlencode(values)
	data = str.encode(data)
	req  = Request(API_URL, data=data)
	try:
		response = urlopen(req)
	except urllib.error.HTTPError as e:
		import sys
		print()
		if e.msg == "Forbidden":
			error = '''
			*****************************************************************
			Received a 'Forbidden' Error code...
			Steps you can take:
				1. Check that your API Token is valid	
				2. Check that you have permission to access this project
				3. Check your internet connection
				4. Check that you are using the correct API URL (config.py)
			*****************************************************************
			'''	
			print(error)
		else:
			raise e	
		sys.exit()
	the_page = response.read()
	the_page = the_page.decode('utf-8')
	j = json.loads(the_page)

	return j


def query_records(project_name: str) -> json:
	'''
	Query redcap for the records of this project
	Get all the records from a project
	
	Params:
		project_name: str
	Return:
		json object list of the records
	'''
	if DEBUG:
		print("  * Querying {} for data records ... ".format(project_name),end= "")
		start = time.time()
	try:
		project_token = TOKENS[project_name]
	except KeyError:
		raise KeyError("{} is not a valid project name. If this is a new project, then update the token information in config.py".format(project_name))
	values = {
	    'token': project_token,
	    'content': 'record',
	    'format': 'json',
	    'type': 'flat',
	    'returnFormat': 'json'
	}
	j = query_redcap(values)

	if DEBUG:
		print("Done. ({:.2f} seconds)".format(time.time() - start))
	return j

def query_data_dict(project_name):
	'''
	This function will query the Redcap API to get a data dictionary for a project
	Params:
		project_name: str
	Return:
		json Object: an iterable data dictionary
	'''
	if DEBUG:
		print("  * Querying {} for the data dictionary ... ".format(project_name), end="")	
		start = time.time()
	try:
		project_token = TOKENS[project_name]
	except KeyError:
		if DEBUG:
			print()
		raise KeyError("{} is not a valid project name. If this is a new project, then update the token information in config.py".format(project_name))
	values = {
	    'token': project_token,
	    'content': 'metadata',
	    'format': 'json',
	    'returnFormat': 'json'
	}
	j = query_redcap(values)
	if DEBUG:
		print("Done. ({:.2f} seconds)".format(time.time() - start))
	return j
