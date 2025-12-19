from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager
import cloudinary
app=Flask(__name__)
app.secret_key="ashduefj!#a"
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:hao7895123@localhost/saledb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 3

cloudinary.config( cloud_name='dohfiqnqc',
                   api_key='172216865175389',
                   api_secret='WPhBg0xDguStQDIuDp799-4hlx8')

db = SQLAlchemy(app)
login = LoginManager(app)