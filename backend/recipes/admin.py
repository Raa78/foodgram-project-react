from django.contrib import admin

from .models import Favorite, Ingredient, IngredientRecipe, Recipe, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'measurement_unit',
    )


class IngredientInline(admin.TabularInline):
    model = IngredientRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)
    list_display = (
        'id',
        'author',
        'name',
        'text',
        'cooking_time',
        'favorites'
    )
    list_filter = ('name',)

    def favorites(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    favorites.short_description = 'В избранных'
