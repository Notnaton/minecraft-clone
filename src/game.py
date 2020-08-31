from pyglet.gl import *
from pyglet.window import key
from pyglet.window import FPSDisplay
from pyglet.text import Label
from opensimplex import OpenSimplex
import math
#import os
#import sys

class TextureHandler():
    def get_tex(self, file):
        texture = pyglet.image.load(file).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(texture)

    def __init__(self):
        os_path = "c:/Users/anton/Documents/dev/minecraft-clone/src/"
        self.rock = (self.get_tex(os_path + '../res/rock.png'),self.get_tex(os_path + '../res/rock.png'),self.get_tex(os_path + '../res/rock.png'))
        self.dirt = (self.get_tex(os_path + '../res/grass_bottom.png'),self.get_tex(os_path + '../res/grass_bottom.png'),self.get_tex(os_path + '../res/grass_bottom.png'))
        self.grass = (self.get_tex(os_path + '../res/grass_side.png'),self.get_tex(os_path + '../res/grass_bottom.png'),self.get_tex(os_path + '../res/grass_top.png'))


class Renderer():
    def chunkToRenderer(self, chunkPos):

        self.test = self.ch.generateChunk(chunkPos)

        x,y,z =0,0,0
        for a in self.test:
            for b in a:
                for c in b:
                    if(c == 0):
                        pass
                    else:
                        if(c == 1):
                            tex=self.tex.rock
                        elif (c == 2):
                            tex = self.tex.dirt
                        elif(c == 3):
                            tex=self.tex.grass
                        self.renderBlock((chunkPos[0]*16+x,chunkPos[1]*16+y,chunkPos[2]*16+z), tex)
                    z+=1
                z=0
                y+=1
            y=0
            x+=1
        x=0


    def renderBlock(self, pos, texture):
        x,z,y = pos[0],pos[1],pos[2]
        self.batch.add(4, GL_QUADS, texture[0], ('v3f', (x+1,z+0,y+0, x+0,z+0,y+0, x+0,z+1,y+0, x+1,z+1,y+0, )), self.tex_coord) #Back
        self.batch.add(4, GL_QUADS, texture[0], ('v3f', (x+0,z+0,y+1, x+1,z+0,y+1, x+1,z+1,y+1, x+0,z+1,y+1, )), self.tex_coord) #Front
        self.batch.add(4, GL_QUADS, texture[0], ('v3f', (x+0,z+0,y+0, x+0,z+0,y+1, x+0,z+1,y+1, x+0,z+1,y+0, )), self.tex_coord) #Left
        self.batch.add(4, GL_QUADS, texture[0], ('v3f', (x+1,z+0,y+1, x+1,z+0,y+0, x+1,z+1,y+0, x+1,z+1,y+1, )), self.tex_coord) #Right
        self.batch.add(4, GL_QUADS, texture[1], ('v3f', (x+0,z+0,y+0, x+1,z+0,y+0, x+1,z+0,y+1, x+0,z+0,y+1, )), self.tex_coord) #Bottom
        self.batch.add(4, GL_QUADS, texture[2], ('v3f', (x+0,z+1,y+1, x+1,z+1,y+1, x+1,z+1,y+0, x+0,z+1,y+0, )), self.tex_coord) #Top


    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.tex = TextureHandler()
        self.ch = ChunkHandler()
        self.tex_coord = ('t2f', (0,0, 1,0, 1,1, 0,1, ))

        #self.chunkToRenderer((0,0,0))
        #self.renderBlock()

    def draw(self):
        self.batch.draw()



class ChunkHandler():
    def __init__(self):
        self.gen = OpenSimplex()
        #self.loadChunk() #TEST

    def loadChunk(self, chunkPos=(0,0,0)):
        pass
        #self.genChunk = generateChunk(chunkPos)
        #print(self.genChunk)
        #TODO Check if exist: load changes from memory generate, else generate.

    def generateElevation(self, chunkPos):
        self.posX, self.posY = chunkPos[0]*16, chunkPos[2]*16
        self.elevation=[[0 for _ in range(16)] for _ in range(16)]
        for y in range(self.posY, self.posY+16):
            for x in range(self.posX, self.posX+16):
                nx= x/16 -0.5
                ny= y/16 -0.5
                e= (50.0* (self.gen.noise2d(0.1*nx, 0.1*ny)+1)/2
                +    1.0* (self.gen.noise2d(2*nx, 2*ny)+1)/2
                +    0.5* (self.gen.noise2d(4*nx, 4*ny)+1)/2)
                #print(int(e*100))
                self.elevation[x%16][y%16] = int(math.pow(e, 0.5)*100)
        return self.elevation

    def generateChunk(self, chunkPos):
        self.surface = self.generateElevation(chunkPos)
        self.chunkData = [[[0 for _ in range(16)]for _ in range(16)]for _ in range(16)]
        for y in range(16):
            for x in range(16):
                for z in range(16):
                    if (self.surface[x][y] -2 > chunkPos[1]*16+z):
                        self.chunkData[x][z][y] = 1
                    elif (self.surface[x][y] -2 <= chunkPos[1]*16+z and self.surface[x][y] > chunkPos[1]*16+z):
                        self.chunkData[x][z][y] = 2
                    elif (self.surface[x][y] == chunkPos[1]*16+z):
                        self.chunkData[x][z][y] = 3
        return self.chunkData




