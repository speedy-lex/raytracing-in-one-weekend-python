from random import uniform, random
from math import sqrt

class Vec3:
    def __init__(self, x, y=None, z=None) -> None:
        if isinstance(x, (tuple, list)):
            self.x, self.y, self.z=x
        elif y==None:
            self.x, self.y, self.z=x, x, x
        else:
            self.x=x
            self.y=y
            self.z=z
    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)
    def __add__(self, vec):
        if isinstance(vec, Vec3):
            return Vec3(self.x+vec.x, self.y+vec.y, self.z+vec.z)
        else:
            return Vec3(self.x+vec, self.y+vec, self.z+vec)
    def __sub__(self, vec):
        if isinstance(vec, Vec3):
            return Vec3(self.x-vec.x, self.y-vec.y, self.z-vec.z)
        else:
            return Vec3(self.x-vec, self.y-vec, self.z-vec)
    def __mul__(self, vec):
        if isinstance(vec, Vec3):
            return Vec3(self.x*vec.x, self.y*vec.y, self.z*vec.z)
        else:
            return Vec3(self.x*vec, self.y*vec, self.z*vec)
    def __truediv__(self, vec):
        if isinstance(vec, Vec3):
            return Vec3(self.x/vec.x, self.y/vec.y, self.z/vec.z)
        else:
            return Vec3(self.x/vec, self.y/vec, self.z/vec)
    def __iadd__(self, vec):
        return self.__add__(vec)
    def __isub__(self, vec):
        return self.__sub__(vec)
    def __imul__(self, vec):
        return self.__mul__(vec)
    def __idiv__(self, vec):
        return self.__truediv__(vec)
    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'
    def length_squared(self):
        return self.x**2+self.y**2+self.z**2
    def length(self):
        return self.length_squared()**0.5
    def near_zero(self):
        s = 1e-8
        return (abs(self.x) < s) and (abs(self.y) < s) and (abs(self.z) < s)

class Color(Vec3):
    def from_hex(self, hex):
        self.x, self.y, self.z=(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

class Point(Vec3):
    pass

def dot(u, v):
    return u.x * v.x + u.y * v.y + u.z * v.z

def cross(u, v):
    return Vec3(u.y * v.z - u.z * v.y, u.z * v.x - u.x * v.z, u.x * v.y - u.y * v.x)

def unit_vector(v):
    return v / v.length()

def random_vec(min=0, max=1):
    return Vec3(uniform(min, max), uniform(min, max), uniform(min, max))

def random_col(min=0, max=1):
    return Color(uniform(min, max), uniform(min, max), uniform(min, max))

def random_in_unit_sphere():
    while True:
        p = random_vec(-1,1)
        if p.length_squared() >= 1: continue
        return p

def random_unit_vector():
    return unit_vector(random_in_unit_sphere())

def random_in_hemisphere(normal):
    in_unit_sphere = random_in_unit_sphere()
    if dot(in_unit_sphere, normal) > 0.0:
        return in_unit_sphere
    else:
        return -in_unit_sphere

def random_in_unit_disk():
    while True:
        p = Vec3(uniform(-1,1), uniform(-1,1), 0)
        if p.length_squared() >= 1: continue
        return p

def reflect(v, n):
    return v - Vec3(2*dot(v,n))*n

def refract(uv, n, etai_over_etat):
    cos_theta = min(dot(-uv, n), 1.0)
    r_out_perp =  Vec3(etai_over_etat) * (uv + Vec3(cos_theta)*n)
    r_out_parallel = Vec3(-sqrt(abs(1.0 - r_out_perp.length_squared()))) * n
    return r_out_perp + r_out_parallel