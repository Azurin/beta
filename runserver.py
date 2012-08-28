#!/usr/bin/env python
from controller import app
from model import createDB


# Create database if needed
createDB();

# Run the application
app.run('172.17.57.167', 5000, debug=True)

