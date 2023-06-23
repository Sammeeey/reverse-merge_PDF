#!/usr/bin/env python
from wsgiref.handlers import CGIHandler
from flaskapp import create_app

app = create_app()
CGIHandler().run(app)