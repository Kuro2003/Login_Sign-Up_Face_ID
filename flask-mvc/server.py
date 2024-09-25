#Flask MVC

__author__ = "Vo Hoai Viet"
__version__ = "1.0"
__email__ = "vhviet@fit.hcmus.edu.vn"

from app import app

if __name__ == '__main__':
    app.run(host="localhost", port=8800, debug=True)
