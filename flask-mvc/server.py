#Flask MVC

# __author__ = "Vo Hoai Viet"
# __version__ = "1.0"
# __email__ = "vhviet@fit.hcmus.edu.vn"

# from app import app

# --------
from app import create_app
from flask import render_template
from app.config.AppConfig import Config

app = create_app()

#route index
@app.route('/', methods = ['GET'])
def index():
    data = {
        "title": "Hello World",
        "body": "Flask simple MVC"
    }
    return render_template('index.html.j2', data = data)


if __name__ == '__main__':
    app.run(host="localhost", port=Config.PORT, debug=True)
