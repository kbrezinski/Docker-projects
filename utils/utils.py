
def land_transfer_calc(house_price):
    rate_dict = {
        30_000: 0.0,
        90_000: 0.005,
        150_000: 0.01,
        200_000: 0.015,
        200_001: 0.02,
    }
    tax = 0
    tax += 30_000 * rate_dict[30_000]
    tax += 60_000 * rate_dict[90_000]
    tax += 60_000 * rate_dict[150_000]
    tax += 50_000 * rate_dict[200_000]
    tax += (house_price - 200_000) * rate_dict[200_001]
    return tax
 
def compound_interest(principal, rate, years):
    home_value = []
    for year in range(years):
        home_value.append(principal * (1 + rate) ** year)
    return home_value
