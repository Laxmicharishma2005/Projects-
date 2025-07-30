class Expense:
    def __init__(self, name, category, amount, day):
        self.name = name
        self.category = category
        self.amount = amount
        self.day = day

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, ₹{self.amount:.2f}, Day {self.day}>"
