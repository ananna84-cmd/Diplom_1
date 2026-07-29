import pytest
from unittest.mock import Mock

from praktikum.burger import Burger


@pytest.fixture
def empty_burger():
    return Burger()

@pytest.fixture
def burger_three_ingredients():
    burger = Burger()

    # Булочка
    bun = Mock()
    bun.get_name.return_value = "Булочка"
    bun.get_price.return_value = 100
    burger.set_buns(bun)

    # Ингредиенты
    ing1 = Mock()
    ing1.get_name.return_value = "Соус 1"
    ing1.get_type.return_value = "SAUCE"
    ing1.get_price.return_value = 20

    ing2 = Mock()
    ing2.get_name.return_value = "Начинка 1"
    ing2.get_type.return_value = "FILLING"
    ing2.get_price.return_value = 50

    ing3 = Mock()
    ing3.get_name.return_value = "Начинка 2"
    ing3.get_type.return_value = "FILLING"
    ing3.get_price.return_value = 70

    burger.add_ingredient(ing1)
    burger.add_ingredient(ing2)
    burger.add_ingredient(ing3)

    return burger, bun, ing1, ing2, ing3