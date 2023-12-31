class TreeViewDataFormatter:
    def __init__(self):
        pass

    @staticmethod
    def format_data_for_display(order_dto):
        formatted_data = []
        for item_dto in order_dto.line_items:
            price = (float(item_dto.total) + float(item_dto.total_tax)) * item_dto.quantity
            formatted_price = '{:.2f} PLN'.format(price)


            placing = ' | '.join([item.split(' ')[1] for item in item_dto.na_miejscu_na_wynos])
            formatted_data.append((item_dto.item_name, item_dto.quantity, placing, formatted_price))
        return formatted_data