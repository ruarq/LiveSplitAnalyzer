import LiveSplit as ls

# TODO(ruarq): remove when debugging finished
import json

# plotly
import plotly.express as px

# dash
import dash
from dash import dcc
from dash import html
import pandas as pd

#########################################################################################################

def dash_split_table(splits: dict) -> dcc.Graph:
	return None

#########################################################################################################

def dash_finished_attempts(splits: dict) -> dcc.Graph:
	finished_attempts = ls.finished_attempts(splits, 'time_real')

	if len(finished_attempts) == 0:
		return html.P(children='No finished attempts')

	fig = px.line(finished_attempts, x='id', y='time_real', title='Run Duration over Time',
		labels={
			'id': 'Attempt',
			'realtime': 'Duration'
		})

	return dcc.Graph(id='Finished Attempts', figure=fig)

#########################################################################################################

def dash_segment_history(segment: dict) -> dcc.Graph:
	segment_history = segment['segment_history']

	fig = px.line(segment_history, x='id', y='time_real', title='Segment Duration over Time',
		labels={
			'id': 'Attempt',
			'realtime': 'Duration'
		})

	return dcc.Graph(id='Finished Attempts', figure=fig)

#########################################################################################################

# create the figure
splits = ls.from_file('minecraft.lss')

# create the app
app = dash.Dash('LiveSplit Analyzer')
app.layout = html.Div(children=[
	html.H1(children='LiveSplit Analyzer'),
	dash_finished_attempts(splits)
])

if __name__ == '__main__':
	app.run_server(debug=True)