#!/usr/bin/env python
from controller import app
from model import createDB
import config


if __name__ == '__main__':
	# Create database if needed
	createDB();

	# Run the application
	app.run(config.app.webserver.host, config.app.webserver.port, debug=True)

