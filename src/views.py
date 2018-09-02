from src import app

@app.route('/')
def index():
    return '<h1>Index page</h1>'