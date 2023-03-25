from vec3 import Vec3, Color, Point, unit_vector, dot, cross, random_in_unit_sphere, random_unit_vector, random_col
from img_write import write, new, to_np
from math import inf
from random import random, uniform
from scene_objects import HitData, HittableList, Sphere
from camera import Camera
from materials import Metal, Lambertian, Dielectric

def ray_color(r, world, depth):
    if depth <= 0:
        return Color(0)
    rec=HitData()
    h=world.hit(r, 0.001, inf, rec)
    if h[0]:
        rec=h[1]
        k=rec.mat.scatter(r, rec)
        if (k[0]):
            return k[2] * ray_color(k[1], world, depth-1)
        return Color(0,0,0)
    unit_direction = unit_vector(r.dir)
    t = 0.5*(unit_direction.y + 1.0)
    return Color(1.0-t)*Color(1.0, 1.0, 1.0) + Color(t)*Color(0.5, 0.7, 1.0)

def random_scene():
    world=HittableList()

    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point(0,-1000,0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random()
            center=Point(a + 0.9*random(), 0.2, b + 0.9*random())

            if ((center - Point(4, 0.2, 0)).length() > 0.9):
                if (choose_mat < 0.8):
                    albedo = random_col()*random_col()
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif (choose_mat < 0.95):
                    albedo = random_col(0.5, 1)
                    fuzz = uniform(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material1 = Dielectric(1.5)
    world.add(Sphere(Point(0, 1, 0), 1.0, material1))

    material2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point(-4, 1, 0), 1.0, material2))

    material3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Point(4, 1, 0), 1.0, material3))

    return world

aspect_ratio = 3.0 / 2.0
image_width = 150#1200
image_height = int(image_width / aspect_ratio)
samples_per_pixel = 1#500
max_depth = 5#50

world = random_scene()

lookfrom=Point(13,2,3)
lookat=Point(0,0,0)
vup=Vec3(0,1,0)
dist_to_focus = 10.0
aperture = 0.1

cam=Camera(lookfrom, lookat, vup, aperture, dist_to_focus, aspect_ratio, 20)

img=new((image_width, image_height))

for j in range(image_height):
    print('scanlines left:', image_height-1-j)
    for i in range(image_width):
        col=Color(0)
        for s in range(samples_per_pixel):
            u = (i+random())/(image_width-1)
            v = (j+random())/(image_height-1)
            r=cam.get_ray(u, v)
            col += ray_color(r, world, max_depth)
        img[i][j]=to_np(col)

write((img/samples_per_pixel)**0.5, 'img.png')