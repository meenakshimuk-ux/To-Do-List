from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

import models  # noqa: E402
import routes  # noqa: E402
