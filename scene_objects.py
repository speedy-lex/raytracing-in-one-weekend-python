from vec3 import dot

class HitData:
    def __init__(self, point=None, normal=None, t=None, ff=None, material=None) -> None:
        self.point=point
        self.normal=normal
        self.t=t
        self.mat=material
        self.frontface=ff
    def set_face_normal(self, r, out):
        if dot(r.dir, out) > 0.0:
            self.normal = -out
            self.front_face = False
        else:
            self.normal = out
            self.front_face = True

class Hittable:
    def __init__(self) -> None:
        pass
    def hit(self, r, t_min, t_max):
        return False

class Sphere(Hittable):
    def __init__(self, center, radius, mat) -> None:
        self.center=center
        self.radius=radius
        self.mat=mat
    def hit(self, r, t_min, t_max, rec):
        oc = r.orig - self.center
        a = r.dir.length_squared()
        half_b = dot(oc, r.dir)
        c = oc.length_squared() - self.radius*self.radius

        discriminant = half_b*half_b - a*c
        if discriminant < 0: return (False,)
        sqrtd = discriminant**0.5

        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return (False,)

        rec.t = root
        rec.point = r.lerp(rec.t)
        rec.normal = (rec.point - self.center) / self.radius
        outward_normal = (rec.point - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.mat=self.mat

        return (True, rec)

class HittableList(Hittable):
    def __init__(self, *args):
        self.objects=list(args)
    def clear(self):
        self.objects=[]
    def add(self, obj):
        self.objects.append(obj)
    def hit(self, r, t_min, t_max, rec):
        hit_anything = False
        closest_so_far = t_max
        temp_rec=HitData()
        for obj in self.objects:
            h=obj.hit(r, t_min, closest_so_far, temp_rec)
            if h[0]:
                temp_rec=h[1]
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec
        return (hit_anything, rec)