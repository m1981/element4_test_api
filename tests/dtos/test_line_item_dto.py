from modules.dtos.line_item_dto import LineItemDto

def test_line_item_dto_init():
    line_item_dto = LineItemDto('Item1', 2, 15.0, 1.5, ['Na miejscu', 'Na wynos'])
    assert line_item_dto.item_name == 'Item1'
    assert line_item_dto.quantity == 2
    assert line_item_dto.total == 15.0
    assert line_item_dto.total_tax == 1.5
    assert "Na miejscu" == line_item_dto.na_miejscu_na_wynos[0]
    assert "Na wynos" == line_item_dto.na_miejscu_na_wynos[1]
