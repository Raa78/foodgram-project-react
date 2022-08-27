"""
Унифицированные настройки приложения Foodgram
для соблюдения принципа DRY.
"""

# Общие настройки для админок
EMPTY_VALUE_DISPLAY = '-пусто-'

# Настройки модели приложения recipes
COOKING_MIN_TIME = 1
COOKING_MIN_TIME_ERROR = 'Время приготовления не может быть меньше 1-ой минуты'  # Быстро только кошки родятся
INGREDIENT_MIN_QUANTITY = 1
INGREDIENT_MIN_QUANTITY_ERROR = 'В рецепте должно быть не менее 1-ого ингридиента'

# Настройки для сериализатора
INGREDIENTS_COUNT_ERROR = 'Количество ингредиента в рецепте не может быть <=1'
INGREDIENT_REPETITION_ERROR = 'Ингредиенты не могут повторяться'

# Настройки вьюхи api
SUBSCRIBE_TO_YOURSELF_ERROR = 'Нельзя подписатья на самого себя!'
UNSUBSCRIBE_TO_YOURSELF_ERROR = 'Вы пытаетесь отписаться от самого себя!'
EXIST_SUBSCRIBE_ERROR = 'Вы уже подписаны на этого пользователя!'
NON_EXIST_UNSUBSCRIBE_ERROR = 'Вы и так не подписаны на этого пользователя!'
CART_INGREDIENTS_FORMAT = '\t{name}, {measurement_unit}: {total}'
SHOPPING_CART_FILENAME = 'shopping_cart.txt'

# Вывод покупок
FILENAME = 'shopping_cart.pdf'
