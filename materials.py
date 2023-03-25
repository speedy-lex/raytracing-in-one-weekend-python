from vec3 import random_unit_vector, reflect, refract, unit_vector, dot, Vec3, random_in_unit_sphere, Color
from ray import Ray
from random import random

class Material:
    def __init__(self, a) -> None:
        self.albedo=a

class Lambertian(Material):
    def scatter(self, r_in, rec):
        scatter_direction = rec.normal + random_unit_vector()
        if scatter_direction.near_zero():
            scatter_direction = rec.normal
        scattered = Ray(rec.point, scatter_direction)
        return (True, scattered, self.albedo)

class Metal(Material):
    def __init__(self, a, roughness) -> None:
        super().__init__(a)
        self.fuzz=roughness
    def scatter(self, r_in, rec):
        reflected = reflect(unit_vector(r_in.dir), rec.normal)
        scattered = Ray(rec.point, reflected+Vec3(self.fuzz)*random_in_unit_sphere())
        return (dot(scattered.dir, rec.normal) > 0, scattered, self.albedo)

class Dielectric(Material):
    def __init__(self, ior) -> None:
        self.ior=ior
    def scatter(self, r_in, rec):
        if rec.frontface:
            refraction_ratio = (self.ior)
        else:
            refraction_ratio=1.0/self.ior

        unit_direction = unit_vector(r_in.dir)
        cos_theta = min(dot(-unit_direction, rec.normal), 1.0)
        sin_theta = (1.0 - cos_theta*cos_theta)**0.5

        cannot_refract = refraction_ratio * sin_theta > 1.0

        if cannot_refract or self.reflectance(cos_theta, refraction_ratio)>random():
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, refraction_ratio)

        scattered = Ray(rec.point, direction)
        return (True, scattered, Color(1))
    def reflectance(self, cosine, ref_idx):
        r0 = (1-ref_idx) / (1+ref_idx)
        r0 = r0**2
        return r0 + (1-r0)*pow((1 - cosine),5)