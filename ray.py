class Ray:
    def __init__(self, origin, direction) -> None:
        self.orig=origin
        self.dir=direction
    def lerp(self, t):
        return self.orig+self.dir*t