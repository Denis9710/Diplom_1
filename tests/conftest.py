import pytest
from unittest.mock import Mock


class Burger:

    def __init__(self):
        self.bun = None
        self.ingredients = []

    def set_buns(self, bun):
        self.bun = bun

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def remove_ingredient(self, index: int):
        del self.ingredients[index]

    def move_ingredient(self, index: int, new_index: int):
        self.ingredients.insert(new_index, self.ingredients.pop(index))

    def get_price(self) -> float:
        price = self.bun.get_price() * 2

        for ingredient in self.ingredients:
            price += ingredient.get_price()

        return price

    def get_receipt(self) -> str:
        receipt = [f'(==== {self.bun.get_name()} ====)']

        for ingredient in self.ingredients:
            receipt.append(f'= {str(ingredient.get_type()).lower()} {ingredient.get_name()} =')

        receipt.append(f'(==== {self.bun.get_name()} ====)\n')
        receipt.append(f'Price: {self.get_price()}')

        return '\n'.join(receipt)


@pytest.fixture
def burger():
    """Фикстура для создания чистого бургера."""
    return Burger()


@pytest.fixture
def mock_bun():
    """Фикстура для создания мока булочки с базовыми значениями."""
    mock_bun = Mock()
    mock_bun.get_name.return_value = 'Белая булочка'
    mock_bun.get_price.return_value = 100.0
    return mock_bun


@pytest.fixture
def mock_ingredient():
    """Фикстура для создания мока ингредиента с базовыми значениями."""
    mock_ingredient = Mock()
    mock_ingredient.get_name.return_value = 'Сыр'
    mock_ingredient.get_type.return_value = 'FILLING'
    mock_ingredient.get_price.return_value = 50.0
    return mock_ingredient


@pytest.fixture
def configured_burger(mock_bun, mock_ingredient):
    """Фикстура для создания настроенного бургера с булочкой и одним ингредиентом."""
    burger = Burger()
    burger.set_buns(mock_bun)
    burger.add_ingredient(mock_ingredient)
    return burger


@pytest.fixture
def complex_burger():
    """Фикстура для создания сложного бургера с несколькими ингредиентами."""
    burger = Burger()
    
    # Булочка
    mock_bun = Mock()
    mock_bun.get_name.return_value = 'Крафтовая булочка'
    mock_bun.get_price.return_value = 80.0
    burger.set_buns(mock_bun)
    
    # Ингредиенты
    ingredients_data = [
        {'type': 'SAUCE', 'name': 'Соус барбекю', 'price': 15.0},
        {'type': 'FILLING', 'name': 'Говядина', 'price': 120.0},
        {'type': 'FILLING', 'name': 'Сыр чеддер', 'price': 40.0},
        {'type': 'SAUCE', 'name': 'Майонез', 'price': 10.0}
    ]
    
    mock_ingredients = []
    for ingredient_data in ingredients_data:
        mock_ingredient = Mock()
        mock_ingredient.get_type.return_value = ingredient_data['type']
        mock_ingredient.get_name.return_value = ingredient_data['name']
        mock_ingredient.get_price.return_value = ingredient_data['price']
        burger.add_ingredient(mock_ingredient)
        mock_ingredients.append(mock_ingredient)
    
    return burger, mock_bun, mock_ingredients


@pytest.fixture
def custom_bun():
    """Фикстура для создания кастомной булочки с параметрами."""
    def _create_bun(name='Булочка', price=100.0):
        mock_bun = Mock()
        mock_bun.get_name.return_value = name
        mock_bun.get_price.return_value = price
        return mock_bun
    return _create_bun


@pytest.fixture
def custom_ingredient():
    """Фикстура для создания кастомного ингредиента с параметрами."""
    def _create_ingredient(name='Ингредиент', ingredient_type='FILLING', price=50.0):
        mock_ingredient = Mock()
        mock_ingredient.get_name.return_value = name
        mock_ingredient.get_type.return_value = ingredient_type
        mock_ingredient.get_price.return_value = price
        return mock_ingredient
    return _create_ingredient