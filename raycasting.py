import pygame
import sys
from math import sin,cos,sqrt,radians,degrees



dis = (1920,1080) # define window size
root = pygame.display.set_mode(dis,pygame.FULLSCREEN)
cx = dis[0]//2 
cy = dis[1]//2 

clock = pygame.time.Clock()
FPS = 0

maxLen = 3000 # max length of rays

pygame.mouse.set_visible(False)

class circle()
    
    # circle hitbox, contains a simple distance estimator and draw methods

    def __init__(self,x,y,r):
        self.pos = [x,y]
        self.r = r

    def draw(self,root):
        pygame.draw.circle(root,(255,255,255),self.pos,self.r,1)

    def distEst(self,point):
        dist = sqrt((self.pos[0]-point[0])**2+(self.pos[1]-point[1])**2)
        return abs(dist-self.r)

class rectangle():
    
    # rectangle hitbox, contains a distance estimator and draw methods
    
    def __init__(self,x,y,w,h):
        self.pos = [x,y]
        self.wh = [w,h]

    def draw(self,root):
        pygame.draw.rect(root,(255,255,255),(self.pos,self.wh),1)

    def distEst(self,point):
        pt = [0,0]

        if point[0] < self.pos[0]:
            pt[0] = self.pos[0]
        elif point[0] > self.pos[0]+self.wh[0]:
            pt[0] = self.pos[0]+self.wh[0]
        else:
            pt[0] = point[0]

        if point[1] < self.pos[1]:
            pt[1] = self.pos[1]
        elif point[1] > self.pos[1]+self.wh[1]:
            pt[1] = self.pos[1]+self.wh[1]
        else:
            pt[1] = point[1]

        return sqrt((pt[0]-point[0])**2+(pt[1]-point[1])**2)
        

class ray():
    
    # The ray class, the ray calculation happens at object creation
    
    def __init__(self,x,y,angle,colliders):
        self.start = [x,y]
        self.target = [x,y]

        vx,vy = sin(angle),cos(angle) # calculate a movement vector of 1px length in ray direction

        length = 0
        step = maxLen

        self.circles = []
        
        while length < maxLen and step > 1: # move the ray forward aslong as the length is less than maximum length and the last step length was greater than 1

            steps = []
            for collider in colliders:
                steps.append(collider.distEst(self.target)) # this gets the value of all distance estimators from the ray
            step = min(min(steps),maxLen-length) # it takes the minimum of the distance estimators, and then compares it to the maximum length to make sure the ray doesn't go too far

            self.circles.append([self.target.copy(),step])

            self.target[0] += vx*step # move the end of the ray by the distance calculated
            self.target[1] += vy*step

            length += step # sum the length

    def draw(self,root):
        pygame.draw.line(root,(255,0,0),self.start,self.target)

        #for circle in self.circles:
         #   pygame.draw.circle(root,(255,0,255),circle[0],circle[1],1)
            

scene = [circle(dis[0]//2,dis[1]//2,100),rectangle(0,0,1920,50)] # defines the objects in the scene


def main(args):

    frame = 0

    while True:
        frame += 0.002
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        

        mx,my = pygame.mouse.get_pos()
        rays = []

        for i in range(360):
            rays.append(ray(mx,my,radians(i/8)+frame,scene)) # generate the rays around the mouse cursor

        root.fill((0,0,0))

        pygame.draw.circle(root,(255,0,0),[mx,my],5)

        for obj in scene:
            obj.draw(root) # draw the scene

        for r in rays:
            r.draw(root) # draw the rays

        pygame.display.update() # update the window
        clock.tick(FPS)

if __name__ == '__main__':
    try:
        main(sys.argv)
    except Exception as e:
        pygame.quit()
        raise e

    pygame.quit()
    sys.exit()
