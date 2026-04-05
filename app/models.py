from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id          = db.Column(db.Integer,     primary_key=True)
    firstName   = db.Column(db.String(50),  unique=False, nullable=False)
    lastName    = db.Column(db.String(50),  unique=False, nullable=False)
    email       = db.Column(db.String(100), unique=True,  nullable=False)
    password    = db.Column(db.String(255), unique=False, nullable=False)
    role        = db.Column(db.String(20),  unique=False, nullable=False, default='contributor')
    isActive    = db.Column(db.Boolean,     unique=False, nullable=True,  default=True)
    dateCreated = db.Column(db.DateTime,    unique=False, nullable=False, default=datetime.now)

    recipes = db.relationship('Recipe', backref='author', lazy=True)

    def __repr__(self):
        return self.firstName + ' ' + self.lastName + ': ' + self.role


class MeasurementUnit(db.Model):
    __tablename__ = 'measurement_units'

    id           = db.Column(db.Integer,    primary_key=True)
    name         = db.Column(db.String(32), unique=True,  nullable=False)
    abbreviation = db.Column(db.String(32), unique=True,  nullable=False)
    system       = db.Column(db.String(32), unique=False, nullable=False)
    isActive     = db.Column(db.Boolean,    unique=False, nullable=True,  default=True)

    ingredients = db.relationship('Ingredient', backref='unit', lazy=True)

    def __repr__(self):
        return self.name + ' (' + self.abbreviation + '): ' + self.system


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id           = db.Column(db.Integer,     primary_key=True)
    authorID     = db.Column(db.Integer,     db.ForeignKey('users.id'),   unique=False, nullable=False)
    title        = db.Column(db.String(150), unique=False, nullable=False)
    description  = db.Column(db.Text,        unique=False, nullable=True)
    instructions = db.Column(db.Text,        unique=False, nullable=False)
    forkedFrom   = db.Column(db.Integer,     db.ForeignKey('recipes.id'), unique=False, nullable=True)
    baseServings = db.Column(db.Integer,     unique=False, nullable=False)
    prepTime     = db.Column(db.Integer,     unique=False, nullable=True)
    cookTime     = db.Column(db.Integer,     unique=False, nullable=True)
    #isPublic     = db.Column(db.Boolean,     unique=False, nullable=True,  default=True)
    dateCreated  = db.Column(db.DateTime,    unique=False, nullable=False, default=datetime.now)

    ingredients  = db.relationship('Ingredient',       backref='recipe', lazy=True, cascade='all, delete-orphan')
    categories   = db.relationship('RecipeCategory',   backref='recipe', lazy=True, cascade='all, delete-orphan')
    dietary_tags = db.relationship('RecipeDietaryTag', backref='recipe', lazy=True, cascade='all, delete-orphan')
    allergens    = db.relationship('RecipeAllergen',   backref='recipe', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return self.title + ': ' + str(self.baseServings) + ' servings'


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id       = db.Column(db.Integer,    primary_key=True)
    recipeID = db.Column(db.Integer,    db.ForeignKey('recipes.id'),           unique=False, nullable=False)
    unitID   = db.Column(db.Integer,    db.ForeignKey('measurement_units.id'), unique=False, nullable=False)
    name     = db.Column(db.String(32), unique=False, nullable=False)
    quantity = db.Column(db.Float,      unique=False, nullable=False)

    def __repr__(self):
        return self.name + ': ' + str(self.quantity)


class Category(db.Model):
    __tablename__ = 'categories'

    id   = db.Column(db.Integer,    primary_key=True)
    name = db.Column(db.String(32), unique=True,  nullable=False)

    def __repr__(self):
        return self.name


class RecipeCategory(db.Model):
    __tablename__ = 'recipe_categories'

    id         = db.Column(db.Integer, primary_key=True)
    recipeID   = db.Column(db.Integer, db.ForeignKey('recipes.id'),    unique=False, nullable=False)
    categoryID = db.Column(db.Integer, db.ForeignKey('categories.id'), unique=False, nullable=False)

    category = db.relationship('Category', backref='recipe_categories')

    def __repr__(self):
        return 'RecipeCategory: recipeID=' + str(self.recipeID) + ' categoryID=' + str(self.categoryID)


class Allergen(db.Model):
    __tablename__ = 'allergens'

    id   = db.Column(db.Integer,    primary_key=True)
    name = db.Column(db.String(32), unique=True,  nullable=False)

    def __repr__(self):
        return self.name

class DietaryTag(db.Model):
    __tablename__ = 'dietary_tags'

    id   = db.Column(db.Integer,    primary_key=True)
    name = db.Column(db.String(32), unique=True,  nullable=False)

    def __repr__(self):
        return self.name

class RecipeAllergen(db.Model):
    __tablename__ = 'recipe_allergens'

    id         = db.Column(db.Integer, primary_key=True)
    recipeID   = db.Column(db.Integer, db.ForeignKey('recipes.id'),    unique=False, nullable=False)
    allergenID = db.Column(db.Integer, db.ForeignKey('allergens.id'),  unique=False, nullable=False)

    allergen = db.relationship('Allergen', backref='recipe_allergens')

    def __repr__(self):
        return 'RecipeAllergen: recipeID=' + str(self.recipeID) + ' allergenID=' + str(self.allergenID)


class RecipeDietaryTag(db.Model):
    __tablename__ = 'recipe_dietary_tags'

    id           = db.Column(db.Integer, primary_key=True)
    recipeID     = db.Column(db.Integer, db.ForeignKey('recipes.id'),      unique=False, nullable=False)
    dietaryTagID = db.Column(db.Integer, db.ForeignKey('dietary_tags.id'), unique=False, nullable=False)

    dietaryTag = db.relationship('DietaryTag', backref='recipe_dietary_tags')

    def __repr__(self):
        return 'RecipeDietaryTag: recipeID=' + str(self.recipeID) + ' dietaryTagID=' + str(self.dietaryTagID)
   
class Comment(db.Model):
    __tablename__ = 'comments'

    id           = db.Column(db.Integer, primary_key=True)
    recipeID     = db.Column(db.Integer, db.ForeignKey('recipes.id'),      unique=False, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False)
    content  = db.Column(db.Text, unique=False, nullable=True)
    dateCreated = db.Column(db.DateTime,    unique=False, nullable=False, default=datetime.now)

    def __repr__(self):
        return 'Comment by userID: ' + str(self.authorID) + ': ' + self.content[:50]

class Rating(db.Model):
    __tablename__ = 'ratings'

    id           = db.Column(db.Integer, primary_key=True)
    recipeID     = db.Column(db.Integer, db.ForeignKey('recipes.id'),      unique=False, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False)
    stars  = db.Column(db.Integer,     unique=False, nullable=False)
    dateCreated = db.Column(db.DateTime,    unique=False, nullable=False, default=datetime.now)

    def __repr__(self):
        return 'Rating by userID ' + str(self.userID) + ': ' + str(self.stars) + ' stars'

class QuickTip(db.Model):
    __tablename__ = 'quick_tips'

    id           = db.Column(db.Integer, primary_key=True)
    recipeID     = db.Column(db.Integer, db.ForeignKey('recipes.id'),      unique=False, nullable=False)
    title        = db.Column(db.String(150), unique=False, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False)
    content  = db.Column(db.Text, unique=False, nullable=False)
    dateCreated = db.Column(db.DateTime,    unique=False, nullable=False, default=datetime.now)

    def __repr__(self):
        return 'Recipes: recipeID=' + str(self.recipeID) + 'Title: ' +  self.title + ': ' + self.content[:50]

# Old

"""
class RecipeAllergen(db.Model):
    __tablename__ = 'recipe_allergens'

    id         = db.Column(db.Integer, primary_key=True)
    recipeID   = db.Column(db.Integer, db.ForeignKey('recipes.id'),    unique=False, nullable=False)
    allergenID = db.Column(db.Integer, db.ForeignKey('allergens.id'),  unique=False, nullable=False)


    def __repr__(self):
        return 'RecipeAllergen: recipeID=' + str(self.recipeID) + ' allergenID=' + str(self.allergenID)


class DietaryTag(db.Model):
    __tablename__ = 'dietary_tags'

    id   = db.Column(db.Integer,    primary_key=True)
    name = db.Column(db.String(32), unique=True,  nullable=False)

    def __repr__(self):
        return self.name


class RecipeDietaryTag(db.Model):
    __tablename__ = 'recipe_dietary_tags'

    id           = db.Column(db.Integer, primary_key=True)
    recipeID     = db.Column(db.Integer, db.ForeignKey('recipes.id'),      unique=False, nullable=False)
    dietaryTagID = db.Column(db.Integer, db.ForeignKey('dietary_tags.id'), unique=False, nullable=False)

    def __repr__(self):
        return 'RecipeDietaryTag: recipeID=' + str(self.recipeID) + ' dietaryTagID=' + str(self.dietaryTagID)
"""     
