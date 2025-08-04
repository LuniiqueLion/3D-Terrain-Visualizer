import numpy as np
import matplotlib.pyplot as plt
import random

def generate_perlin_noise(width, height, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=None):
    if seed is not None:
        random.seed(seed)

    def interpolate(a0, a1, w):
        return (1.0 - w) * a0 + w * a1

    def smoothstep(t):
        return t * t * (3.0 - 2.0 * t)

    def generate_noise_point(x, y):
        X = int(x) & 255
        Y = int(y) & 255
        x -= int(x)
        y -= int(y)
        u = smoothstep(x)
        v = smoothstep(y)
        p00 = grad[P[P[X] + Y]]
        p10 = grad[P[P[X + 1] + Y]]
        p01 = grad[P[P[X] + Y + 1]]
        p11 = grad[P[P[X + 1] + Y + 1]]

        n00 = np.dot(p00, np.array([x, y]))
        n10 = np.dot(p10, np.array([x - 1, y]))
        n01 = np.dot(p01, np.array([x, y - 1]))
        n11 = np.dot(p11, np.array([x - 1, y - 1]))

        u = u * u * (3.0 - 2.0 * u)
        v = v * v * (3.0 - 2.0 * v)

        return interpolate(interpolate(n00, n10, u), interpolate(n01, n11, u), v)

    if seed is None:
        seed = random.randint(0, 1024)

    np.random.seed(seed)
    P = np.arange(0, 512, dtype=int)
    np.random.shuffle(P)
    P = np.stack([P, P]).flatten()

    grad = np.random.normal(size=(512, 2))

    terrain = []

    for i in range(width):
        row = []
        for j in range(height):
            value = 0.0
            for o in range(octaves):
                frequency = 2 ** o
                amplitude = persistence ** o
                value += generate_noise_point(i / scale * frequency, j / scale * frequency) * amplitude

            # Scale the value to be in the range [0, 50]
            scaled_value = (value + 1) * 25
            row.append(scaled_value)

        terrain.append(row)

    return terrain

def display_terrain(terrain):
    plt.imshow(terrain, cmap='terrain', interpolation='bilinear', vmax=50, vmin=0)
    plt.colorbar()
    plt.show()

# Example usage:
terrain = generate_perlin_noise(width=100, height=100, scale=20.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=42)
#display_terrain(terrain)
