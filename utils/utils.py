
from utils.constants import *

def land_transfer_calc(house_price): 
    tax = 0
    tax += 30_000 * land_transfer_dict[30_000]
    tax += 60_000 * land_transfer_dict[90_000]
    tax += 60_000 * land_transfer_dict[150_000]
    tax += 50_000 * land_transfer_dict[200_000]
    tax += (house_price - 200_000) * land_transfer_dict[200_001]
    return tax
 
def compound_interest(principal, rate, years):
    home_value = []
    for year in range(1, years + 1):
        home_value.append(principal * (1 + rate) ** year)
    return home_value

