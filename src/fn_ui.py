import d3dshot
import win32gui
import pyautogui

class FNUI:
  '''
  Handles IO to the Fruit Ninja game. 
  '''

  def __init__(self):
    fn_hwnd = win32gui.FindWindow(None, 'Fruit Ninja')
    if fn_hwnd == 0:
      raise ValueError("Fruit Ninja window not detected!")
    self.win_coords = win32gui.GetWindowRect(fn_hwnd)
    self.d3d_buff = d3dshot.create()


  def get_screenshot(self):
    return self.d3d_buff.screenshot(region=self.win_coords)


  def start_game(self):
    pyautogui.moveTo(self.win_coords[0] + 400, self.win_coords[1] + 340)
    pyautogui.drag(200, 0, 0.2, button='left')


