import fnai.fn_gym as fn_gym
import time
import numpy as np
from PIL import Image

test_gym = fn_gym.FNGym(0.2, False)
for i in range(1):
    test_gym.reset()
    for i in range(200):
        obs, rew, done, info = test_gym.step([1.0, 1.0, 1.0])
        print(done)
        if done:
            break