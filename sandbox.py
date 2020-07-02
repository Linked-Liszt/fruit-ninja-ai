import fnai.fn_gym as fn_gym
import time
import numpy as np
from PIL import Image

test_gym = fn_gym.FNGym(0.2, False)
test_gym.reset()
obs, rew, done, info = test_gym.step(0)
print(np.shape(obs))
im = Image.fromarray(obs)
im.save('test.png')