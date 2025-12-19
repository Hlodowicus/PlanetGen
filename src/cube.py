import numpy as np
import pyray as rl
import pyfastnoiselite.pyfastnoiselite as fnl
from pyfastnoiselite.pyfastnoiselite import NoiseType, FractalType
import ctypes

def vec3_key(v: rl.Vector3):
    return round(v.x, 5), round(v.y, 5), round(v.z, 5)


class Cube:
    def __init__(self, center: rl.Vector3, resolution: int, radius: float):
        self.resolution = resolution
        self.tmp_vertices: list[rl.Vector3] = []
        self.faces: dict[int, list[list[rl.Vector3]]] = {}

        self.vertices: list[float] = []
        self.indices: list[int] = []

        # Initialisation du bruit 1
        self.noise = fnl.FastNoiseLite(seed=42)
        self.noise.noise_type = fnl.NoiseType(NoiseType.NoiseType_Perlin)
        self.noise.frequency = 2.4
        self.noise.fractal_type = fnl.FractalType(FractalType.FractalType_FBm)
        self.noise.fractal_lacunarity = 4.1
        self.noise.fractal_octaves = 2

        #Init du bruit 2
        self.noise2 = fnl.FastNoiseLite(seed=42)
        self.noise2.noise_type = fnl.NoiseType(NoiseType.NoiseType_Perlin)
        self.noise2.frequency = 0.4

        for face in range(6):
            tmp_face = [[rl.Vector3() for j in range(resolution)] for i in range(resolution)]
            for y in range(resolution):
                for x in range(resolution):
                    u = x / (resolution - 1) * 2.0 - 1.0
                    v = y / (resolution - 1) * 2.0 - 1.0

                    p = rl.vector3_zero()

                    match face:
                        case 0:
                            p = rl.Vector3(1.0, v, -u)
                        case 1:
                            p = rl.Vector3(-1.0, v, u)
                        case 2:
                            p = rl.Vector3(u, 1.0, -v)
                        case 3:
                            p = rl.Vector3(u, -1.0, v)
                        case 4:
                            p = rl.Vector3(u, v, 1.0)
                        case 5:
                            p = rl.Vector3(-u, v, -1.0)

                    n = rl.vector3_normalize(p)

                    # noise
                    noise_val = self.noise.get_noise(n.x * 3.0, n.y * 3.0, n.z * 3.0)
                    noise_val2 = self.noise2.get_noise(n.x * 3.0, n.y * 3.0, n.z * 3.0)

                    elevation = 1.0 + noise_val * 0.05 + noise_val2 * 0.05  # 20% de variation

                    pos = rl.vector3_scale(n, radius * elevation)

                    pos = rl.vector3_add(center, pos)

                    self.tmp_vertices.append(pos)
                    tmp_face[x][y] = pos

            self.faces[face] = tmp_face

    def BuildMesh(self):
        tmp_vertices = {}

        for face, arr in self.faces.items():
            for vertices in arr:
                for vertex in vertices:
                    if not(face in tmp_vertices):
                        tmp_vertices[face] = []

                    tmp_vertices[face].append(vertex.x)

        for face_id, grid in self.faces.items():
            for y in range(self.resolution - 1):
                for x in range(self.resolution - 1):
                    v1 = grid[y][x]
                    v2 = grid[y][x + 1]
                    v3 = grid[y + 1][x]
                    v4 = grid[y + 1][x + 1]


    def Update(self):
        pass

    def Draw(self):
        # for v in self.vertices:
        #     rl.draw_cube_v(v, rl.Vector3(0.001, 0.001, 0.001), rl.RED)

        for face_id, grid in self.faces.items():
            for y in range(self.resolution - 1):
                for x in range(self.resolution - 1):
                    v1 = grid[y][x]
                    v2 = grid[y][x + 1]
                    v3 = grid[y + 1][x]
                    v4 = grid[y + 1][x + 1]

                    rl.draw_line_3d(v1, v2, rl.BLUE)
                    rl.draw_line_3d(v1, v3, rl.BLUE)
                    rl.draw_line_3d(v2, v4, rl.BLUE)
                    rl.draw_line_3d(v3, v4, rl.BLUE)

                    #rl.draw_triangle_3d(v3, v2, v1, rl.GRAY)
                    #rl.draw_triangle_3d(v3, v4, v2, rl.GRAY)

        #rl.draw_model(self.model, rl.vector3_zero(), 1.0, rl.GRAY)