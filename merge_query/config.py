
'''
config.py

This file contains the configuration parameters to access the RedCap API to do more complex data manipulation for theYassaLab data.

To use this you need both the API_URL, and the TOKENS for each project you have access to.
'''

# Set this to false if you do not want to see any print statements about the progress
DEBUG = True


PROJECTS = [
	"dep_ro1_test",
	"adrc_project_1"
]


# The API URL for Yassa UCI Mind 
API_URL = 'http://myapi.uci.edu'

# Tokens for each individual Project for RedCap.
# Each token belongs to a redcap user and a redcap project
# In order to use this script, you must put in YOUR token and ONLY YOUR TOKEN
# You can request your token from Dan or Myra
TOKENS = {
	'master'        : 'ABCD1234ABCD1234ABCD1234ABCD1234',
	'dep_ro1_test'  : 'ABCD1234ABCD1234ABCD1234ABCD1234',
	'survey'        : 'ABCD1234ABCD1234ABCD1234ABCD1234',
	'adrc_project_1': 'ABCD1234ABCD1234ABCD1234ABCD1234',
	'nia_ro1'       : 'ABCD1234ABCD1234ABCD1234ABCD1234'
}
