from config.settings import app

@app.route('/')
def hello_world():
    return "<p>Go to /graphql to access API's !</p>"

if __name__ == '__main__':
    app.run()