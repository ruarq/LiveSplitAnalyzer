from re import split
import xml.etree.ElementTree as xml
from datetime import datetime
import dateutil.parser

#########################################################################################################

def _parse_time(time_str: str) -> datetime:
	return dateutil.parser.parse(time_str, fuzzy=True)

#########################################################################################################

def _parse_time_element(element: xml.Element) -> dict:
	data = {}
	
	realtime = element.find('RealTime')
	gametime = element.find('GameTime')

	if realtime is not None:
		data['time_real'] = _parse_time(realtime.text)

	if gametime is not None:
		data['time_game'] = _parse_time(gametime.text)

	return data

#########################################################################################################

def _parse_attempt(attempt: xml.Element) -> dict:
	data = {}
	data['id'] = int(attempt.get('id'))
	data['started'] = _parse_time(attempt.get('started'))
	data['started_synced'] = (True, False)[attempt.get('isStartedSynced') == 'False']
	data['ended']  = _parse_time(attempt.get('ended'))
	data['ended_synced'] = (True, False)[attempt.get('isEndedSynced') == 'False']
	data.update(_parse_time_element(attempt))
	
	return data

#########################################################################################################

def _parse_segment_time(segment_time: xml.Element) -> dict:
	data = {}

	data['id'] = int(segment_time.get('id'))
	data.update(_parse_time_element(segment_time))
	
	return data

#########################################################################################################

def _parse_segment(segment: xml.Element) -> dict:
	data = {}
	name = segment.find('Name').text
	data[name] = {}

	# parse split times
	data[name]['split_times'] = {}
	for split_time in segment.find('SplitTimes'):
		data[name]['split_times'].update(_parse_split_time(split_time))

	data[name]['best_time'] = _parse_time_element(segment.find('BestSegmentTime'))
	data[name]['history'] = []
	for segment_time in segment.find('SegmentHistory'):
		data[name]['history'].append(_parse_segment_time(segment_time))

	# make sure the segment history is sorted. I noticed that Live split messes the order up occasionally
	data[name]['history'].sort(key=lambda elem : elem['id'])

	return data

#########################################################################################################

def _parse_split_time(split_time: xml.Element) -> dict:
	data = {}
	name = split_time.get('name')
	data[name] = {}
	data[name].update(_parse_time_element(split_time))

	return data

#########################################################################################################

def from_str(string: str) -> dict:
	root = xml.fromstring(string)

	data = {}
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
	data['offset'] = _parse_time(root.find('Offset').text)
	data['attempt_count'] = int(root.find('AttemptCount').text)

	# parse all attempts
	data['attempts'] = []
	attempts = root.find('AttemptHistory')
	for attempt in attempts:
		data['attempts'].append(_parse_attempt(attempt))
	
	# sort the attempts by id. LiveSplit messed up the order sometimes
	data['attempts'].sort(key=lambda elem : elem['id'])

	# parse all segments
	data['segments'] = {}
	segments = root.find('Segments')
	for segment in segments:
		data['segments'].update(_parse_segment(segment))

	return data

#########################################################################################################

def from_file(filename: str) -> dict:
	return from_str(open(filename, 'r').read())

#########################################################################################################

def finished_attempts(splits: dict, timing_mode: str) -> list:
	if 'attempts' in splits:
		return [attempt for attempt in splits['attempts'] if timing_mode in attempt]
	else:
		return []