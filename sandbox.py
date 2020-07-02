import fnai.fn_gym as fn_gym
import time
import numpy as np
from PIL import Image

test_gym = fn_gym.FNGym()
test_gym._start_game()
time.sleep(0.5)

old_sc = None
sc_counter = 0
for _ in range(900):
    new_sc = test_gym._get_screenshot()
    new_sc = new_sc[:33, 30:150, :]
    time.sleep(1)
    if old_sc is None or not (old_sc == new_sc).all():
        im = Image.fromarray(new_sc)
        im.save(f'test{sc_counter}.png')
        old_sc = new_sc
        sc_counter += 1