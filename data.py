from datetime import timezone, datetime


class Categories:
    CARS = {'id': 0, 'name': 'Cars'}
    ELECTRONICS = {'id': 1, 'name': 'Electronics'}
    GAMES = {'id': 2, 'name': 'Games'}
    DICT = {0: CARS, 1: ELECTRONICS, 2: GAMES}


class Colors:
    RED = {'id': 0, 'name': 'Red'}
    GREEN = {'id': 1, 'name': 'Green'}
    BLUE = {'id': 2, 'name': 'Blue'}
    DICT = {0: RED, 1: GREEN, 2: BLUE}


class Products:
    MAZDA = {
        'id': 0,
        'name': 'Mazda',
        'description': 'No reviews yet',
        'amount': 1,
        'category': Categories.CARS,
        'color': Colors.RED,
        'created': datetime.now(timezone.utc).isoformat(),
    }
    DICT = {0: MAZDA}
