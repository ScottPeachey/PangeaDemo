# -*- coding: utf-8 -*-
import os

SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(16))

# configure flask app for local development
ENV = "development"
