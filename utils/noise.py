"""
3D Perlin noise implementation for world generation
"""

import math
import random
from typing import List

class PerlinNoise3D:
    """3D Perlin noise generator"""
    
    def __init__(self, seed: int = 0):
        self.seed = seed
        random.seed(seed)
        
        # Generate permutation table
        self.p = list(range(256))
        random.shuffle(self.p)
        self.p = self.p + self.p  # Duplicate for overflow
        
    def sample(self, x: float, y: float, z: float) -> float:
        """Sample noise at given 3D coordinates"""
        # Find unit cube that contains point
        X = int(math.floor(x)) & 255
        Y = int(math.floor(y)) & 255
        Z = int(math.floor(z)) & 255
        
        # Find relative x,y,z of point in cube
        x -= math.floor(x)
        y -= math.floor(y)
        z -= math.floor(z)
        
        # Compute fade curves for each of x,y,z
        u = self._fade(x)
        v = self._fade(y)
        w = self._fade(z)
        
        # Hash coordinates of 8 cube corners
        A = self.p[X] + Y
        AA = self.p[A] + Z
        AB = self.p[A + 1] + Z
        B = self.p[X + 1] + Y
        BA = self.p[B] + Z
        BB = self.p[B + 1] + Z
        
        # Add blended results from 8 corners of cube
        return self._lerp(w,
            self._lerp(v,
                self._lerp(u, self._grad(self.p[AA], x, y, z),
                             self._grad(self.p[BA], x - 1, y, z)),
                self._lerp(u, self._grad(self.p[AB], x, y - 1, z),
                             self._grad(self.p[BB], x - 1, y - 1, z))),
            self._lerp(v,
                self._lerp(u, self._grad(self.p[AA + 1], x, y, z - 1),
                             self._grad(self.p[BA + 1], x - 1, y, z - 1)),
                self._lerp(u, self._grad(self.p[AB + 1], x, y - 1, z - 1),
                             self._grad(self.p[BB + 1], x - 1, y - 1, z - 1))))
                             
    def _fade(self, t: float) -> float:
        """Fade function: 6t^5 - 15t^4 + 10t^3"""
        return t * t * t * (t * (t * 6 - 15) + 10)
        
    def _lerp(self, t: float, a: float, b: float) -> float:
        """Linear interpolation"""
        return a + t * (b - a)
        
    def _grad(self, hash_val: int, x: float, y: float, z: float) -> float:
        """Gradient function"""
        h = hash_val & 15  # Take the hashed value and take the first 4 bits of it
        u = x if h < 8 else y  # If the most significant bit (MSB) of the hash is 0 then set u = x.  Otherwise y.
        
        if h < 4:
            v = y
        elif h == 12 or h == 14:
            v = x
        else:
            v = z
            
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)
        
    def octave_noise(self, x: float, y: float, z: float, octaves: int = 4, 
                    persistence: float = 0.5, lacunarity: float = 2.0) -> float:
        """Generate octave noise (fractal noise)"""
        value = 0.0
        amplitude = 1.0
        frequency = 1.0
        max_value = 0.0
        
        for _ in range(octaves):
            value += self.sample(x * frequency, y * frequency, z * frequency) * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= lacunarity
            
        return value / max_value
