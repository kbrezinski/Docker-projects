
import numpy as np
import matplotlib.pyplot as plt

prizes = {
    8: 0,
    81: 5, # extra 1
    57: 10,
    1_033: 99,
    55_492: 1410,
    2_330_636: 187_229, # extra 2
    5_045_344: 3_430_000, # accounts for golden ball chance
    13_983_816: 5_000_000,
}
week_prizes = set(prizes.keys())

#num_iter = int(1e7)
num_iter = 4420

for with_extra in [True, False]:
    curr_balance = 0
    for week in range(num_iter):
        curr_balance -= 4 if with_extra else 3
        if week in week_prizes:
            if not with_extra and week in [81, 2_330_636]:
                continue
            curr_balance += prizes[week]
    print(f"{with_extra=} | {curr_balance / num_iter:.4f}")


from random import randint

iter = int(1e7)
payout = 0
winning_sum = 0
balls = 30

for i in range(iter):
    if randint(0, balls) == 0:
        # gold ball
        winning_sum += payout + 10_000_000
        payout = 0
        balls = 30
    else:
        # white ball
        winning_sum += 1_000_000
        payout += 2_000_000
        balls -= 1

    if not i % (iter // 5):
        print(f"{i=} | {winning_sum / (i + 1):.2f}")