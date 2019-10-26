
class Car:
    def __init__(self, trim, paint, interior, price, vin):
        self.trim = trim
        self.paint = paint
        self.interior = interior
        self.price = price
        self.vin = vin

    def __str__(self):
        return '{} {} with {} interior for £{}'.format(self.paint, self.trim, self.interior, self.price)

    def __eq__(self, other):
        return self.trim == other.trim and self.paint == other.paint and self.interior == other.interior and self.price == other.price

