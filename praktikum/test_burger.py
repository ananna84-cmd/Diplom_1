import pytest

from praktikum.burger import Burger


# Проверки "__init__"
# После инициализации булочка должна отсутствовать (None)
def test_burger_bun_is_none_after_init():
    burger = Burger()
    assert burger.bun is None

# Список ингредиентов пустой после создания объекта
def test_burger_ingredients_list_is_empty():
    burger = Burger()
    assert len(burger.ingredients) == 0

# Проверки "set_buns"
# Проверка: set_buns корректно присваивает булочку
def test_set_buns_assigns_bun_correctly(mock_bun):
    burger = Burger()
    burger.set_buns(mock_bun)
    assert burger.bun is mock_bun

# Проверка: set_buns сохраняет последнюю дорбавленую булочку
def test_set_buns_overwrites_previous_bun(mock_buns):
    burger = Burger()
    old_bun, new_bun = mock_buns
    burger.set_buns(old_bun)
    burger.set_buns(new_bun)
    assert burger.bun is new_bun

# Проверки "add_ingredient"
# Проверка: после добавления длина списка ингредиентов увеличивается на 1.
def test_add_ingredient_increases_count(mock_ingredient):
    burger = Burger()
    start_len = len(burger.ingredients)
    burger.add_ingredient(mock_ingredient)
    assert len(burger.ingredients) == start_len + 1

# Проверка: "move_ingredient"(index: int, new_index: int)
# Проверка: элемент перемещается на указанный индекс
def test_move_ingredient_shifts_element(burger_with_full_setup):
    burger, _, ing1, ing2 = burger_with_full_setup
    burger.move_ingredient(0, 1) 
    assert burger.ingredients == [ing2, ing1]

# Проверка remove_ingredient
# Проверка: после удаления длина уменьшается, остальные элементы сдвигаются
def test_remove_ingredient_decreases_count(burger_with_full_setup):
    burger, _, _, _ = burger_with_full_setup
    start_len = len(burger.ingredients)
    burger.remove_ingredient(0)
    assert len(burger.ingredients) == start_len - 1

# Проверка: при неверном индексе выбрасывается `IndexError
def test_remove_invalid_index_raises_error():
    burger = Burger()
    with pytest.raises(IndexError):
        burger.remove_ingredient(0)

# Проверка "get_price()"
# Проверка: цена считается как 2 * цена булочки + сумма цен ингредиентов
def test_get_price_calculates_correctly_with_ingredients(burger_with_full_setup):
    burger, bun, ing1, ing2 = burger_with_full_setup

    expected_price = (2 * bun.get_price()) + ing1.get_price() + ing2.get_price()
    result = burger.get_price()
    
    assert result == expected_price

# Проверка "get_receipt()"
# Проверка: формат строки содержит шапку с булочкой, список ингредиентов, нижнюю часть и цену
def test_get_receipt_format_and_price(burger_with_full_setup):
    burger, bun, ing1, ing2 = burger_with_full_setup
    
    bun.get_name.return_value = "Булочка 2"
    ing1.get_name.return_value = "Соус 2"
    ing1.get_type.return_value = "SAUCE"
    ing2.get_name.return_value = "Начинка 3"
    ing2.get_type.return_value = "FILLING"
    
    expected_price = (2 * bun.get_price()) + ing1.get_price() + ing2.get_price()
    receipt = burger.get_receipt()
    expected_receipt = [
        f"(==== {bun.get_name()} ====",
        f"= {ing1.get_type().lower()} {ing1.get_name()} =",
        f"= {ing2.get_type().lower()} {ing2.get_name()} =",
        f"(==== {bun.get_name()} ====)\n",
        f"Price: {expected_price}"
    ]
    expected_string = "\n".join(expected_receipt)

    assert receipt == expected_string
    