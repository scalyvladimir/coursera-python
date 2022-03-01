from os.path import splitext
from csv import reader


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return splitext(self.photo_file_name)[-1]


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = self.__class__.__name__.lower()
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = self.__class__.__name__.lower()

        result = [0.0] * 3
        try:
            params_list = body_whl.split('x')
            params_list = [float(x) for x in params_list]
            if len(params_list) == 3:
                result = params_list
        except ValueError:
            pass

        self.body_length, self.body_width, self.body_height = result
        print(self.body_length, self.body_width, self.body_height, sep='x')

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'spec_machine'
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(file=csv_filename, encoding='utf-8') as csv_fd:
        reader_obj = reader(csv_fd, delimiter=';')
        # Skip header
        next(reader_obj)
        for row in reader_obj:
            try:
                car_obj = None
                car = row[0]
                args = row[1:]

                if car == 'car':
                    temp = [args[0], args[1], args[2], args[4]]
                    if all(temp):
                        car_obj = Car(brand=args[0], passenger_seats_count=args[1],
                                      photo_file_name=args[2], carrying=args[4])
                elif car == 'spec_machine':
                    temp = [args[0], args[2], args[4], args[5]]
                    if all(temp):
                        car_obj = SpecMachine(brand=args[0], photo_file_name=args[2],
                                              carrying=args[4], extra=args[5])
                elif car == 'truck':
                    temp = [args[0], args[2], args[4]]
                    if all(temp):
                        car_obj = Truck(brand=args[0], photo_file_name=args[2],
                                        carrying=args[4], body_whl=args[3])

                if car_obj is not None and car_obj.get_photo_file_ext() in ['.jpg', '.jpeg', '.png', '.gif']:
                    car_list.append(car_obj)
                    car_obj = None

            except IndexError:
                pass
            except ValueError:
                pass
    return car_list
