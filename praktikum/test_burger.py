from unittest.mock import Mock
import pytest

from praktikum.burger import Burger


# Проверки "__init__"
# Проверка: после инициализации булочка должна отсутствовать (None)
def test_burger_bun_is_none_after_init():
    burger = Burger()
    assert burger.bun is None

# Проверка: список ингредиентов пустой после создания объекта
def test_burger_ingredients_list_is_empty():
    burger = Burger()
    assert len(burger.ingredients) == 0

# Проверки "set_buns"
# Проверка: set_buns корректно присваивает булочку
def test_set_buns_assigns_bun_correctly(empty_burger):
    mock_bun = Mock()
    empty_burger.set_buns(mock_bun)
    assert empty_burger.bun is mock_bun

# Проверка: set_buns сохраняет последнюю добавленную булочку (перезаписывает предыдущую)
def test_set_buns_overwrites_previous_bun(empty_burger):
    old_bun = Mock()
    new_bun = Mock()
    empty_burger.set_buns(old_bun)
    empty_burger.set_buns(new_bun)
    assert empty_burger.bun is new_bun

# Проверки "add_ingredient"
# Проверка: после добавления длина списка ингредиентов увеличивается на указанное количество
@pytest.mark.parametrize("count", [1, 3])
def test_add_ingredient_increases_count(empty_burger, count):
    start_len = len(empty_burger.ingredients)
    for _ in range(count):
        empty_burger.add_ingredient(Mock())
    assert len(empty_burger.ingredients) == start_len + count

# Проверка: ингредиент добавляется в конец списка (сохраняется ссылка на переданный объект)
def test_add_ingredient_adds_exact_object(empty_burger):
    ingredient = Mock()
    empty_burger.add_ingredient(ingredient)
    assert empty_burger.ingredients[-1] is ingredient

# Проверка: ингредиенты добавляются в корректном порядке (порядок вставки сохраняется)
def test_add_multiple_ingredients_maintains_order(empty_burger):
    ing1, ing2, ing3 = Mock(), Mock(), Mock()
    empty_burger.add_ingredient(ing1)
    empty_burger.add_ingredient(ing2)
    empty_burger.add_ingredient(ing3)
    assert empty_burger.ingredients == [ing1, ing2, ing3]

# Проверка: "move_ingredient"
# Проверка: move_ingredient перемещает элемент на указанный индекс
@pytest.mark.parametrize("from_idx,to_idx", [
    (0, 1), (1, 0), (0, 0), (2, 0), (0, 2),],
    ids=["shift_forward",
        "shift_backward",
        "same_index",
        "from_end_to_start",
        "from_start_to_end"]
    )
def test_move_ingredient_shifts_element(burger_three_ingredients, from_idx, to_idx):
    burger, _, _, _, _ = burger_three_ingredients
    original = burger.ingredients[:]

    burger.move_ingredient(from_idx, to_idx)

    expected = original[:]
    item = expected.pop(from_idx)
    expected.insert(to_idx, item)

    assert burger.ingredients == expected

# Проверка: неверный индекс источника вызывает ошибку IndexError
def test_move_ingredient_raises_on_invalid_source_index(burger_three_ingredients):
    burger, _, _, _, _ = burger_three_ingredients
    with pytest.raises(IndexError):
        burger.move_ingredient(99, 0)

# Проверка "remove_ingredient"
# Проверка: после удаления ингредиента длина списка уменьшается согласно ожидаемому значению
@pytest.mark.parametrize("remove_idx,expected_len", [
    (0, 2), (1, 2), (2, 2)
    ],
    ids=["remove_first", "remove_middle", "remove_last"]
)
def test_remove_ingredient_decreases_count(burger_three_ingredients, remove_idx, expected_len):
    burger, _, _, _, _ = burger_three_ingredients
    burger.remove_ingredient(remove_idx)
    assert len(burger.ingredients) == expected_len

# Проверка: при попытке удаления из пустого списка вызывает ошибка IndexError
def test_remove_from_empty_list_raises_index_error(empty_burger):
    with pytest.raises(IndexError):
        empty_burger.remove_ingredient(0)

# Проверка: при неверном индексе выбрасывается IndexError
def test_remove_invalid_index_raises_error(burger_three_ingredients):
    burger, _, _, _, _ = burger_three_ingredients
    with pytest.raises(IndexError):
        burger.remove_ingredient(99)

# Проверка "get_price()"
# Проверка: get_price корректно рассчитывает стоимость бургера с разным количеством ингредиентов
@pytest.mark.parametrize("ing_count,expected_price", [(0, 200), (1, 220), (3, 340)])
def test_get_price_parametrized(empty_burger, ing_count, expected_price):
    bun = Mock()
    bun.get_price.return_value = 100
    empty_burger.set_buns(bun)

    prices = [20, 50, 70]
    for i in range(ing_count):
        ing = Mock()
        ing.get_price.return_value = prices[i]
        empty_burger.add_ingredient(ing)

    assert empty_burger.get_price() == expected_price

# Проверка "get_receipt()"
# Проверка: get_receipt формирует корректный текст чека с ингредиентами и итоговой ценой
@pytest.mark.parametrize("ing_count", [0, 1, 3])
def test_get_receipt_format_and_price(empty_burger, ing_count):
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
    # Ингредиенты
    for name, typ in ings:
        lines.append(f"= {typ.lower()} {name} =")
    lines.append(f"(==== {bun.get_name()} ====)\n")

    expected_price = 2 * bun.get_price() + total_price
    lines.append(f"Price: {expected_price}")
    expected_string = "\n".join(lines)

    assert receipt == expected_string

# Проверка: get_price выбрасывает AttributeError, если булочка не установлена
def test_get_price_raises_attribute_error_if_bun_is_none(empty_burger):
    with pytest.raises(AttributeError):
        empty_burger.get_price()

# Проверка: get_receipt выбрасывает AttributeError, если булочка не установлена
def test_get_receipt_raises_attribute_error_if_bun_is_none(empty_burger):
    with pytest.raises(AttributeError):
        empty_burger.get_receipt()
        