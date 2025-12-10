
def house(name, age, address, city, country):
    """
    :param name:
    :param age:
    :param address:
    :param city:
    :param country:
    :return:
    """
    def identity():
        print(f"name:{name}, age:{age}, address:{address}, city:{city}, country:{country}")

    def cook(recipe):
        return f"{name} cooking :{recipe} in kitchen"

    def sleep():
        return f"{name} sleeping in bedroom"

    def walk():
        return f"{name} walking in the hall"

    attributes = {
        "name": name,
        "age": age,
        "address": address,
        "city": city,
        "country": country
    }

    return attributes, identity, cook, sleep, walk

p_attributes, p_identity, p_cook, p_sleep, p_walk = house("Prudhvi", 40, "123 Main St", "New York", "USA")
print(p_attributes)
p_identity()
print(p_cook("Dal Makhani"))
print(p_sleep())
print(p_walk())
print("---------------------")
r_attributes, r_identity, r_cook, r_sleep, r_walk = house("Ravi", 35, "124 Main St", "New York",country="USA")
print(r_attributes)
print(r_identity())
print(r_cook("Fried Rice"))
print(r_sleep())
print(r_walk())

class House:
    def __init__(self,name, age, address, city, country):
        print("value of self",self)
        self.name = name
        self.age = age
        self.address = address
        self.city = city
        self.country = country

    def identity(self):
        return f"name:{self.name}, age:{self.age}, address:{self.address}, city:{self.city}, country:{self.country}"

    def cook(self, recipe):
        return f"{self.name} cooking :{recipe} in kitchen"


prudhvi = House("Prudhvi", 40, "123 Main St", "New York", "USA")
print(prudhvi.name,prudhvi.age,prudhvi.address,prudhvi.city,prudhvi.country)
print(prudhvi.identity())
print(prudhvi.cook("Dal Makhani"))
###########
ravi = House("Ravi", 42, "123 Main St", "New York", "USA")
print(ravi.name,ravi.age,ravi.address,ravi.city,ravi.country)
print(ravi.identity())
print(ravi.cook("Fried Rice"))