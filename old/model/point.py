class Point:
    def __init__(self, x = None, y = None, z = None):
        self.x = x
        self.y = y
        self.z = z

    def get(self):
        return (self.x, self.y, self.z)
    