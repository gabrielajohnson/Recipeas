from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
import re

# Create your models here.


# Validate preptime and cooktime so that it is entered in this format 00:00:00
def validate_duration(value):
    durationPattern = re.compile("\d\d:\d\d:\d\d")
    emptyPattern = "00:00:00"
    stringValue = str(value)
    if not (durationPattern.match(stringValue)):
        raise ValidationError(
            ('%(value)s is not in the correct format 00:00:00'),
            params={'value': value},
        )


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=32)
    custom = models.BooleanField()

    def __str__(self):

        return f"{self.category}"


class Recipe(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=64)
    image = models.ImageField(upload_to='static/images/')
    description = models.TextField(blank=True)
    # User enters time in intial field
    preptime_initial = models.CharField(max_length=64, validators=[validate_duration])
    # Intial field value is saved here so 00:00:00 format can always be retrieved
    preptime = models.CharField(max_length=64)
    cooktime_initial = models.CharField(max_length=64, validators=[validate_duration])
    cooktime = models.CharField(max_length=64)
    total_time = models.IntegerField()
    servings = models.IntegerField()
    ingredients = models.TextField()
    ingredients_length = models.IntegerField()
    steps = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category)
    public = models.BooleanField(default=True)
    inspiration = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="recipe_inspiration", blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.user}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "title": self.title,
            "description": self.description,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
        }


class Review(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="reviews")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="recipes")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="recipe_comments")
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class RecipeList(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="recipe_lists")
    name = models.CharField(max_length=30)
    recipes = models.ManyToManyField(Recipe)
    timestamp = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField()
