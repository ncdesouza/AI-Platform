from flask_sqlalchemy import SQLAlchemy
from crunch import CramServer
from flask import Flask, render_template, request

app = Flask(__name__)
db = SQLAlchemy(app)