class Player():
    def __init__(self, pos=(0,0,0), rot=(0,0)):
        self.pos= list(pos)
        self.rot= list(rot)
        self.currentChunkPos= [int((i-i%16)/16)  for i in pos]
        self.updateChunk = True



    def mouse_motion(self, dx, dy):
        dx/=8; dy/=8; self.rot[0]+=dy; self.rot[1]-=dx
        if(self.rot[0]>90): self.rot[0]=90
        elif(self.rot[0]<-90): self.rot[0]=-90



    def update(self, dt ,keys):

        s = dt*10
        rotY = self.rot[1]/180*math.pi
        dx, dz = s*math.sin(rotY), s*math.cos(rotY)

        if(keys[key.W]): self.pos[0] -= dx; self.pos[2] -= dz
        if(keys[key.S]): self.pos[0] += dx; self.pos[2] += dz
        if(keys[key.A]): self.pos[0] -= dz; self.pos[2] += dx
        if(keys[key.D]): self.pos[0] += dz; self.pos[2] -= dx
        if(keys[key.SPACE]): self.pos[1] += s
        if(keys[key.LSHIFT]): self.pos[1] -= s

        #TODO Mouse buttons
        #chunkPos
        newChunkPos= [int((i-i%16)/16)  for i in self.pos]
        if(newChunkPos == self.currentChunkPos):
            self.updateChunk = False
        else:
            self.currentChunkPos = newChunkPos
            self.updateChunk = True




class Window(pyglet.window.Window):
    def push(self, pos, rot): glPushMatrix(); glRotatef(-rot[0], 1, 0, 0); glRotatef(-rot[1], 0, 1, 0); glTranslatef(-pos[0], -pos[1], -pos[2])
    def Projection(self): glMatrixMode(GL_PROJECTION); glLoadIdentity()
    def Model(self): glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    def set2d(self): self.Projection(); gluOrtho2D(0, self.width, 0, self.height); self.Model() #0, self.width, 0, self.height, 0
    def set3d(self): self.Projection(); gluPerspective(90, self.width/self.height, 0.05, 1000); self.Model()
    def setLock(self, state): self.lock = state; self.set_exclusive_mouse(state)
    lock = False; mouse_lock = property(lambda self:self.lock, setLock)




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300, 200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        self.fps = FPSDisplay(self).label = Label(color=(0,0,0,255), y=int(self.height-50))
        self.playerInfo = Label(color=(0,0,0,255), y=int(self.height-75))
        self.mouse_lock = not self.mouse_lock


        self.renderer = Renderer()
        #TODO draw chunk
        self.chunk = ChunkHandler()
        #self.chunk.generateChunk((0,0,0))

        self.player = Player((1, 540, 2), (0, 0))
        self.renderer.chunkToRenderer(self.player.currentChunkPos)

    def on_mouse_motion(self, x, y, dx, dy):
        if(self.mouse_lock): self.player.mouse_motion(dx, dy)

    def on_key_press(self, KEY, MOD):
        if(KEY== key.ESCAPE): self.close()
        elif(KEY== key.CAPSLOCK): self.mouse_lock = not self.mouse_lock

    def update(self, dt):
        self.player.update(dt, self.keys)
        if self.player.updateChunk:
            self.renderer.chunkToRenderer(self.player.currentChunkPos)


    def on_draw(self):

        self.clear()
        self.set3d()
        self.push(self.player.pos, self.player.rot)
        self.renderer.draw()

        x= list(map(int, self.player.pos))+ [' Chunk: '] + list(map(int, self.player.currentChunkPos))
        self.playerInfo.text=(str(x))

        self.set2d()
        self.fps.draw()
        self.playerInfo.draw()
        glPopMatrix()


def main():
    _window = Window(width=1600, height=1200, caption="Test Game", resizable=True)
    glClearColor(0.5, 0.7, 1, 0.5)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    pyglet.app.run()

if(__name__ == "__main__"):
    main()
