from dragline.item import Item, TextField, JSONField


class Hoteldata(Item):
	ID = TextField()
	property_id = TextField()
	hotel_name = TextField()
	check_in_date = TextField()
	price = TextField()
	rate_type = TextField()
	url = TextField()
