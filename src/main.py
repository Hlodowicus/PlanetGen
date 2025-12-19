from pyray import *
from src.cam import Cam
from src.cube import Cube

init_window(0, 0, "planet")
set_target_fps(60)
toggle_fullscreen()
disable_cursor()

cam = Cam()

cube = Cube(Vector3(0.0, 0.0, 0.0), 50, 3.0)

while not window_should_close():
    #UPDATE
    cam.Update()

    #DRAW
    begin_drawing()
    clear_background(BLACK)
    begin_mode_3d(cam.core)
    #draw_grid(10, 1)
    cube.Draw()
    end_mode_3d()
    #draw_fps(10, 10)
    end_drawing()

close_window()