import d3dshot
import win32gui

class FNUI:
  def __init__(self):
    fn_hwnd = win32gui.FindWindow(None, 'Fruit Ninja')

    if fn_hwnd == 0:
      raise ValueError("Fruit Ninja window not detected!")

    self.win_coords = win32gui.GetWindowRect(fn_hwnd)
  
    self.d3d_buff = d3dshot.create()

  def capture_screenshot(self):
    #self.d3d_buff.screenshot(region=self.win_coords)
    self.d3d_buff.screenshot_to_disk(region=self.win_coords)

