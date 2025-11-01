import pytest
from unittest.mock import Mock

# Тестовые данные прямо в файле
PRICE_TEST_DATA = [
    (100.0, [50.0, 75.0], 325.0),      # 100*2 + 50 + 75
    (50.0, [25.0, 30.0, 45.0], 200.0), # 50*2 + 25 + 30 + 45
    (80.0, [], 160.0),                  # Только булочки
    (0.0, [10.0, 20.0], 30.0),         # Бесплатные булочки
]

RECEIPT_TEST_DATA = [
    (
        "white bun", 
        [("SAUCE", "ketchup"), ("FILLING", "cheese")],
        # Цена: 100*2 + 50 + 50 = 300.0
    ),
    (
        "black bun",
        [("FILLING", "beef")],
        # Цена: 100*2 + 50 = 250.0
    ),
]

BURGER_CONFIGS = {
    "empty": {
        "bun_name": "basic bun",
        "bun_price": 50.0,
        "ingredients": [],
        # Цена: 50*2 = 100.0
    },
    "cheeseburger": {
        "bun_name": "sesame bun", 
        "bun_price": 80.0,
        "ingredients": [
            {"name": "beef", "type": "FILLING", "price": 120.0},
            {"name": "cheese", "type": "FILLING", "price": 40.0}
        ],
        # Цена: 80*2 + 120 + 40 = 320.0
    },
}


