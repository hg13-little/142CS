class Vehicle:
    def __init__(self, name, fuel_capacity, cost_per_gallon, miles_per_gallon):
        self._name = name
        self._fuel_capacity = fuel_capacity
        self._cost_per_gallon = cost_per_gallon
        self._miles_per_gallon = miles_per_gallon

    @property
    def name (self):
        return self._name
    
    @property
    def range(self):
        return self._fuel_capacity * self._miles_per_gallon
    
    @property
    def cost_per_gallon(self):
        return self._cost_per_gallon / self._miles_per_gallon
    
# Create at least 4 vehicles
v1 = Vehicle("Car", 15, 3.50, 30)
v2 = Vehicle("Motorcycle", 4, 3.50, 55)
v3 = Vehicle("Bus", 100, 3.50, 6)
v4 = Vehicle("Airplane", 5000, 5.00, 0.2)
v5 = Vehicle("Truck", 30, 3.50, 15)

vehicles = [v1, v2, v3, v4]

# Sort by cost per mile
vehicles_sorted = sorted(vehicles, key=lambda v: v.cost_per_mile)

# Print table header
print(f"{'Name':<15}{'Range (miles)':<20}{'Cost per mile ($)':<20}")
print("-" * 55)

# Print each vehicle's data
for v in vehicles_sorted:
    print(f"{v.name:<15}{v.range:<20}{v.cost_per_mile:<20.4f}")
    