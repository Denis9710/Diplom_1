"""
Вспомогательные данные для параметризации тестов класса Burger.
"""

# Тестовые данные для параметризации расчета цены
PRICE_TEST_DATA = [
    # (цена_булочки, [цены_ингредиентов], ожидаемая_цена)
    (100.0, [50.0, 75.0], 325.0),      # 100*2 + 50 + 75
    (50.0, [25.0, 30.0, 45.0], 200.0), # 50*2 + 25 + 30 + 45
    (80.0, [], 160.0),                  # Только булочки
    (0.0, [10.0, 20.0], 30.0),         # Бесплатные булочки
    (150.0, [100.0], 400.0),           # Один дорогой ингредиент
]

# Тестовые данные для параметризации генерации чека
RECEIPT_TEST_DATA = [
    # (название_булочки, [(тип_ингредиента, название_ингредиента)], ожидаемые_части_чека)
    (
        "white bun", 
        [("SAUCE", "ketchup"), ("FILLING", "cheese")],
        ["(==== white bun ====)", "= sauce ketchup =", "= filling cheese =", "Price: "]
    ),
    (
        "black bun",
        [("FILLING", "beef"), ("SAUCE", "mayo"), ("FILLING", "tomato")],
        ["(==== black bun ====)", "= filling beef =", "= sauce mayo =", "= filling tomato =", "Price: "]
    ),
    (
        "regular bun",
        [],
        ["(==== regular bun ====)", "(==== regular bun ====)", "Price: "]
    ),
    (
        "sesame bun",
        [("SAUCE", "barbecue"), ("FILLING", "chicken")],
        ["(==== sesame bun ====)", "= sauce barbecue =", "= filling chicken =", "Price: "]
    ),
]

# Тестовые данные для параметризации перемещения ингредиентов
INGREDIENT_MOVEMENT_TEST_DATA = [
    # (начальные_индексы, индекс_для_перемещения, новый_индекс, ожидаемые_индексы)
    ([0, 1, 2], 0, 2, [1, 2, 0]),  # Первый элемент в конец
    ([0, 1, 2], 2, 0, [2, 0, 1]),  # Последний элемент в начало
    ([0, 1, 2], 1, 1, [0, 1, 2]),  # Перемещение на то же место
]

# Готовые конфигурации бургеров для тестирования
BURGER_CONFIGS = {
    "empty": {
        "bun_name": "basic bun",
        "bun_price": 50.0,
        "ingredients": []
    },
    "cheeseburger": {
        "bun_name": "sesame bun", 
        "bun_price": 80.0,
        "ingredients": [
            {"name": "beef", "type": "FILLING", "price": 120.0},
            {"name": "cheese", "type": "FILLING", "price": 40.0}
        ]
    },
    "deluxe": {
        "bun_name": "premium bun",
        "bun_price": 120.0,
        "ingredients": [
            {"name": "angus beef", "type": "FILLING", "price": 180.0},
            {"name": "cheddar", "type": "FILLING", "price": 60.0},
            {"name": "bacon", "type": "FILLING", "price": 80.0},
            {"name": "bbq sauce", "type": "SAUCE", "price": 20.0}
        ]
    }
}