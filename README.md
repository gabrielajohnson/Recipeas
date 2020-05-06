Project: Recipeas

Description: This app allows users to create an account, post their own recipes, and view the recipes of others by category such as 3 ingredient recipes or healthy recipes.  They can also view, comment and give a rating and review other recipes, along with creating favorites lists and can add recipes to these lists.

Files:

-recipes:

 -urls.py: Contains all url paths for views functions
 -util.py: Formats recipe form field values such as preptime, cooktime, steps and ingredients. Also includes functions that get total recipe time and total ingredients
 -views.py: All views functions and forms such as: Add, edit and view recipes functions and forms. Add reviews and comments to recipes, as well as forms. Create recipe list and add recipes to it. View recipes by category. View profile of user.
 -models.py: User, Category, Recipe, Review, Comment, RecipeList and validate duration function

-templatetags:

 -recipes_extras.py: Has filter that converts every line in ingredients and steps into list items

-static:

-recipes:
 -style.css: Contains styling for page, including CSS for Star Rating Visual in the "Add Review" Modal and other pages.
 -script.js: Contains scripting that opens modal for "Add Review","View Reviews","Add to List". Also allows user to edit recipe list in place
     
-images:
 -recipe images are saved here

-templates:

-recipes:
-add_recipe.html: RecipeForm is generated here to add recipe to website
-category.html: List of categories is generated here, user can click on a category and it generates a list of matching recipes
-edit_recipe.html: RecipeForm is generated here to edit recipe currently on site
-index.html: Displays all recipes, newest first
-layout.html: Contains html for navigation menu
-new_list.html: Generates form to create new recipelist, and displays cards with recipeList titles and links
-profile.html: Generates recipes, recipelists and reviews created by the chosen user
-recipe_list: Generates all recipes in chosen list
-recipe.html: Generates all information in recipe
-login.html: Login page for user
-register.html: Register account page for user


