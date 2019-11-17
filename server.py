from logging import getLogger
from logging import basicConfig as log_base_config
from logging import INFO as log_level_INFO

from flask import Flask

from Routes.Constitution.constitution import bp_constitution
from Routes.Penal.penal import bp_penal


VERSION = "v1"


# Flask Configration
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# Logging Configration
formatter = "%(asctime)s [%(levelname)s] in %(pathname)s %(lineno)d: %(message)s"
log_base_config(level=log_level_INFO, format=formatter)

# Make Logger
logger = getLogger(__name__)

# Set Routing
app.register_blueprint(bp_constitution, url_prefix=f"/{VERSION}/constitution")
app.register_blueprint(bp_penal, url_prefix=f"/{VERSION}/penal")


def main():
    app.run()


if __name__ == "__main__":
    main()
