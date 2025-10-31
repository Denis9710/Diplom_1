import pytest
from unittest.mock import Mock
from tests.helpers import (
    PRICE_TEST_DATA,
    RECEIPT_TEST_DATA,
    BURGER_CONFIGS
)


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

    @pytest.mark.parametrize("ingredient_count", [1, 2, 5])
    def test_add_multiple_ingredients(self, burger, custom_ingredient, ingredient_count):
        """Тест добавления нескольких ингредиентов."""
        for i in range(ingredient_count):
            mock_ingredient = custom_ingredient(name=f"ingredient_{i}")
            burger.add_ingredient(mock_ingredient)
        
        assert len(burger.ingredients) == ingredient_count

    def test_remove_ingredient(self, configured_burger, mock_ingredient):
        """Тест удаления ингредиента по индексу."""
        initial_count = len(configured_burger.ingredients)
        assert initial_count == 1  # configured_burger должен иметь 1 ингредиент
        assert configured_burger.ingredients[0] == mock_ingredient
        
        configured_burger.remove_ingredient(0)
        
        assert len(configured_burger.ingredients) == initial_count - 1
        assert len(configured_burger.ingredients) == 0

    def test_remove_ingredient_invalid_index(self, configured_burger):
        """Тест удаления ингредиента с невалидным индексом."""
        with pytest.raises(IndexError):
            configured_burger.remove_ingredient(1)  # Только 0 индекс валиден

    def test_move_ingredient_basic(self, complex_burger):
        """Базовый тест перемещения ингредиента."""
        burger, mock_bun, mock_ingredients = complex_burger
        
        # Сохраняем исходный порядок
        original_order = burger.ingredients.copy()
        ingredient_to_move = original_order[0]
        
        # Перемещаем первый ингредиент в конец
        burger.move_ingredient(0, 3)
        
        # Проверяем новый порядок
        assert burger.ingredients[3] == ingredient_to_move
        assert len(burger.ingredients) == len(original_order)
        # Дополнительная проверка: элемент действительно переместился
        assert ingredient_to_move not in burger.ingredients[:3]

    @pytest.mark.parametrize("from_index,to_index", [(0, 1), (1, 0), (2, 3)])
    def test_move_ingredient_positions(self, burger, custom_bun, custom_ingredient, from_index, to_index):
        """Параметризованный тест перемещения ингредиентов между позициями."""
        # Создаем бургер с 4 ингредиентами для согласованности с complex_burger
        mock_bun = custom_bun()
        burger.set_buns(mock_bun)
        
        mock_ingredients = []
        for i in range(4):
            mock_ingredient = custom_ingredient(name=f"ingredient_{i}")
            burger.add_ingredient(mock_ingredient)
            mock_ingredients.append(mock_ingredient)
        
        original_ingredients = burger.ingredients.copy()
        
        # Выполняем перемещение
        burger.move_ingredient(from_index, to_index)
        
        # Проверяем результат
        assert burger.ingredients[to_index] == original_ingredients[from_index]
        assert len(burger.ingredients) == len(original_ingredients)

    def test_move_ingredient_invalid_index(self, configured_burger):
        """Тест перемещения ингредиента с невалидным индексом."""
        with pytest.raises(IndexError):
            configured_burger.move_ingredient(1, 0)  # Только 0 индекс валиден

    @pytest.mark.parametrize("bun_price,ingredient_prices,expected_price", PRICE_TEST_DATA)
    def test_get_price(self, burger, custom_bun, custom_ingredient, bun_price, ingredient_prices, expected_price):
        """Параметризованный тест расчета цены бургера."""
        # Создаем и устанавливаем булочку
        mock_bun = custom_bun(price=bun_price)
        burger.set_buns(mock_bun)
        
        # Добавляем ингредиенты
        for i, price in enumerate(ingredient_prices):
            mock_ingredient = custom_ingredient(name=f"ingredient_{i}", price=price)
            burger.add_ingredient(mock_ingredient)
        
        result_price = burger.get_price()
        
        assert result_price == expected_price
        mock_bun.get_price.assert_called_once()
        
        # Проверяем, что get_price вызван для каждого ингредиента
        for mock_ingredient in burger.ingredients:
            mock_ingredient.get_price.assert_called_once()

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
        mock_bun.get_price.assert_called_once()

    @pytest.mark.parametrize("bun_name,ingredient_data,expected_receipt_parts", RECEIPT_TEST_DATA)
    def test_get_receipt(self, burger, custom_bun, custom_ingredient, bun_name, ingredient_data, expected_receipt_parts):
        """Параметризованный тест генерации чека."""
        # Создаем и устанавливаем булочку
        mock_bun = custom_bun(name=bun_name, price=100.0)
        burger.set_buns(mock_bun)
        
        # Добавляем ингредиенты
        for ingredient_type, ingredient_name in ingredient_data:
            mock_ingredient = custom_ingredient(
                name=ingredient_name, 
                ingredient_type=ingredient_type, 
                price=50.0
            )
            burger.add_ingredient(mock_ingredient)
        
        receipt = burger.get_receipt()
        
        # Проверяем наличие ожидаемых частей в чеке
        for expected_part in expected_receipt_parts:
            assert expected_part in receipt
        
        # Проверяем структуру чека
        receipt_lines = receipt.split('\n')
        assert receipt_lines[0] == f'(==== {bun_name} ====)'
        assert receipt_lines[-2] == f'(==== {bun_name} ====)'
        assert receipt_lines[-1].startswith('Price: ')

    def test_get_receipt_no_bun(self, burger):
        """Тест генерации чека без установленной булочки."""
        with pytest.raises(AttributeError):
            burger.get_receipt()

    def test_get_receipt_empty_burger(self, burger, mock_bun):
        """Тест генерации чека бургера без ингредиентов."""
        burger.set_buns(mock_bun)
        receipt = burger.get_receipt()
        
        assert mock_bun.get_name.return_value in receipt
        assert "Price:" in receipt
        # Проверяем, что булочка встречается дважды (верх и низ)
        assert receipt.count(mock_bun.get_name.return_value) == 2

    @pytest.mark.parametrize("burger_config_name", ["empty", "cheeseburger", "deluxe"])
    def test_burger_configurations(self, burger, custom_bun, custom_ingredient, burger_config_name):
        """Тест готовых конфигураций бургеров."""
        config = BURGER_CONFIGS[burger_config_name]
        
        # Создаем и устанавливаем булочку
        mock_bun = custom_bun(name=config["bun_name"], price=config["bun_price"])
        burger.set_buns(mock_bun)
        
        # Добавляем ингредиенты
        for ingredient_config in config["ingredients"]:
            mock_ingredient = custom_ingredient(
                name=ingredient_config["name"],
                ingredient_type=ingredient_config["type"],
                price=ingredient_config["price"]
            )
            burger.add_ingredient(mock_ingredient)
        
        # Проверяем цену
        expected_price = (config["bun_price"] * 2 + 
                         sum(ingredient["price"] for ingredient in config["ingredients"]))
        assert burger.get_price() == expected_price
        
        # Проверяем чек
        receipt = burger.get_receipt()
        assert config["bun_name"] in receipt
        for ingredient_config in config["ingredients"]:
            assert ingredient_config["name"] in receipt
            assert ingredient_config["type"].lower() in receipt

    def test_multiple_operations_integration(self, burger, custom_bun, custom_ingredient):
        """Интеграционный тест нескольких операций с бургером."""
        # Создаем компоненты
        mock_bun = custom_bun(name="sesame bun", price=80.0)
        mock_ingredient1 = custom_ingredient(name="cheese", ingredient_type="FILLING", price=40.0)
        mock_ingredient2 = custom_ingredient(name="ketchup", ingredient_type="SAUCE", price=20.0)
        mock_ingredient3 = custom_ingredient(name="tomato", ingredient_type="FILLING", price=15.0)
        
        # Выполняем последовательность операций
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        burger.add_ingredient(mock_ingredient3)
        
        # Проверяем промежуточное состояние
        assert len(burger.ingredients) == 3
        original_order = burger.ingredients.copy()
        
        # Перемещаем ингредиент
        burger.move_ingredient(0, 2)
        assert burger.ingredients[2] == original_order[0]
        
        # Удаляем ингредиент
        burger.remove_ingredient(0)
        
        # Проверяем финальное состояние и цену
        assert len(burger.ingredients) == 2
        expected_price = 80.0 * 2 + 15.0 + 40.0  # булочка * 2 + tomato + cheese
        assert burger.get_price() == expected_price

    def test_receipt_contains_correct_ingredient_format(self, burger, mock_bun, mock_ingredient):
        """Тест корректного форматирования ингредиентов в чеке."""
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient)
        
        receipt = burger.get_receipt()
        receipt_lines = receipt.split('\n')
        
        # Проверяем формат строки ингредиента
        ingredient_line = receipt_lines[1]
        expected_format = f"= {mock_ingredient.get_type.return_value.lower()} {mock_ingredient.get_name.return_value} ="
        assert ingredient_line == expected_format