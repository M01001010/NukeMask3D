'''
This code is embded in the gizmo found in the provided nuke script "Example.nk"
it get called when clicking on the button "Sample"
'''


import math

class Mask():

    def __init__(self, node):
        #self.n = nuke.thisNode()
        self.n = node
        if self.n["ctrl"].getValue() == 0:
            self.point1()
        if self.n["ctrl"].getValue() == 1:
            self.point2()
        

    def point1(self):
        p0 = self.n["focal_point"].getValue()
        with self.n:
            sampler = nuke.toNode("sample")
            r0 = nuke.sample(sampler, "red", p0[0], p0[1], 1, 1)
            g0 = nuke.sample(sampler, "green", p0[0], p0[1], 1, 1)
            b0 = nuke.sample(sampler, "blue", p0[0], p0[1], 1, 1)

        self.n["pos0"].setValue(r0, 0)
        self.n["pos0"].setValue(g0, 1)
        self.n["pos0"].setValue(b0, 2)

        self.n["pos1"].setValue(r0+self.n["range"].getValue(), 0)
        self.n["pos1"].setValue(g0, 1)
        self.n["pos1"].setValue(b0+self.n["range"].getValue(), 2)
        
        # depth
        camPos = []
        with n:
            info = nuke.toNode("cam_info")
            camPos = info["pos"].getValue()

        self.pos0 = (r0, g0, b0)
        far = math.sqrt((self.pos0[0] - camPos[0])**2  +  (self.pos0[1] - camPos[1])**2  +  (self.pos0[2] - camPos[2])**2)
        #self.n["near"].setValue(0)
        self.n["far"].setValue(far)


    def point2(self):
        self.sample()
        self.calculate()


    def sample(self):
        p0 = self.n["p0"].getValue()
        p1 = self.n["p1"].getValue()

        with self.n:
            sampler = nuke.toNode("sample")
            r1 = nuke.sample(sampler, "red", p1[0], p1[1], 1, 1)
            g1 = nuke.sample(sampler, "green", p1[0], p1[1], 1, 1)
            b1 = nuke.sample(sampler, "blue", p1[0], p1[1], 1, 1)
            r0 = nuke.sample(sampler, "red", p0[0], p0[1], 1, 1)
            g0 = nuke.sample(sampler, "green", p0[0], p0[1], 1, 1)
            b0 = nuke.sample(sampler, "blue", p0[0], p0[1], 1, 1)

        self.n["pos0"].setValue(r0, 0)
        self.n["pos0"].setValue(g0, 1)
        self.n["pos0"].setValue(b0, 2)
        self.n["pos1"].setValue(r1, 0)
        self.n["pos1"].setValue(g1, 1)
        self.n["pos1"].setValue(b1, 2)
        self.pos0 = [r0, g0, b0]
        self.pos1 = [r1, g1, b1]


    def calculate(self):
        vector = [self.pos1[0]-self.pos0[0] ,  self.pos1[1]-self.pos0[1], self.pos1[2]-self.pos0[2] ] 
        mag = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1] + vector[2]*vector[2])
        normalized = [vector[0] / mag, vector[1] / mag, vector[2] / mag]
        direction = math.atan2(vector[0] , vector[2])

        rotatedX = normalized[0] * math.cos(direction) - normalized[2] * math.sin(direction)
        rotatedY = normalized[1]
        rotatedZ = normalized[0] * math.sin(direction) + normalized[2] * math.cos(direction)

        angle = -math.atan2(rotatedY , rotatedZ)
        self.n["range"].setValue(mag)
        self.n["rotatey0"].setValue(math.degrees(direction))
        self.n["rotatex0"].setValue(math.degrees(angle))

        # depth
        camPos = []
        with n:
            info = nuke.toNode("cam_info")
            camPos = info["pos"].getValue()

        near = math.sqrt((self.pos0[0] - camPos[0])**2  +  (self.pos0[1] - camPos[1])**2  +  (self.pos0[2] - camPos[2])**2)
        far = math.sqrt( (self.pos1[0] - camPos[0])**2  +  (self.pos1[1] - camPos[1])**2  +  (self.pos1[2] - camPos[2])**2)
        self.n["near"].setValue(near)
        self.n["far"].setValue(far)


mask = Mask(nuke.thisNode())











