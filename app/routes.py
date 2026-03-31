from app import app
from flask import render_template, request, redirect, url_for
from app import db
from app.forms import  DeleteForm, SearchForm, CreateRecipeForm
from app.models import (
    Recipe, Ingredient, RecipeCategory, RecipeDietaryTag, RecipeAllergen,
    Category, DietaryTag, Allergen, MeasurementUnit
)


"""@app.route('/create_recipe', methods=['GET', 'POST'])
def creat_recipe():
    form = CreateRecipeForm()
    if form.validate_on_submit():"""

"""
from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import (
    Recipe, Ingredient, RecipeCategory, RecipeDietaryTag, RecipeAllergen,
    Category, DietaryTag, Allergen, MeasurementUnit
)
from app.forms import CreateRecipeForm

main = Blueprint('main', __name__)

"""
"""
# ── Dashboard ──────────────────────────────────────────────────────────────────
@main.route('/')
@main.route('/dashboard')
def dashboard():
    recipes = Recipe.query.order_by(Recipe.dateCreated.desc()).all()
    return render_template('dashboard.html', recipes=recipes)
"""
# ── Create Recipe ──────────────────────────────────────────────────────────────
@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():
    form = CreateRecipeForm()

    # Populate dropdown choices from the database
    form.category_id.choices  = [(0, '-- Select Category --')] + [
        (c.id, c.name) for c in Category.query.all()
    ]
    form.dietary_tags.choices = [(t.id, t.name) for t in DietaryTag.query.all()]
    form.allergens.choices    = [(a.id, a.name) for a in Allergen.query.all()]
    units = MeasurementUnit.query.filter_by(isActive=True).all()

    # ── GET — serve the empty form ─────────────────────────────────────────────
    if request.method == 'GET':
        return render_template('create_recipe.html', form=form, units=units)

    # ── POST — process the submission ──────────────────────────────────────────
    ingredient_names = request.form.getlist('ing_name')
    ingredient_quantitys  = request.form.getlist('ing_quantity')
    ingredient_units = request.form.getlist('ing_unit')

    has_ingredient = any(n.strip() for n in ingredient_names)
    duplicate      = Recipe.query.filter_by(
                        authorID=1, title=form.title.data
                     ).first()

    if form.validate_on_submit() and has_ingredient and not duplicate:

        new_recipe = Recipe(
            authorID     = 1,  # placeholder until auth is implemented
            title        = form.title.data,
            description  = form.description.data  or None,
            instructions = form.instructions.data,
            baseServings = form.baseServings.data,
            prepTime     = form.prepTime.data      or None,
            cookTime     = form.cookTime.data      or None,
            isPublic     = form.isPublic.data,
        )
        db.session.add(new_recipe)
        db.session.flush()

        # Save ingredients
        for name, quantity, unit_id in zip(ing_names, ing_qtys, ing_units):
            name = name.strip()
            if not name:
                continue
            db.session.add(Ingredient(
                recipeID = new_recipe.id,
                unitID   = int(unit_id) if unit_id else 1,
                name     = name,
                quantity = float(quantity) if quantity else 0.0
            ))

        # Save category
        if form.category_id.data and form.category_id.data != 0:
            db.session.add(RecipeCategory(
                recipeID   = new_recipe.id,
                categoryID = form.category_id.data
            ))

        # Save dietary tags
        for tag_id in form.dietary_tags.data:
            db.session.add(RecipeDietaryTag(
                recipeID=new_recipe.id, dietaryTagID=tag_id
            ))

        # Save allergens
        for allergen_id in form.allergens.data:
            db.session.add(RecipeAllergen(
                recipeID=new_recipe.id, allergenID=allergen_id
            ))

        db.session.commit()
        return redirect(url_for('main.dashboard'))

    # Collect all errors
    errors = []
    for field, messages in form.errors.items():
        for msg in messages:
            errors.append(msg)
    if not has_ingredient:
        errors.append('At least one ingredient is required.')
    if duplicate:
        errors.append('You already have a recipe with this name.')

    return render_template('create_recipe.html',
                           form=form, units=units, errors=errors)
        
"""
@app.route('/population', methods=['GET', 'POST'])
def population():
    form = PopulationForm()
    if form.validate_on_submit():
        newCity = City(form.city.data, form.country.data, form.population.data)
        if newCity not in cities:
            cities.append(newCity)
            form.city.data = ''
            form.country.data=''
            form.population.data= ''
            return redirect(url_for('population'))
    return render_template('population.html', form=form)
    
    
@app.route('/view_all')
def view():
    return render_template('view_cities.html', cities=cities)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        foundCity = form.city.data
        if foundCity in cities:
            cities.pop(foundCity)
            return redirect(url_for('view'))
    return render_template('delete.html', cities=cities, form=form)

    
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    cityName = None
    if form.validate_on_submit():
        searchedCity = form.city.data.strip() 
        for city in cities:
            if city.name.lower() ==searchedCity.lower():
                cityName = city
                break
    return render_template('search.html', form=form, city=cityName)         
"""
