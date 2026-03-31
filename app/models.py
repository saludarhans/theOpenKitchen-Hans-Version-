from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id          = db.Column(db.Integer,     primary_key=True)
    firstName   = db.Column(db.String(50),  nullable=False) #missing unique attribute
    lastName    = db.Column(db.String(50),  nullable=False)
    email       = db.Column(db.String(100), nullable=False, unique=True)
    password    = db.Column(db.String(255), nullable=False)
    role        = db.Column(db.String(20),  nullable=False, default='contributor')
    isActive    = db.Column(db.Boolean,     default=True)
    dateCreated = db.Column(db.DateTime,    default=datetime.now)

    recipes = db.relationship('Recipe', backref='author', lazy=True)


class MeasurementUnit(db.Model):
    __tablename__ = 'measurement_units'

    id           = db.Column(db.Integer,    primary_key=True)
    name         = db.Column(db.String(32), nullable=False)
    abbreviation = db.Column(db.String(32), nullable=False)
    system       = db.Column(db.String(32), nullable=False)
    isActive     = db.Column(db.Boolean,    default=True)

    ingredients = db.relationship('Ingredient', backref='unit', lazy=True)


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id           = db.Column(db.Integer,     primary_key=True)
    authorID     = db.Column(db.Integer,     db.ForeignKey('users.id'),    nullable=False)
    title        = db.Column(db.String(150), nullable=False)
    description  = db.Column(db.Text,        nullable=True)
    instructions = db.Column(db.Text,        nullable=False)
    forkedFrom   = db.Column(db.Integer,     db.ForeignKey('recipes.id'),  nullable=True)
    servings     = db.Column(db.Integer,     nullable=True)
    prepTime     = db.Column(db.Integer,     nullable=True)
    cookTime     = db.Column(db.Integer,     nullable=True)
    isPublic     = db.Column(db.Boolean,     default=True) #check to remove
    dateCreated  = db.Column(db.DateTime,    default=datetime.now)

    ingredients   = db.relationship('Ingredient',       backref='recipe', lazy=True, cascade='all, delete-orphan')
    categories    = db.relationship('RecipeCategory',   backref='recipe', lazy=True, cascade='all, delete-orphan')
    dietary_tags  = db.relationship('RecipeDietaryTag', backref='recipe', lazy=True, cascade='all, delete-orphan')
    allergens     = db.relationship('RecipeAllergen',   backref='recipe', lazy=True, cascade='all, delete-orphan')


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id       = db.Column(db.Integer,    primary_key=True)
    recipeID = db.Column(db.Integer,    db.ForeignKey('recipes.id'),          nullable=False)
    unitID   = db.Column(db.Integer,    db.ForeignKey('measurement_units.id'), nullable=False)
    name     = db.Column(db.String(32), nullable=False)
    quantity = db.Column(db.Float,      nullable=False)


class Category(db.Model):
    __tablename__ = 'categories'

    id   = db.Column(db.Integer,    primary_key=True)
    name = db.Column(db.String(32), nullable=False)


class RecipeCategory(db.Model):
    __tablename__ = 'recipe_categories'

    id         = db.Column(db.Integer, primary_key=True)
    recipeID   = db.Column(db.Integer, db.ForeignKey('recipes.id'),   nullable=False)
    categoryID = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)


class Allergen(db.Model):
    __tablename__ = 'allergens'

    id   = db.Column(db.Integer,    primary_key=True)
    name = db.Column(db.String(32), nullable=False)


class RecipeAllergen(db.Model):
    __tablename__ = 'recipe_allergens'

    id         = db.Column(db.Integer, primary_key=True)
    recipeID   = db.Column(db.Integer, db.ForeignKey('recipes.id'),   nullable=False)
    allergenID = db.Column(db.Integer, db.ForeignKey('allergens.id'), nullable=False)


class DietaryTag(db.Model):
    __tablename__ = 'dietary_tags'

    id   = db.Column(db.Integer,    primary_key=True)
    name = db.Column(db.String(32), nullable=False)


class RecipeDietaryTag(db.Model):
    __tablename__ = 'recipe_dietary_tags'

    id           = db.Column(db.Integer, primary_key=True)
    recipeID     = db.Column(db.Integer, db.ForeignKey('recipes.id'),     nullable=False)
    dietaryTagID = db.Column(db.Integer, db.ForeignKey('dietary_tags.id'), nullable=False)
