import fnai.fn_gym as fn_gym
import time
import numpy as np
from PIL import Image

test_gym = fn_gym.FNGym(0.2, False)
test_gym.reset()
obs, rew, done, info = test_gym.step([1.0, 1.0, 1.0])
Image.fromarray(obs).save('test.png')