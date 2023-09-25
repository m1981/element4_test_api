class BillingDto:
    def __init__(self, payment_method, payment_method_title, transaction_id):
        self.payment_method = payment_method
        self.payment_method_title = payment_method_title
        self.transaction_id = transaction_id
