#!/usr/bin/env python
import os


import config


def main():
	if os.geteuid() != 0:
		print "Script must be run as root."
		return

	cmd = '''sudo -u postgres psql -c "CREATE USER %s WITH PASSWORD '%s';"''' % (config.app.db.username, config.app.db.password)
	os.system(cmd)

	cmd = '''sudo -u postgres createdb %s -O %s''' % (config.app.db.name, config.app.db.username)
	os.system(cmd)


if __name__ == '__main__':
	main()

