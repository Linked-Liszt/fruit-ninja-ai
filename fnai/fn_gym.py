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

  def __init__(self, obs_scale, is_obs_color=True, reward_score=True):
    super().__init__()
    self.reward_score = reward_score

    fn_hwnd = win32gui.FindWindow(None, 'Fruit Ninja')
    if fn_hwnd == 0:
      raise ValueError("Fruit Ninja window not detected!")
    self.win_coords = win32gui.GetWindowRect(fn_hwnd)
    
    # Add offest to not capture window controls
    self.win_coords = list(self.win_coords)
    self.win_coords[0] += 15
    self.win_coords[1] += 35
    self.win_coords[2] -= 35 
    self.win_coords[3] -= 35
    self.win_coords = tuple(self.win_coords)

    self.d3d_buff = d3dshot.create(capture_output='numpy')
  
    self.is_obs_color = is_obs_color
    self._calculate_obs_size(obs_scale)
    self.observation_space = gym.spaces.Box(low=0, high=255, shape=
      (self.obs_size[1], self.obs_size[0], self.obs_size[2]), dtype=np.uint8)
    self.action_space = gym.spaces.Box(low=np.array([0.0, 0.0]), 
      high=np.array([1.0, 1.0]), dtype=np.float32)
    
    self.passoff_time = time.time()

  def reset(self):
    time.sleep(4.0)
    self.done_counter = 0
    self._start_game()
    time.sleep(0.5)
    raw_screenshot = self.d3d_buff.screenshot(region=self.win_coords)
    if self.reward_score:
      self.last_score = raw_screenshot[:33, 30:150, :]
    return self._get_observation(raw_screenshot)


  def step(self, action):
    curr_time = time.time()
    self._make_swipe(action)
    time_diff = self.passoff_time - curr_time
    
    raw_screenshot = self.d3d_buff.screenshot(region=self.win_coords)
    observation = self._get_observation(raw_screenshot) 
    done = self._is_done(raw_screenshot)
    info = {'time_diff': time_diff}
    self.passoff_time = time.time()

    if self.reward_score:
      if self._has_score_changed(raw_screenshot):
        reward = 1.0
      else:
        reward = 0.0
    else:
      reward = 1.0


    print(f'Reward: {reward} | Time Passed: {time_diff}')
    return observation, reward, done, info
  
  def _make_swipe(self, action):
    pix_x = self.win_coords[0] + round((self.win_coords[2] - self.win_coords[0]) * action[0])
    
    pix_y = self.win_coords[1] + round((self.win_coords[3] - self.win_coords[1]) * action[1])

    # Restrict from moving off screen
    #pix_x = min(pix_x, self.win_coords[2] - 150)
    pix_y = max(pix_y, self.win_coords[1] + 160)

    # Restrict from hitting score area
    if pix_x < self.win_coords[0] + 165 and pix_y < self.win_coords[1] + 200:
      pix_y = self.win_coords[1] + 200

    pyautogui.moveTo(pix_x, pix_y)
    pyautogui.drag(0, -150, duration=0.17, button='left')
  

  def _has_score_changed(self, raw_screenshot):
    current_score = raw_screenshot[:33, 30:150, :]
    diff = np.sum(cv2.subtract(self.last_score, current_score))
    self.last_score = current_score
    return diff > 10000


  def _get_observation(self, raw_screenshot):
    scaled_screenshot = cv2.resize(raw_screenshot, (self.obs_size[0], self.obs_size[1]), interpolation=cv2.INTER_CUBIC)
    if self.is_obs_color:
      return scaled_screenshot
    else:
      return cv2.cvtColor(scaled_screenshot, cv2.COLOR_BGR2GRAY)
    
  def _is_done(self, raw_screenshot):
    """
    Analyze a a pixel insdie of the 3 x's to see if it turns red. 
    Since fruits can overlay the UI, wait a 3 consecutive interactions. 
    """
    return raw_screenshot[27,-12,0] > 160 or raw_screenshot[25, 10, 0] < 80
    """
    if raw_screenshot[27,-12,0] > 160:
      if self.done_counter > 1:
        return True
      else:
        self.done_counter += 1
    else:
      self.done_counter = 0
    return False
    """

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