class TestBurger:
    """
    Тесты для класса Burger.
    """

    def test_initialization(self, burger):
        """Тест инициализации бургера."""
        assert burger.bun is None
        assert burger.ingredients == []

    def test_set_buns(self, burger, mock_bun):
        """Тест установки булочки."""
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient(self, burger, mock_ingredient):
        """Тест добавления одного ингредиента."""
        burger.add_ingredient(mock_ingredient)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient

    def test_add_multiple_ingredients(self, burger, custom_ingredient):
        """Тест добавления нескольких ингредиентов."""
        mock_ingredient1 = custom_ingredient(name="ingredient_1")
        mock_ingredient2 = custom_ingredient(name="ingredient_2")
        
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        
        assert len(burger.ingredients) == 2
        assert burger.ingredients[0] == mock_ingredient1
        assert burger.ingredients[1] == mock_ingredient2

    def test_remove_ingredient(self, configured_burger, mock_ingredient):
        """Тест удаления ингредиента по индексу."""
        initial_count = len(configured_burger.ingredients)
        assert initial_count == 1
        assert configured_burger.ingredients[0] == mock_ingredient
        
        configured_burger.remove_ingredient(0)
        
        assert len(configured_burger.ingredients) == 0

    def test_remove_ingredient_invalid_index(self, configured_burger):
        """Тест удаления ингредиента с невалидным индексом."""
        with pytest.raises(IndexError):
            configured_burger.remove_ingredient(1)

    def test_move_ingredient(self, burger, custom_bun, custom_ingredient):
        """Тест перемещения ингредиента."""
        mock_bun = custom_bun()
        burger.set_buns(mock_bun)
        
        mock_ingredient1 = custom_ingredient(name="ingredient_1")
        mock_ingredient2 = custom_ingredient(name="ingredient_2")
        mock_ingredient3 = custom_ingredient(name="ingredient_3")
        
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        burger.add_ingredient(mock_ingredient3)
        
        # Перемещаем первый ингредиент в конец
        burger.move_ingredient(0, 2)
        
        # Проверяем новый порядок
        assert burger.ingredients[0] == mock_ingredient2
        assert burger.ingredients[1] == mock_ingredient3
        assert burger.ingredients[2] == mock_ingredient1

    def test_move_ingredient_invalid_index(self, configured_burger):
        """Тест перемещения ингредиента с невалидным индексом."""
        with pytest.raises(IndexError):
            configured_burger.move_ingredient(1, 0)

    @pytest.mark.parametrize("bun_price,ingredient_prices,expected_price", PRICE_TEST_DATA)
    def test_get_price(self, burger, custom_bun, custom_ingredient, bun_price, ingredient_prices, expected_price):
        """Параметризованный тест расчета цены бургера."""
        mock_bun = custom_bun(price=bun_price)
        burger.set_buns(mock_bun)
        
        for i, price in enumerate(ingredient_prices):
            mock_ingredient = custom_ingredient(name=f"ingredient_{i}", price=price)
            burger.add_ingredient(mock_ingredient)
        
        result_price = burger.get_price()
        assert result_price == expected_price

    def test_get_price_no_bun(self, burger):
        """Тест расчета цены без установленной булочки."""
        with pytest.raises(AttributeError):
            burger.get_price()

    def test_get_price_empty_burger(self, burger, mock_bun):
        """Тест расчета цены бургера без ингредиентов."""
        burger.set_buns(mock_bun)
        expected_price = mock_bun.get_price.return_value * 2
        
        result_price = burger.get_price()
        assert result_price == expected_price

    @pytest.mark.parametrize("bun_name,ingredient_data,expected_receipt_lines", RECEIPT_TEST_DATA)
    def test_get_receipt_parametrized(self, burger, custom_bun, custom_ingredient, bun_name, ingredient_data):
        """Параметризованный тест генерации чека."""
        mock_bun = custom_bun(name=bun_name, price=100.0)
        burger.set_buns(mock_bun)
        
        for ingredient_type, ingredient_name in ingredient_data:
            mock_ingredient = custom_ingredient(
                name=ingredient_name, 
                ingredient_type=ingredient_type, 
                price=50.0
            )
            burger.add_ingredient(mock_ingredient)
        
        receipt = burger.get_receipt()
        receipt_lines = receipt.split('\n')
        
        # Динамически рассчитываем ожидаемые строки
        expected_lines = [f"(==== {bun_name} ====)"]
        
        for ingredient_type, ingredient_name in ingredient_data:
            expected_lines.append(f"= {ingredient_type.lower()} {ingredient_name} =")
        
        expected_lines.append(f"(==== {bun_name} ====)")
        expected_lines.append("")  # Пустая строка
        expected_lines.append(f"Price: {burger.get_price()}")
        
        # Проверяем точное соответствие строк
        assert receipt_lines == expected_lines

    def test_get_receipt_no_bun(self, burger):
        """Тест генерации чека без установленной булочки."""
        with pytest.raises(AttributeError):
            burger.get_receipt()

    def test_get_receipt_empty_burger(self, burger, mock_bun):
        """Тест генерации чека бургера без ингредиентов."""
        burger.set_buns(mock_bun)
        receipt = burger.get_receipt()
        receipt_lines = receipt.split('\n')
        
        # Динамически рассчитываем ожидаемые строки
        expected_price = mock_bun.get_price.return_value * 2
        expected_lines = [
            f"(==== {mock_bun.get_name.return_value} ====)",
            f"(==== {mock_bun.get_name.return_value} ====)",
            "",  # Пустая строка
            f"Price: {expected_price}"
        ]
        
        assert receipt_lines == expected_lines

    def test_burger_configuration_empty(self, burger, custom_bun):
        """Тест пустого бургера."""
        config = BURGER_CONFIGS["empty"]
        
        mock_bun = custom_bun(name=config["bun_name"], price=config["bun_price"])
        burger.set_buns(mock_bun)
        
        expected_price = config["bun_price"] * 2
        assert burger.get_price() == expected_price
        
        receipt = burger.get_receipt()
        receipt_lines = receipt.split('\n')
        
        # Динамически рассчитываем ожидаемые строки
        expected_lines = [
            f"(==== {config['bun_name']} ====)",
            f"(==== {config['bun_name']} ====)",
            "",  # Пустая строка
            f"Price: {expected_price}"
        ]
        
        assert receipt_lines == expected_lines

    def test_burger_configuration_cheeseburger(self, burger, custom_bun, custom_ingredient):
        """Тест чизбургера."""
        config = BURGER_CONFIGS["cheeseburger"]
        
        mock_bun = custom_bun(name=config["bun_name"], price=config["bun_price"])
        burger.set_buns(mock_bun)
        
        for ingredient_config in config["ingredients"]:
            mock_ingredient = custom_ingredient(
                name=ingredient_config["name"],
                ingredient_type=ingredient_config["type"],
                price=ingredient_config["price"]
            )
            burger.add_ingredient(mock_ingredient)
        
        expected_price = (config["bun_price"] * 2 + 
                         sum(ingredient["price"] for ingredient in config["ingredients"]))
        assert burger.get_price() == expected_price
        
        receipt = burger.get_receipt()
        receipt_lines = receipt.split('\n')
        
        # Динамически рассчитываем ожидаемые строки
        expected_lines = [f"(==== {config['bun_name']} ====)"]
        
        for ingredient_config in config["ingredients"]:
            expected_lines.append(f"= {ingredient_config['type'].lower()} {ingredient_config['name']} =")
        
        expected_lines.append(f"(==== {config['bun_name']} ====)")
        expected_lines.append("")  # Пустая строка
        expected_lines.append(f"Price: {expected_price}")
        
        assert receipt_lines == expected_lines

    def test_multiple_operations(self, burger, custom_bun, custom_ingredient):
        """Интеграционный тест нескольких операций с бургером."""
        mock_bun = custom_bun(name="sesame bun", price=80.0)
        mock_ingredient1 = custom_ingredient(name="cheese", ingredient_type="FILLING", price=40.0)
        mock_ingredient2 = custom_ingredient(name="ketchup", ingredient_type="SAUCE", price=20.0)
        
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        
        assert len(burger.ingredients) == 2
        
        burger.remove_ingredient(0)
        
        assert len(burger.ingredients) == 1
        expected_price = 80.0 * 2 + 20.0  # булочка * 2 + ketchup
        assert burger.get_price() == expected_price

    def test_receipt_format(self, burger, mock_bun, mock_ingredient):
        """Тест корректного форматирования ингредиентов в чеке."""
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient)
        
        receipt = burger.get_receipt()
        receipt_lines = receipt.split('\n')
        
        # Динамически рассчитываем ожидаемые строки
        expected_price = mock_bun.get_price.return_value * 2 + mock_ingredient.get_price.return_value
        expected_lines = [
            f"(==== {mock_bun.get_name.return_value} ====)",
            f"= {mock_ingredient.get_type.return_value.lower()} {mock_ingredient.get_name.return_value} =",
            f"(==== {mock_bun.get_name.return_value} ====)",
            "",  # Пустая строка
            f"Price: {expected_price}"
        ]
        
        assert receipt_lines == expected_lines

        