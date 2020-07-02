import d3dshot
import win32gui
import pyautogui
import gym
import numpy as np

class FNGym(gym.Env):
  '''
  Handles IO to the Fruit Ninja game. 
  '''

  def __init__(self):
    super().__init__()
    fn_hwnd = win32gui.FindWindow(None, 'Fruit Ninja')
    if fn_hwnd == 0:
      raise ValueError("Fruit Ninja window not detected!")
    self.win_coords = win32gui.GetWindowRect(fn_hwnd)
    
    # Add offest to not capture window
    self.win_coords = list(self.win_coords)
    self.win_coords[0] += 15
    self.win_coords[1] += 35
    self.win_coords[2] -= 25 
    self.win_coords[3] -= 35
    self.win_coords = tuple(self.win_coords)
    
    self.d3d_buff = d3dshot.create(capture_output='numpy')

  def reset(self):
    pass


  def step(self):
    pass

  def _get_score(self, raw_screenshot):
    score_area = raw_screenshot

  def _get_screenshot(self):
    return self.d3d_buff.screenshot(region=self.win_coords)


  def _start_game(self):
    pyautogui.moveTo(self.win_coords[0] + 400, self.win_coords[1] + 320)
    pyautogui.drag(200, 0, 0.2, button='left')

