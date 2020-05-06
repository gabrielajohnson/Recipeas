from django.contrib import admin

# Register your models here.
from .models import User, Category, Recipe, Review, RecipeList

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(RecipeList)