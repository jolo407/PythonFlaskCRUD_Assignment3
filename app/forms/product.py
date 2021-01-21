#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""Product Form"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    name = StringField("What is the name of the product?", validators=[DataRequired()])
    price = StringField("What is the price of the product?", validators=[DataRequired()])
    description = StringField("What is the description of the product", validators=[DataRequired()])
    category = StringField("What is the category of the product", validators=[DataRequired()])
    quantity = StringField("What is the quantity of the product?", validators=[DataRequired()])
    unique_tag = StringField("What is the unique_tag of the product?", validators=[DataRequired()])
    submit = SubmitField("Submit")