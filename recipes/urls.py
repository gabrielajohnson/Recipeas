from django.urls import path

from . import views

urlpatterns = [
    # Login, logout and register paths
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # Add, edit and view recipe paths
    path("addrecipe", views.add_recipe, name="addrecipe"),
    path("editrecipe/<int:recipe_id>", views.edit_recipe, name="editrecipe"),
    path("recipe/<int:recipe_id>", views.view_recipe, name="viewrecipe"),

    # Add comment and review paths
    path("addcomment/<int:recipe_id>", views.add_comment, name="addcomment"),
    path("addreview/<int:recipe_id>", views.add_review, name="addreview"),

    # View Category page and get category paths
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.get_category, name="getcategory"),
    path("category", views.get_category, name="getcategory"),

    # Create and edit recipe list url paths
    path("createlist", views.create_list, name="createlist"),
    path("editlist/<int:recipeList_id>", views.edit_list, name="editlist"),
    path("editlist/<int:recipeList_id>/status", views.get_list_status, name="getliststatus"),
    path("addtolist/<int:recipe_id>", views.add_to_list, name="addtolist"),

    # View Profile and Recipe List paths
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("recipelist/<int:list_id>", views.view_recipe_list, name="viewrecipelist")
]
