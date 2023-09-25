from modules.dtos.line_item_dto import LineItemDto

def test_line_item_dto_init():
    line_item_dto = LineItemDto('Item1', 1, 15.0, 1.5, False, "Na miejscu")
    assert line_item_dto.item_name == 'Item1'
    assert line_item_dto.quantity == 1
    assert line_item_dto.total == 15.0
    assert line_item_dto.total_tax == 1.5
    assert line_item_dto.is_vat_exempt == False
    assert line_item_dto.na_miejscu_na_wynos == "Na miejscu"
