from app import app
from flask import render_template, request, redirect, url_for
from app import db
from app.forms import CreateRecipeForm, SearchForm
from app.models import (
    Recipe, Ingredient, RecipeCategory, RecipeDietaryTag, RecipeAllergen,
    Category, DietaryTag, Allergen, MeasurementUnit
)


# ── Dashboard ──────────────────────────────────────────────────────────────────
@app.route('/')
def dashboard():
    recipes = Recipe.query.order_by(Recipe.dateCreated.desc()).all()
    return render_template('dashboard.html', recipes=recipes)

# ── Create Recipe ──────────────────────────────────────────────────────────────
@app.route('/recipe/create', methods=['GET', 'POST'])
def create_recipe():
    form = CreateRecipeForm()

    form.category_id.choices  = [(0, '-- Select Category --')] + [
        (c.id, c.name) for c in Category.query.all()
    ]
    form.dietary_tags.choices = [(t.id, t.name) for t in DietaryTag.query.all()]
    form.allergens.choices    = [(a.id, a.name) for a in Allergen.query.all()]
    units = MeasurementUnit.query.filter_by(isActive=True).all()

    if form.validate_on_submit():

        # Collect ingredients
        ing_names = request.form.getlist('ing_name')
        ing_qtys  = request.form.getlist('ing_quantity')
        ing_units = request.form.getlist('ing_unit')

        # Check at least one ingredient exists
        has_ingredient = any(n.strip() for n in ing_names)
        if not has_ingredient:
            return render_template('recipe.html', form=form, units=units,
                                   errors=['At least one ingredient is required.'])

        # Check for duplicate title
        duplicate = Recipe.query.filter_by(authorID=1, title=form.title.data).first()
        if duplicate:
            return render_template('recipe.html', form=form, units=units,
                                   errors=['You already have a recipe with this name.'])

        # All checks passed — save to database
        new_recipe = Recipe(
            authorID     = 1,
            title        = form.title.data,
            description  = form.description.data  or None,
            instructions = form.instructions.data,
            forkedFrom   = None,
            baseServings = form.baseServings.data,
            prepTime     = form.prepTime.data      or None,
            cookTime     = form.cookTime.data      or None,
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
                recipeID     = new_recipe.id,
                dietaryTagID = tag_id
            ))

        # Save allergens
        for allergen_id in form.allergens.data:
            db.session.add(RecipeAllergen(
                recipeID   = new_recipe.id,
                allergenID = allergen_id
            ))

        db.session.commit()
        return redirect(url_for('dashboard'))

    # GET or validation failed — show the form
    return render_template('recipe.html', form=form, units=units, errors=[])

# New View recipes

@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    # Fetch the recipe or return 404 if not found
    recipe = Recipe.query.get_or_404(recipe_id)

    # Fetch related data
    ingredients   = Ingredient.query.filter_by(recipeID=recipe_id).all()
    categories    = RecipeCategory.query.filter_by(recipeID=recipe_id).all()
    dietary_tags  = RecipeDietaryTag.query.filter_by(recipeID=recipe_id).all()
    allergens     = RecipeAllergen.query.filter_by(recipeID=recipe_id).all()

    return render_template('view_recipe.html',
                           recipe       = recipe,
                           ingredients  = ingredients,
                           categories   = categories,
                           dietary_tags = dietary_tags,
                           allergens    = allergens)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    results = set()  # Use a set to avoid duplicates

    if form.validate_on_submit():
        query = form.query.data.strip().lower()

        # 1️⃣ Search by title
        title_matches = Recipe.query.filter(Recipe.title.ilike(f"%{query}%")).all()
        results.update(title_matches)

        # 2️⃣ Search by description
        desc_matches = Recipe.query.filter(Recipe.description.ilike(f"%{query}%")).all()
        results.update(desc_matches)

        # 3️⃣ Search by ingredients
        ingredient_matches = (
            db.session.query(Recipe)
            .join(Ingredient)
            .filter(Ingredient.name.ilike(f"%{query}%"))
            .all()
        )
        results.update(ingredient_matches)

        # 4️⃣ Search by dietary tags
        tag_matches = (
            db.session.query(Recipe)
            .join(RecipeDietaryTag)
            .join(DietaryTag)
            .filter(DietaryTag.name.ilike(f"%{query}%"))
            .all()
        )
        results.update(tag_matches)

        # 5️⃣ Search by allergens
        allergen_matches = (
            db.session.query(Recipe)
            .join(RecipeAllergen)
            .join(Allergen)
            .filter(Allergen.name.ilike(f"%{query}%"))
            .all()
        )
        results.update(allergen_matches)

    return render_template('search.html', form=form, results=list(results))

"""
@app.route('/recipe/create', methods=['GET', 'POST'])
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
        return render_template('recipe.html', form=form, units=units)

    # ── POST — process the submission ──────────────────────────────────────────
    if request.method == 'POST':
    ingredient_names = request.form.getlist('ingredient_name')
    ingredient_quantity  = request.form.getlist('ingredient_quantity')
    ingredient_units = request.form.getlist('ingredient_unit')

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
            forkedFrom   = None,     # hardcoded for demo — not a fork
            baseServings = form.baseServings.data,
            prepTime     = form.prepTime.data      or None,
            cookTime     = form.cookTime.data      or None,
        )
        db.session.add(new_recipe)
        db.session.flush()

        # Save ingredients
        for name, quantity, unit_id in zip(ingredient_names, ingredient_quantity, ingredient_units):
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
        return redirect(url_for('app.dashboard')) #says main instead of app

    # Collect all errors
    errors = []
    for field, messages in form.errors.items():
        for msg in messages:
            errors.append(msg)
    if not has_ingredient:
        errors.append('At least one ingredient is required.')
    if duplicate:
        errors.append('You already have a recipe with this name.')

    return render_template('recipe.html',
                           form=form, units=units, errors=errors)
"""
#Old above
        
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


#import sys

#DeleteForm, SearchForm,
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

"""
