from vec3 import Point, Vec3, cross, unit_vector, random_in_unit_disk
from ray import Ray
from math import radians, tan

class Camera:
    def __init__(self, lookfrom, lookat, vup, aperture, focus_dist, aspect_ratio=16/9, vfov=90):
        self.theta=radians(vfov)
        self.h=tan(self.theta/2)
        self.aspect_ratio = aspect_ratio
        self.viewport_height = 2.0*self.h
        self.viewport_width = self.aspect_ratio * self.viewport_height

        self.w = unit_vector(lookfrom - lookat)
        self.u = unit_vector(cross(vup, self.w))
        self.v = cross(self.w, self.u)

        self.origin = lookfrom
        self.horizontal = Vec3(focus_dist*self.viewport_width) * self.u
        self.vertical = Vec3(focus_dist*self.viewport_height) * self.v
        self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical/2 - Vec3(focus_dist)*self.w

        self.lens_radius=aperture / 2
    
    def get_ray(self, s, t):
        rd = Vec3(self.lens_radius) * random_in_unit_disk()
        offset = self.u * rd.x + self.v * rd.y

        return Ray(
            self.origin + offset,
            self.lower_left_corner + Vec3(s)*self.horizontal + Vec3(t)*self.vertical - self.origin - offset)