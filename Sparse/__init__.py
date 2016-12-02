"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import Sparse.routes
#from raven.contrib.flask import Sentry
#sentry = Sentry(app, dsn='http://9594c0d2f78142a597dbf722dbe768b4:605afabb68e249208549927f07f47340@13.76.101.247:9000/10')