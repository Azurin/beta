#!/usr/bin/env python
from controller import app
from model import createDB


# Create database if needed
createDB();

# Run the application
app.run(debug=True)

