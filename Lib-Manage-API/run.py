import sys
import config
sys.dont_write_bytecode = True

from flask import Flask
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


from route.admin_route import *
from route.user_route import *
from route.home import *

if __name__ == '__main__':
    # print app.url_map
    app.run(port=config.port, host=config.host)