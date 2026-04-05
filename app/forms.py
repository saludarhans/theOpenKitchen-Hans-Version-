from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,SelectField, SelectMultipleField, TextAreaField, BooleanField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange
#import sys

class IngredientForm(FlaskForm):
    ingredient_name     = StringField('Ingredient Name', validators=[DataRequired()])
    ingredien_quantity = StringField('Quantity',         validators=[Optional()]) #named ing_ before
    ingredien_unit     = SelectField('Unit', coerce=int, validators=[DataRequired()],
                               choices=[])

class CreateRecipeForm(FlaskForm):
    # Required fields
    title        = StringField('Recipe Name',
                        validators=[DataRequired(message='Recipe name is required.')])
    instructions = TextAreaField('Recipe Directions',
                        validators=[DataRequired(message='Recipe directions are required.')])
    baseServings = IntegerField('Base Servings',
                            validators=[
                                DataRequired(message='Base serving size is required.'),
                                NumberRange(min=1, message='Servings must be at least 1.')
                            ])
    description  = TextAreaField('Description',   validators=[Optional()])
    servings     = IntegerField('Servings',        validators=[Optional(),
                        NumberRange(min=1, message='Servings must be a positive number.')])
    prepTime     = IntegerField('Prep Time',       validators=[Optional(),
                        NumberRange(min=0, message='Prep time must be 0 or more.')])
    cookTime     = IntegerField('Cook Time',       validators=[DataRequired(),
                        NumberRange(min=0, message='Cook time must be 0 or more.')])
    # Optional fields
    category_id  = SelectField('Category', coerce=int, validators=[Optional()],
                        choices=[])
    dietary_tags = SelectMultipleField('Dietary Tags', coerce=int,
                        validators=[Optional()], choices=[])
    allergens    = SelectMultipleField('Allergens',    coerce=int,
                        validators=[Optional()], choices=[])
    isPublic     = BooleanField('Make this recipe public', default=True)#Think about this one if it should be implemented

#class SearchForm(FlaskForm):
"""
class PopulationForm(FlaskForm):
    city = StringField('City:', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    population = IntegerField('Population: ', validators=[DataRequired()])
    submit = SubmitField('save')

class DeleteForm(FlaskForm):
    city = StringField('City:', validators=[DataRequired()])
    submit = SubmitField('Delete')

class SearchForm(FlaskForm):
    city = StringField('City:', validators=[DataRequired()])
    submit = SubmitField('Search')
"""
