from django.db.models.aggregates import Sum

from foodgram.settings import CART_INGREDIENTS_FORMAT
from recipes.models import IngredientRecipe


def make_shopping_list(request):
    text_lines = ['Список покупок\n']
    # Замечание-почему бы сразу не использовать строку?
    # Переменная используется, как список.К строке не добовляются ингридиенты
    for item in IngredientRecipe.objects.filter(
        recipe__cart__user=request.user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).order_by(
        'ingredient__name'
    ).annotate(
        total_amount=Sum('amount')
    ):
        text_lines.append(
            CART_INGREDIENTS_FORMAT.format(
                name=item['ingredient__name'],
                measurement_unit=item['ingredient__measurement_unit'],
                total=item['total_amount']
            )
        )
    response_content = '\n'.join(text_lines)

    return response_content
