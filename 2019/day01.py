from aoc_components.input_getter import get_my_list

modules = get_my_list(2019, 1, t=int)


def fuel(mass):
    return int(mass/3)-2


def fuel_recursive(mass):
    total = 0
    while True:
        mass = fuel(mass)
        if mass <= 0:
            return total
        total += mass

fuel_for_modules = sum((fuel(m) for m in modules))
print("fuel for all modules:" + str(fuel_for_modules))  # 3_421_505

fuel_for_modules_and_fuel = sum((fuel_recursive(m) for m in modules))
print("fuel for all modules+fuel:" + str(fuel_for_modules_and_fuel))  # 5_129_386


wrong = [(5_132_213, "too big"), (15_394_612, "to big"),

         (3_421_505, "too small")]
