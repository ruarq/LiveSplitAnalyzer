import LiveSplit as ls
import plotly.express as px

def main():
	splits = ls.from_file('splits.lss')

	finished_attempts = [attempt for attempt in splits['attempts'] if 'realtime' in attempt]
	fig = px.line(finished_attempts, x="id", y="realtime", title='finished runs over time',
		labels={
			'id': 'attempt'
		})
	fig.show()

if __name__ == '__main__':
	main()
