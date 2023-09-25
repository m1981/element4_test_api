from modules.dtos.billing_dto import BillingDto

def test_billing_dto_init():
    billing_dto = BillingDto('cash', 'Cash on delivery', '123')
    assert billing_dto.payment_method == 'cash'
    assert billing_dto.payment_method_title == 'Cash on delivery'
    assert billing_dto.transaction_id == '123'
