from app import db
from objects import Customer, Order, Product

def db_init():
    
    db.create_all()
    customer1 = Customer(name='Sandro Ephrem', address='Mansourieh, Bedran Street Yazbeck Hammouche 10', countryCode=961, email='sandro.ephrem@gmail.com')
    customer2 = Customer(name='Maroun Ayli', address='Bsaba, Mtoll Street Anibal Abi Antoun Bdlg', countryCode=961, email='marounayle@gmail.com')
    customer3 = Customer(name='Joe Biden', address='The White House 1600 Pennsylvania Avenue NW Washington, DC 20500',
                            countryCode=1, email='joseph.biden@usa.gov')

    product1 = Product(productDescription='Nvidia Geforce RTX 3090', pricePerUnit=700, currency='USD', quantityAvailable=5)

    db.session.add(customer1)
    db.session.add(customer2)
    db.session.add(customer3)

    db.session.add(product1)

    db.session.commit()
