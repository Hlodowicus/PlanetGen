import pyray as rl
from pyray import KeyboardKey as kb


class Cam:
    def __init__(self):
        self.core = rl.Camera3D(
            rl.Vector3(0.0, 3.0, 1.0),
            rl.Vector3(0.0, 2.0, 0.0),
            rl.Vector3(0.0, 1.0, 0.0),
            60.0,
            rl.CameraProjection(0)
        )
        self.movement = rl.Vector3()
        self.rotation = rl.Vector3()
        self.zoom = 0.0
        self.speed = 5
        self.sensitivity = 0.2

    def Update(self):
        mult = self.speed * rl.get_frame_time()

        self.movement.x = (rl.is_key_down(kb.KEY_W) - rl.is_key_down(kb.KEY_S)) * mult
        self.movement.y = (rl.is_key_down(kb.KEY_D) - rl.is_key_down(kb.KEY_A)) * mult
        self.movement.z = (rl.is_key_down(kb.KEY_SPACE) - rl.is_key_down(kb.KEY_C)) * mult

        self.rotation.x = rl.get_mouse_delta().x * self.sensitivity
        self.rotation.y = rl.get_mouse_delta().y * self.sensitivity

        rl.update_camera_pro(self.core, self.movement, self.rotation, self.zoom)