import fnai.fn_gym as fn_gym
import time
import numpy as np
from PIL import Image

test_gym = fn_gym.FNGym(0.2)
init_img = test_gym.reset()
for i in range(500):
    screenshot = test_gym.d3d_buff.screenshot(region=test_gym.win_coords)
    print(screenshot[25, 10, 0])

"""
print(np.shape(init_img))
obs, rew, done, info = test_gym.step([1.0, 1.0, 1.0])
print(np.shape(obs))
Image.fromarray(obs).save('test.png')
"""