from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class NewShoppingListForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

    submit = SubmitField('Create')


class EditShoppingListForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

    submit = SubmitField('Edit')


class AddProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    gtin = StringField('GTin')
    amount = IntegerField('Amount', default='1', validators=[NumberRange(min=1)])

    submit = SubmitField('Add')


class EditProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    amount = IntegerField('Amount', default='1', validators=[NumberRange(min=1)])

    submit = SubmitField('Edit')
