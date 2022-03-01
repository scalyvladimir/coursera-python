from solution import *

car = Car('Bugatti Veyron', 'bugatti.png', '0.312', '2')

print(car.car_type, car.brand, car.photo_file_name, car.carrying,
      car.passenger_seats_count, sep='\n')

truck = Truck('Nissan', 'nissan.jpeg', '1.5', '3.92x2.09x1.87')

print(truck.car_type, truck.brand, truck.photo_file_name, truck.body_length,
      truck.body_width, truck.body_height, sep='\n')

spec_machine = SpecMachine('Komatsu-D355', 'd355.jpg', '93', 'pipelayer specs')

print(spec_machine.car_type, spec_machine.brand, spec_machine.carrying,
      spec_machine.photo_file_name, spec_machine.extra, sep='\n')

print(spec_machine.get_photo_file_ext())

cars = get_car_list('cars_week3.csv')

print(len(cars))

for car in cars:
    print(type(car))

print(cars[0].passenger_seats_count)

print(cars[1].get_body_volume())

l = all(['', '4', 'f1.jpeg', '2.5'])
print(l)
