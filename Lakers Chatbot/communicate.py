import flask

if __name__ == '__main__':
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True


    @app.route('/', methods=['GET'])
    def home():
            return input()


app.run()