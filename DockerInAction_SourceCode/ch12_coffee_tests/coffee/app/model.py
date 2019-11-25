from . import db
from exceptions import ValidationError

class CoffeeShop(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    max_seats = db.Column(db.Integer, nullable=False)
    power = db.Column(db.Boolean, nullable=False, default=False)
    wifi = db.Column(db.Boolean, nullable=False, default=False)

    def to_json(self):
        json_coffeeshop = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'zipcode': self.zipcode,
            'price': self.price,
            'max_seats': self.max_seats,
            'power': self.power,
            'wifi': self.wifi
        }
        return json_coffeeshop

    @staticmethod
    def from_json(json_coffeeshop):
        if json_coffeeshop is None:
            raise ValidationError('json body must be provided')

        name = json_coffeeshop.get('name')
        if name is None or name == '' or len(name) > 120:
            raise ValidationError('name must be specified, not blank, and fewer than 121 characters')

        address = json_coffeeshop.get('address')
        if address is None or address == '' or len(address) > 300:
            raise ValidationError('address must be specified, not blank, and fewer than 301 characters')

        zipcode = json_coffeeshop.get('zipcode')
        try:
            zipcode = int(zipcode)
        except (TypeError, ValueError) as e:
            raise ValidationError('zipcode must be specified and a valid number')
        if zipcode < 1:
            raise ValidationError('zipcode must be greater than 0')

        price = json_coffeeshop.get('price')
        try:
            price = int(price)
        except (TypeError, ValueError) as e:
            raise ValidationError('price must be specified and a valid number')
        if price < 1 or price > 5:
            raise ValidationError('price must be between 1 and 5')
 
        max_seats = json_coffeeshop.get('max_seats')
        try:
            max_seats = int(max_seats)
        except (TypeError, ValueError) as e:
            raise ValidationError('max_seats must be specified and a valid number')
        if max_seats < 1:
            raise ValidationError('max_seats must be greater than 0')

        power = json_coffeeshop.get('power')
        try:
            power = bool(power)
        except (TypeError, ValueError) as e:
            raise ValidationError('power must be specified and either true or false')

        wifi = json_coffeeshop.get('wifi')
        try:
            wifi = bool(wifi)
        except (TypeError, ValueError) as e:
            raise ValidationError('wifi must be specified and either true or false')

        return CoffeeShop(name=name, address=address, zipcode=zipcode, price=price, max_seats=max_seats, power=power, wifi=wifi) 
