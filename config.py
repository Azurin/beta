
class Container: pass


app = Container()

app.db = Container()
app.webserver = Container()


app.db.username = 'major'
app.db.password = 'hello'
app.db.name     = 'beta'
app.db.host     = 'localhost'
app.db.url      = 'postgres://%s:%s@localhost/%s' % (app.db.username, app.db.password, app.db.name)


app.webserver.host = 'localhost'
app.webserver.port = 5000


