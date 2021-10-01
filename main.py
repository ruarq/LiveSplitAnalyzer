from plotly.missing_ipywidgets import FigureWidget
import LiveSplit as ls

# plotly
import plotly.express as px

# dash
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import base64

#########################################################################################################

splits = {}

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
splits = {}

# create the app
app = dash.Dash('LiveSplit Analyzer')
app.layout = html.Div(
	children=[
		html.H1(children='LiveSplit Analyzer',
			style={
				'textAlign': 'center'
			}
		),
		dcc.Upload(id='upload-split-file',
			children=html.Div([
				'Drag and Drop or ',
				html.A('Select Files')
			]),
			style={
				'height': '60px',
				'lineHeight': '60px',
				'borderWidth': '1px',
				'borderStyle': 'dashed',
				'borderRadius': '5px',
				'textAlign': 'center',
				'margin': '10px',
			},
		),
		dcc.Dropdown(
			options=[
				{'label': 'Real Time', 'value': 'time_real'},
				{'label': 'Game Time', 'value': 'time_game'}
			],
			value='time_real',
			id='timing-mode-dropdown'
		),
		dcc.Graph(id='finished-attempts', figure=fig_finished_attempts(splits, 'time_real'))
	]
)

@app.callback(
	Output('finished-attempts', 'figure'),
	Input('upload-split-file', 'contents'),
	Input('timing-mode-dropdown', 'value'))
def update_finished_attempts(content, timing_mode):
	if content is not None:
		_, content_string = content.split(',')
		global splits
		splits = ls.from_str(base64.b64decode(content_string))

	fig = fig_finished_attempts(splits, timing_mode)
	fig.update_layout(transition_duration=500)
	return fig

if __name__ == '__main__':
	app.run_server(debug=True)