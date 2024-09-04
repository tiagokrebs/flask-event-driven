class Order:
    def __init__(self, order_id, user_id, body):
        self.order_id = order_id
        self.user_id = user_id
        self.body = body

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "body": self.body
        }