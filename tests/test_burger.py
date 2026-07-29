from unittest.mock import Mock
import pytest

from praktikum.burger import Burger


# Проверки "__init__"
# Инициализация без аргументов → булочка равна None
def test_init_no_args_bun_is_none():
    burger = Burger()
    assert burger.bun is None

# Инициализация без аргументов → список ингредиентов пустой
def test_init_no_args_ingredients_list_empty():
    burger = Burger()
    assert len(burger.ingredients) == 0

# Проверки "set_buns"
# set_buns принимает булочку → в атрибуте bun оказывается эта булочка
def test_set_buns_bun_assigned(empty_burger):
    mock_bun = Mock()
    empty_burger.set_buns(mock_bun)
    assert empty_burger.bun is mock_bun

# set_buns вызывается дважды → сохраняется только последняя булочка
def test_set_buns_second_bun_overwrites_first(empty_burger):
    old_bun = Mock()
    new_bun = Mock()
    empty_burger.set_buns(old_bun)
    empty_burger.set_buns(new_bun)
    assert empty_burger.bun is new_bun

# Проверки "add_ingredient"
# Добавляем N ингредиентов → длина списка увеличивается на N
@pytest.mark.parametrize(
    "count",
    [1, 3],
    ids=["add_1_len_increased", "add_3_len_increased"]
)
def test_add_ingredient_count_n_list_length_increased_by_n(empty_burger, count):
    start_len = len(empty_burger.ingredients)
    for _ in range(count):
        empty_burger.add_ingredient(Mock())
    assert len(empty_burger.ingredients) == start_len + count

# Добавляем один ингредиент → он становится последним элементом списка
def test_add_ingredient_single_item_appended_as_last(empty_burger):
    ingredient = Mock()
    empty_burger.add_ingredient(ingredient)
    assert empty_burger.ingredients[-1] is ingredient

# Добавляем несколько ингредиентов → порядок сохраняется
def test_add_multiple_ingredients_order_preserved(empty_burger):
    ing1, ing2, ing3 = Mock(), Mock(), Mock()
    empty_burger.add_ingredient(ing1)
    empty_burger.add_ingredient(ing2)
    empty_burger.add_ingredient(ing3)
    assert empty_burger.ingredients == [ing1, ing2, ing3]

# Проверки "move_ingredient"
@pytest.mark.parametrize(
    "from_idx,to_idx",
    [(0, 1), (1, 0), (0, 0), (2, 0), (0, 2)],
    ids=[
        "move_0_to_1",
        "move_1_to_0",
        "move_same_idx",
        "move_end_to_start",
        "move_start_to_end"
    ]
)
# Перемещаем элемент с индекса N на индекс M → порядок списка меняется корректно
def test_move_ingredient_from_n_to_m_element_placed_at_target_index(burger_three_ingredients, from_idx, to_idx):
    burger, _, _, _, _ = burger_three_ingredients
    original = burger.ingredients[:]

    burger.move_ingredient(from_idx, to_idx)

    expected = original[:]
    item = expected.pop(from_idx)
    expected.insert(to_idx, item)

    assert burger.ingredients == expected

# Передаём неверный индекс источника → выбрасывается IndexError
def test_move_ingredient_invalid_source_index_raises_index_error(burger_three_ingredients):
    burger, _, _, _, _ = burger_three_ingredients
    with pytest.raises(IndexError):
        burger.move_ingredient(99, 0)

# Проверки "remove_ingredient"
# Удаляем ингредиент по индексу N → длина списка становится M
@pytest.mark.parametrize(
    "remove_idx,expected_len",
    [(0, 2), (1, 2), (2, 2)],
    ids=["remove_first_len_2", "remove_middle_len_2", "remove_last_len_2"]
)
def test_remove_ingredient_index_n_length_m(burger_three_ingredients, remove_idx, expected_len):
    burger, _, _, _, _ = burger_three_ingredients
    burger.remove_ingredient(remove_idx)
    assert len(burger.ingredients) == expected_len

# Пытаемся удалить из пустого списка → выбрасывается IndexError
def test_remove_from_empty_list_raises_index_error(empty_burger):
    with pytest.raises(IndexError):
        empty_burger.remove_ingredient(0)

# Передаём неверный индекс → выбрасывается IndexError
def test_remove_invalid_index_raises_index_error(burger_three_ingredients):
    burger, _, _, _, _ = burger_three_ingredients
    with pytest.raises(IndexError):
        burger.remove_ingredient(99)

# Проверки "get_price()"
# При N ингредиентах get_price возвращает цену X
@pytest.mark.parametrize(
    "ing_count,expected_price",
    [(0, 200), (1, 220), (3, 340)],
    ids=["price_0_ing_200", "price_1_ing_220", "price_3_ing_340"]
)
def test_get_price_ingredients_count_n_returns_price_x(empty_burger, ing_count, expected_price):
    bun = Mock()
    bun.get_price.return_value = 100
    empty_burger.set_buns(bun)

    prices = [20, 50, 70]
    for i in range(ing_count):
        ing = Mock()
        ing.get_price.return_value = prices[i]
        empty_burger.add_ingredient(ing)

    assert empty_burger.get_price() == expected_price

# Проверки "get_receipt()"
# При N ингредиентах get_receipt возвращает строку ожидаемого формата
@pytest.mark.parametrize(
    "ing_count",
    [0, 1, 3],
    ids=["receipt_0_ing", "receipt_1_ing", "receipt_3_ing"]
)
def test_get_receipt_ingredients_count_n_returns_expected_format(empty_burger, ing_count):
    bun = Mock()
    bun.get_name.return_value = "Булочка"
    bun.get_price.return_value = 100
    empty_burger.set_buns(bun)

    ings = []
    total_price = 0

    for i in range(ing_count):
        ing = Mock()
        name = f"Ингредиент {i}"
        typ = "SAUCE" if i % 2 == 0 else "FILLING"
        price = 20 + i * 30
        ing.get_name.return_value = name
        ing.get_type.return_value = typ
        ing.get_price.return_value = price
        empty_burger.add_ingredient(ing)
        ings.append((name, typ))
        total_price += price

    receipt = empty_burger.get_receipt()
   
    lines = []
    lines.append(f"(==== {bun.get_name()} ====)")
    for name, typ in ings:
        lines.append(f"= {typ.lower()} {name} =")
    lines.append(f"(==== {bun.get_name()} ====)\n")

    expected_price = 2 * bun.get_price() + total_price
    lines.append(f"Price: {expected_price}")
    expected_string = "\n".join(lines)

    assert receipt == expected_string

# Проверки ошибок при отсутствии булочки
# Булочка не установлена → get_price выбрасывает AttributeError
def test_get_price_bun_none_raises_attribute_error(empty_burger):
    with pytest.raises(AttributeError):
        empty_burger.get_price()

# Булочка не установлена → get_receipt выбрасывает AttributeError
def test_get_receipt_bun_none_raises_attribute_error(empty_burger):
    with pytest.raises(AttributeError):
        empty_burger.get_receipt()
