import cv2
import d3dshot
import gym
import numpy as np
import pyautogui
import time
import win32gui

class FNGym(gym.Env):
  '''
  Handles IO to the Fruit Ninja game. 

  Params:
    obs_scale: (float) the downscaling factor of the observation
    obs_color: (bool) true to use all 3 color channels, or 
      false to convert into single chanel
  '''

  def __init__(self, obs_scale, is_obs_color):
    super().__init__()

    fn_hwnd = win32gui.FindWindow(None, 'Fruit Ninja')
    if fn_hwnd == 0:
      raise ValueError("Fruit Ninja window not detected!")
    self.win_coords = win32gui.GetWindowRect(fn_hwnd)
    
    # Add offest to not capture window controls
    self.win_coords = list(self.win_coords)
    self.win_coords[0] += 15
    self.win_coords[1] += 35
    self.win_coords[2] -= 25 
    self.win_coords[3] -= 35
    self.win_coords = tuple(self.win_coords)

    self.d3d_buff = d3dshot.create(capture_output='numpy')
  
    self.is_obs_color = is_obs_color
    self._calculate_obs_size(obs_scale)
    self.observation_space = gym.spaces.Box(low=0, high=255, shape=
      (self.obs_size[0], self.obs_size[1], self.obs_size[2]), dtype=np.uint8)

  def reset(self):
    self._start_game()
    time.sleep(0.5)


  def step(self, action):
    observation = self._get_observation() 
    reward = None
    done = None
    info = None

    return observation, reward, done, info
  

  def _get_observation(self):
    raw_screenshot = self.d3d_buff.screenshot(region=self.win_coords)
    scaled_screenshot = cv2.resize(raw_screenshot, (self.obs_size[0], self.obs_size[1]), interpolation=cv2.INTER_CUBIC)
    if self.is_obs_color:
      return scaled_screenshot
    else:
      return cv2.cvtColor(scaled_screenshot, cv2.COLOR_BGR2GRAY)

  def _calculate_obs_size(self, obs_scale):
    x_size = round((self.win_coords[2] - self.win_coords[0]) * obs_scale)
    y_size = round((self.win_coords[3] - self.win_coords[1]) * obs_scale)
    if self.is_obs_color:
      layers = 3
    else:
      layers = 1
    self.obs_size = [x_size, y_size, layers]


  def _start_game(self):
    pyautogui.moveTo(self.win_coords[0] + 400, self.win_coords[1] + 320)
    pyautogui.drag(200, 0, 0.2, button='left')

