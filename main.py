from website import create_app

app = create_app()


# Make the debug False in the production
if __name__ == '__main__':
	app.run(debug=True)
