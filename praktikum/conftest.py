import pytest
from unittest.mock import Mock

from praktikum.burger import Burger
from praktikum.bun import Bun


# Mock булка
@pytest.fixture
def mock_bun():
    bun = Mock(spec=Bun)
    bun.get_name.return_value = "Булочка 1"
    bun.get_price.return_value = 100
    return bun


# Mock ингридиенты
@pytest.fixture
def mock_ingredient():
    ing = Mock()
    ing.get_name.return_value = "Начинка 1"
    ing.get_type.return_value = "FILLING"
    ing.get_price.return_value = 50
    return ing


# Создание бургер с булочкой и несколькими разными ингредиентами
@pytest.fixture
def burger_with_full_setup(mock_bun, mock_ingredient):
    burger = Burger()
    burger.set_buns(mock_bun)

    ing1 = Mock()
    ing1.get_name.return_value = "Соус1"
    ing1.get_type.return_value = "SAUCE"
    ing1.get_price.return_value = 20
    
    ing2 = Mock()
    ing2.get_name.return_value = "Начинка 2"
    ing2.get_type.return_value = "FILLING"
    ing2.get_price.return_value = 200
    
    burger.add_ingredient(ing1)
    burger.add_ingredient(ing2)
    
    return burger, mock_bun, ing1, ing2
