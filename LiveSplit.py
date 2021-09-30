import xml.etree.ElementTree as xml
from datetime import datetime

def _parse_attempt(attempt: xml.Element) -> dict:
	data = {}
	data['id'] = int(attempt.get('id'))
	data['started'] = datetime.strptime(attempt.get('started'), '%m/%d/%Y %H:%M:%S')
	data['started_synced'] = (True, False)[attempt.get('isStartedSynced') == 'False']
	data['ended']  = datetime.strptime(attempt.get('ended'), '%m/%d/%Y %H:%M:%S')
	data['ended_synced'] = (True, False)[attempt.get('isEndedSynced') == 'False']

	realtime = attempt.find('RealTime')
	if realtime is not None:
		# why realtime.text[:-1]? datetime doesn't support having more than 6 digits after the '.',
		# # and since live split saves 7 digits, we have to cut one off
		data['realtime'] = datetime.strptime(realtime.text[:-1], '%H:%M:%S.%f')
	
	return data

def from_file(filename: str) -> dict:
	data = {}
	
	root = xml.parse(filename)

	# read game and category name
	data['game'] = root.find('GameName').text
	data['category'] = root.find('CategoryName').text

	# read metadata
	metadata = root.find('Metadata')
	data['meta'] = {}
	data['meta']['platform'] = metadata.find('Platform').text
	data['meta']['uses_emulator'] = (True, False)[metadata.find('Platform').get('usesEmulator') == 'False']
	data['meta']['region'] = metadata.find('Region').text
	
	# read metadata variables
	variables = metadata.find('Variables')
	data['meta']['variables'] = {}
	for variable in variables:
		data['meta']['variables'][variable.get('name')] = variable.text

	# read offset and attempt count
	data['offset'] = datetime.strptime(root.find('Offset').text, '%H:%M:%S')
	data['attempt_count'] = int(root.find('AttemptCount').text)

	# parse all attempts
	data['attempts'] = []
	attempts = root.find('AttemptHistory')
	for attempt in attempts:
		data['attempts'].append(_parse_attempt(attempt))

	return data