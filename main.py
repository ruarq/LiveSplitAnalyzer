from plotly.missing_ipywidgets import FigureWidget
import LiveSplit as ls

# TODO(ruarq): remove when debugging finished
import json

# plotly
import plotly.express as px

# dash
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
#########################################################################################################

def dash_split_table(splits: dict) -> dcc.Graph:
	return None

#########################################################################################################

def fig_finished_attempts(splits: dict, timing_mode: str) -> FigureWidget:
	finished_attempts = ls.finished_attempts(splits, timing_mode)

	if len(finished_attempts) == 0:
		return px.line()

	fig = px.line(finished_attempts, x='id', y='time_real', title='Run Duration over Time',
		labels={
			'id': 'Attempt',
			timing_mode: 'Duration'
		})

	return fig

#########################################################################################################

# create the figure
splits = ls.from_file('celeste.lss')

# create the app
app = dash.Dash('LiveSplit Analyzer')
app.layout = html.Div(children=[
	html.H1(children='LiveSplit Analyzer'),
	dcc.Dropdown(
		options=[
			{'label': 'Real Time', 'value': 'time_real'},
			{'label': 'Game Time', 'value': 'time_game'}
		],
		value='time_real',
		id='time_dropdown'
	),
	dcc.Graph(id='finished_attempts', figure=fig_finished_attempts(splits, 'time_real'))
])

@app.callback(
	Output(component_id='finished_attempts', component_property='figure'),
	Input(component_id='time_dropdown', component_property='value'))
def update_finished_attempts(timing_mode):
	fig = fig_finished_attempts(splits, timing_mode)
	fig.update_layout(transition_duration=500)
	return fig


if __name__ == '__main__':
	app.run_server(debug=True)