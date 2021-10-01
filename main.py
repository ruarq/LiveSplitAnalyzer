from datetime import datetime
from dash.dash_table.DataTable import DataTable
from plotly.missing_ipywidgets import FigureWidget
import LiveSplit as ls

# plotly
import plotly.express as px

# dash
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import base64

#########################################################################################################

splits = {}

#########################################################################################################

def format_time(time: datetime) -> str:
	return time.strftime('%H:%M:%S')

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
		html.Div(
			children=[
				html.Div(
					style={'display': 'inline-block'},
					children=[
						dcc.Graph(id='finished-attempts')
					]
				),
				html.Div(
					style={'display': 'inline-block'},
					children=[
						dash_table.DataTable(
							id='splits-table',
							columns=[
								{'name': '#',			'id': 'segment'		},
								{'name': 'Name',		'id': 'name'		},
								{'name': 'Duration',	'id': 'duration'	},
								{'name': 'Finished At',	'id': 'finished'	}
							]
						)
					]
				)
			]
		)
	]
)

@app.callback(
	Output('finished-attempts', 'figure'),
	Output('splits-table', 'data'),
	Input('upload-split-file', 'contents'),
	Input('timing-mode-dropdown', 'value'))
def update_finished_attempts(content, timing_mode):
	global splits

	# finished-attempts
	if content is not None:
		_, content_string = content.split(',')
		splits = ls.from_str(base64.b64decode(content_string))

	if timing_mode is not None:
		fig = fig_finished_attempts(splits, timing_mode)
	
	fig.update_layout(transition_duration=500)

	# splits-table
	data = None
	if 'segments' in splits:
		data = []
		i = 1
		for segment in splits['segments']:
			data.append(
				{
					'segment': str(i),
					'name': segment['name'],
					'duration': format_time(segment['best_time']['time_real']),
					'finished': format_time(segment['split_times'][0]['time_real'])
				}
			)
			i += 1

	return fig, data

if __name__ == '__main__':
	app.run_server(debug=True)