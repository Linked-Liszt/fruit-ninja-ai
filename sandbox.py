import fnai.fn_gym as fn_gym
import time
import numpy as np
from PIL import Image

test_gym = fn_gym.FNGym()
test_gym._start_game()
time.sleep(0.5)
test_sc = test_gym._get_screenshot()
test_sc = test_sc[:33, 30:150, :]
im = Image.fromarray(test_sc)
im.save('test.png')
test_gym._get_score(test_sc)
print(np.shape(test_sc))