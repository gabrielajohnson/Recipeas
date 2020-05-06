import json
from django.shortcuts import render, redirect
from django import forms
from django.forms import ModelForm
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util

from .models import User, Category, Recipe, Comment, Review, RecipeList


# Create your views here.
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ['preptime', 'cooktime', 'ingredients_length', 'user',
                   'timestamp', 'total_time']
        widgets = {
            # Changes placeholder to give direct instruction to user
            'preptime_initial': forms.TextInput(
            attrs={'placeholder': '00:00:00 = hours:minutes:seconds'}),
            'cooktime_initial': forms.TextInput(
            attrs={'placeholder': '00:00:00 = hours:minutes:seconds'}),
            'ingredients': forms.Textarea(
            attrs={'placeholder': 'Put each ingredient on its own line'}),
            'steps': forms.Textarea(
            attrs={'placeholder': 'Put each step on its own line'})
        }
        labels = {
            'preptime_initial': "Prep Time",
            'cooktime_initial': "Cook Time",
            'inspiration':
            'Inspired by another recipe to create this one? Select it below from our list'
        }

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(custom=False)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'timestamp', 'recipe']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': '3'})
        }

        # Remove comment label
        labels = {
            'comment': ''
        }

    def __init__(self, *args, **kwargs):
        super(NewCommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class NewReviewForm(ModelForm):
    class Meta:
        model = Review
        exclude = ['user', 'timestamp', 'recipe', 'rating']
        widgets = {
            'review': forms.Textarea(attrs={'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super(NewReviewForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class NewListForm(ModelForm):
    class Meta:
        model = RecipeList
        exclude = ['user', 'timestamp', 'recipes']

    def __init__(self, *args, **kwargs):
        super(NewListForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddToListForm(forms.Form):
    name = forms.ModelChoiceField(queryset=RecipeList.objects.all())

    def __init__(self, *args, **kwargs):
        super(AddToListForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


def index(request):
    # Generate list of newest recipes
    try:
        newestRecipe = Recipe.objects.filter(public=True).order_by("-timestamp")
        return render(request, "recipes/index.html", {
            "recipes": newestRecipe
        })
    except Recipe.DoesNotExist:
        return render(request, "recipes/index.html", {})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "recipes/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "recipes/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "recipes/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "recipes/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "recipes/register.html")


@login_required
def add_recipe(request):

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            # Save times in their original format to use in the edit form later
            recipe.preptime = recipe.preptime_initial
            recipe.cooktime = recipe.cooktime_initial
            # Format times
            recipe.preptime = util.format_duration(recipe.preptime)
            recipe.cooktime = util.format_duration(recipe.cooktime)
            # Format ingredients and steps
            recipe.ingredients = util.format_steps(recipe.ingredients)
            recipe.steps = util.format_steps(recipe.steps)
            # Get total ingredients and time
            recipe.ingredients_length = util.get_ingredient_length(recipe.ingredients)
            recipe.total_time = util.get_total_time(recipe.preptime_initial, recipe.cooktime_initial)
            recipe.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse("index"))
        else:
            # If not valid, render form again
            return render(request, "recipes/add_recipe.html", {
                "form": form
            })
    else:
        # First time going to form, render new form
        return render(request, "recipes/add_recipe.html", {
            "form": RecipeForm()
        })


@login_required
def edit_recipe(request, recipe_id):
    try:
        # Check if recipe exists
        recipe = Recipe.objects.get(id=recipe_id)
        if request.user == recipe.user:
            if request.method == "POST":
                form = RecipeForm(request.POST, request.FILES, instance=recipe)
                if form.is_valid():
                    recipe = form.save(commit=False)
                    recipe.user = request.user
                    # Save times in their original format to use in the edit form later
                    recipe.preptime = recipe.preptime_initial
                    recipe.cooktime = recipe.cooktime_initial
                    # Format times
                    recipe.preptime = util.format_duration(recipe.preptime)
                    recipe.cooktime = util.format_duration(recipe.cooktime)
                    # Format ingredients and steps
                    recipe.ingredients = util.format_steps(recipe.ingredients)
                    recipe.steps = util.format_steps(recipe.steps)
                    # Get total ingredients and time
                    recipe.ingredients_length = util.get_ingredient_length(recipe.ingredients)
                    recipe.total_time = util.get_total_time(recipe.preptime_initial, recipe.cooktime_initial)
                    recipe.save()
                    form.save_m2m()
                    return redirect("index")
                else:
                    # If not valid, render form again
                    return render(request, "recipes/edit_recipe.html", {
                        "recipe_id": recipe_id,
                        "form": form
                    })
            else:
                # First time going to form, render new form
                return render(request, "recipes/edit_recipe.html", {
                    "recipe_id": recipe_id,
                    "form": RecipeForm(instance=recipe)
                })
    except Recipe.DoesNotExist:
        return JsonResponse({"error": "Recipe not found."}, status=404)


def view_recipe(request, recipe_id):
    try:
        # Check if recipe exists
        recipe = Recipe.objects.get(id=recipe_id)
        commentForm = NewCommentForm()
        reviewForm = NewReviewForm()
        addToListForm = AddToListForm()
        user = request.user
        if(user.is_authenticated):
            addToListForm.fields['name'].queryset = RecipeList.objects.filter(user=request.user).values_list('name', flat=True)
        comments = Comment.objects.filter(recipe=recipe_id).order_by("-timestamp")
        reviews = Review.objects.filter(recipe=recipe_id).order_by("-timestamp")
        starReview = 0

        # Check if there are reviews
        if(len(reviews) != 0):
            for review in reviews:
                starReview += review.rating
            # Get average of all ratings for recipes
            starReview = round(starReview/len(reviews), 2)
        else:
            starReview = 0

        return render(request, "recipes/recipe.html", {
                "recipe": recipe,
                "commentForm": commentForm,
                "comments": comments,
                "reviewForm": reviewForm,
                "reviews": reviews,
                "starReview": starReview,
                "addToListForm": addToListForm
        })
    except Recipe.DoesNotExist:
        return JsonResponse({"error": "Recipe not found."}, status=404)


@login_required
def add_comment(request, recipe_id):
    try:
        # Check if recipe exists
        recipe = Recipe.objects.get(id=recipe_id)
        if request.method == "POST":
            form = NewCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                # Save comment with user and recipe it was made on
                comment.user = request.user
                comment.recipe = recipe
                comment.save()
                return redirect("viewrecipe", recipe_id=recipe_id)
            else:
                return redirect("viewrecipe", recipe_id=recipe_id)
        else:
            return redirect("viewrecipe", recipe_id=recipe_id)
    except Recipe.DoesNotExist:
        return JsonResponse({"error": "Recipe not found."}, status=404)


@login_required
def add_review(request, recipe_id):
    try:
        # Check if recipe exists
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return JsonResponse({"error": "Recipe not found."}, status=404)

    if request.method == "POST":
        form = NewReviewForm(request.POST)
        if form.is_valid():
            # Save rating and review to recipe
            review = form.save(commit=False)
            review.user = request.user
            review.recipe = recipe
            review.rating = request.POST.get("rating")
            review.save()
            return redirect("viewrecipe", recipe_id=recipe_id)
        else:
            return redirect("viewrecipe", recipe_id=recipe_id)
    else:
        return redirect("viewrecipe", recipe_id=recipe_id)


def categories(request):
    # Generates categories in category page
    categories = Category.objects.all()
    return render(request, "recipes/category.html", {
        "categories": categories,
    })


def get_category(request, category=None):
    # Get all categories
    categories = Category.objects.all()
    currentCategory = ""
    recipes = None

    # If category was selected from mobile dropdown
    if request.method == 'POST':
        category_id = request.POST["category"]
        currentCategory = Category.objects.get(id=category_id)
    # If category was chosen on desktop
    elif category:
        currentCategory = Category.objects.get(id=category)

    if currentCategory != "":
        # For custom categories, filter by amount of ingredients and total time
        if currentCategory.category == "3 Ingredients Only":
            recipes = Recipe.objects.filter(ingredients_length=3)
        elif currentCategory.category == "Less than 10 Minutes":
            recipes = Recipe.objects.filter(total_time__lte=10)
        else:
            recipes = Recipe.objects.filter(category=currentCategory)
        # Render categories list, recipes from category, and category name
        return render(request, "recipes/category.html", {
            "categories": categories,
            "recipes": recipes,
            "currentCategory": currentCategory
        })
    # Render categories list, recipes from category, and category name
    return render(request, "recipes/category.html", {
        "categories": categories,
        "recipes": recipes
    })


@login_required
def create_list(request):
    # Get recipe lists of logged in user
    try:
        recipeListItems = RecipeList.objects.filter(user=request.user)
    except RecipeList.DoesNotExist:
        return HttpResponse(status=204)

    # Creates list if form list name is valid
    if request.method == "POST":
        form = NewListForm(request.POST)
        if form.is_valid():
            recipeList = form.save(commit=False)
            recipeList.user = request.user
            recipeList.save()
            return render(request, "recipes/new_list.html", {
                "form": NewListForm(),
                "recipeList": recipeListItems
            })
        else:
            return render(request, "recipes/new_list.html", {
                "form": form,
                "recipeList": recipeListItems
            })
    else:
        return render(request, "recipes/new_list.html", {
            "form": NewListForm(),
            "recipeList": recipeListItems
        })


@login_required
def edit_list(request, recipeList_id):
    # Get recipe list user is editing
    try:
        recipeList = RecipeList.objects.get(id=recipeList_id)
    except RecipeList.DoesNotExist:
        return HttpResponse(status=204)

    # Verify that the logged in user is editing their list
    if request.user == recipeList.user:
        if request.method == "PUT":
            data = json.loads(request.body)
            if data.get("name") is not None:
                recipeList.name = data["name"]
            if data.get("public") is not None:
                recipeList.public = data["public"]
            recipeList.save()
            return HttpResponse(status=204)

    # If not the same user, return error
    return HttpResponse({
            "error": "You don't have permission to edit this list"
    }, status=400)


@login_required
def get_list_status(request, recipeList_id):
    # get public status of recipe list
    try:
        recipeList = RecipeList.objects.get(id=recipeList_id)
        # Verify that logged in user is same as recipe list user
        if request.user == recipeList.user:
            # Return status of recipeList
            return JsonResponse({"status": recipeList.public}, status=200)
    except RecipeList.DoesNotExist:
        return HttpResponse(status=204)

    # If not the same user, return error
    return HttpResponse({
            "error": "You don't have permission to get this public status"
    }, status=400)


@login_required
def add_to_list(request, recipe_id):
    # Get recipe
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except RecipeList.DoesNotExist:
        return HttpResponse(status=204)

    if request.method == "POST":
        form = NewListForm(request.POST)
        if form.is_valid():
            # Get recipe list
            recipeList = RecipeList.objects.get(name=request.POST.get("name"))
            # Add recipe to recipe list
            recipeList.recipes.add(recipe)
            recipeList.save()
            return redirect("viewrecipe", recipe_id=recipe_id)
        else:
            return redirect("viewrecipe", recipe_id=recipe_id)
    else:
        return redirect("viewrecipe", recipe_id=recipe_id)


def profile(request, user_id):
    try:
        # Get user
        user = User.objects.get(id=user_id)
        # If the user is viewing their own profile, get everything
        if(request.user == user):
            recipes = Recipe.objects.filter(user=user)
            recipeList = RecipeList.objects.filter(user=user)
        else:
            # If the user is someone else, get everything that's public
            recipes = Recipe.objects.filter(user=user, public=True)
            recipeList = RecipeList.objects.filter(user=user, public=True)
        reviews = Review.objects.filter(user=user)

        # Render profile with created recipes, recipeList,reviews
        return render(request, "recipes/profile.html", {
            "currentUser": user,
            "recipes": recipes,
            "recipeList": recipeList,
            "reviews": reviews
        })
    except User.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def view_recipe_list(request, list_id):
    # View recipes in recipe list
    try:
        recipeList = RecipeList.objects.get(id=list_id)
        recipes = recipeList.recipes.all()

        return render(request, "recipes/recipe_list.html", {
            "recipeList": recipeList,
            "recipes": recipes
        })
    except User.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
