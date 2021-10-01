# Documentation
## Structure of the dictionaries parsed from LSS/XML files
The `LiveSplit.from_...` functions return a `dict` that has about the same structure as the actual *LSS*/*XML* file 
**Assuming you store the result of a** `LiveSplit.from_...` **function a variable called** `splits`, you can query the
- *GameName* with `splits['game']`
- *CategoryName* with `splits['category']`
- *Metadata* with `splits['meta']`
	- *Platform* with `splits['meta']['platform']`
	- *Platform.usesEmulator* with `splits['meta']['uses_emulator']`
	- *Region* with `splits['meta']['region']`
	- *Variables* with `splits['meta']['variables']`
		- To get the value of a variable as string: `splits['meta']['variables']['variable_name']`
- *Offset* with `splits['offset']`
- *AttemptCount* with `splits['attempt_count']`
- *AttemptHistory* with `splits['attempts']`
	- *Attempt* with `splits['attempts'][attempt_id]`
	- *Attempt.id* with `splits['attempts'][attempt_id]['id']`
	- *Attempt.started* with `splits['attempts'][attempt_id]['started']`
	- *Attempt.isStartedSynced* with `splits['attempts'][attempt_id]['started_synced']`
	- *Attempt.ended* with `splits['attempts'][attempt_id]['ended']`
	- *Attempt.isEndedSynced* with `splits['attempts'][attempt_id]['ended_synced']`
- *Segments* with `splits['segments']`
	- *Segment* with `splits['segments']['segment_name']`
		- *SplitTimes* with `splits['segments']['segment_name']['split_times']`
			- To get the personal best split time: `splits['segments']['segment_name']['split_times']['Personal Best']`
		- *BestSegmentTime* with ``splits['segments']['segment_name']['best_time']
		- *SegmentHistory* with `splits['segments']['segment_name']['history']`
			- *Time* with `splits['segments']['segment_name']['history'][time_id]`

When getting a time in using the dictionary, you need to specify wether you want it in real time or game time.
- To get the real time of an attempt: `splits['attempts'][attempt_id]['time_real']`
- To get the game time of an attempt: `splits['attempts'][attempt_id]['time_game']`