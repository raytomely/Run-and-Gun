from math import degrees,atan2,sqrt
import pygame
from pygame.locals import*

SCREEN_WIDTH=640
SCREEN_HEIGHT=480
SCALE=4
PATH="run_n_gun_data/"

def collide(point,rect):
    collided=0
    if point[0]>=rect[0] and point[0]<rect[0]+rect[2] \
    and point[1]>=rect[1] and point[1]<rect[1]+rect[3]:
        collided=1
    return collided

def rect_collision(rect1,rect2):
    collision=0
    point1=(rect1[0],rect1[1])
    point2=(rect1[0]+rect1[2],rect1[1])
    point3=(rect1[0],rect1[1]+rect1[3])
    point4=(rect1[0]+rect1[2],rect1[1]+rect1[3])
    if collide(point1,rect2) or collide(point2,rect2) \
    or collide(point3,rect2) or collide(point4,rect2):
       collision=1
    return collision

def circle_collision(circle1,circle2):
    collision=0
    c1=circle1.center
    c2=circle2.center
    lenght=math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)
    if circle1.radius+circle2.radius>lenght:
       collision=1
    return collision

def circle_collision2(circle1,circle2):
    #optimized circle collision detection
    #that doesn't rely on the too costly square root function        
    collision=0
    dx=circle1.center[0]-circle2.center[0]
    dy=circle1.center[1]-circle2.center[1]
    if (circle1.radius+circle2.radius)**2>dx**2+dy**2:
       collision=1
    return collision

def circle_collision3(circle1,circle2):
    #optimized circle collision detection
    #that doesn't rely on the too costly square root function    
    collision=0
    xdist=circle1.center[0]-circle2.center[0]
    ydist=circle1.center[1]-circle2.center[1]
    radius_sum=circle1.radius+circle2.radius
    if xdist<0:
       xdist*=-1
    if ydist<0:
       ydist*=-1       
    if radius_sum>xdist and radius_sum>ydist:
       collision=1
    return collision

def normalize(vector):
    lenght=sqrt(vector[0]**2+vector[1]**2)
    vector[0]=vector[0]/lenght
    vector[1]=vector[1]/lenght
    
def normalize2(vec1,vec2):
    dx=abs(vec1[0]-vec2[0])
    dy=abs(vec1[1]-vec2[1])
    lenght=dx+dy-min(dx,dy)/2
    vec=[vec2[0]-vec1[0],vec2[1]-vec1[1]]
    vec[0]=vec[0]/lenght
    vec[1]=vec[1]/lenght
    return vec

def normalize3(vec1,vec2):
    dx=abs(vec1[0]-vec2[0])
    dy=abs(vec1[1]-vec2[1])
    lenght=dx+dy
    vec=[vec2[0]-vec1[0],vec2[1]-vec1[1]]
    vec[0]=vec[0]/lenght
    vec[1]=vec[1]/lenght
    return vec

def make_image(path,scale=1):
    image=pygame.image.load(path)
    alpha_color=image.get_at((0,0))
    image.set_colorkey(alpha_color)
    if scale>1:
       image=pygame.transform.scale(image,(image.get_width()*scale,image.get_height()*scale))
    return image
   
def make_glow_image(path,scale=1):
    glow=pygame.image.load(path)
    alpha_color=glow.get_at((0,0))    
    red=(255,0,0,255)
    for i in range(glow.get_height()):
        for j in range(glow.get_width()):
            if glow.get_at((j,i))!=alpha_color:
               glow.set_at((j,i),red)
    glow.set_colorkey(alpha_color)
    glow.set_alpha(150)
    if scale>1:
       glow=pygame.transform.scale(glow,(glow.get_width()*scale,glow.get_height()*scale))
    return glow

def animate(sprite):
    sprite.anim_time+=1
    if sprite.anim_time>=sprite.max_anim_time:
       sprite.anim_time=0
       if sprite.anim_frame<sprite.hor_cells:
          sprite.anim_frame+=1
          sprite.current_frame[0]+=sprite.cell_width
       else:
          sprite.anim_frame=1
          sprite.current_frame[0]=0


class Sprite:
    def __init__(self,hor_cells,ver_cells,image=None,shadow=None,max_anim_time=3):
        if image:
           self.image=make_image(image,SCALE).convert()
        if shadow:
           self.shadow=make_image(shadow,SCALE).convert()
        self.width=self.image.get_width()
        self.height=self.image.get_height()        
        self.hor_cells=hor_cells
        self.ver_cells=ver_cells
        self.cell_width=int(self.width/self.hor_cells)
        self.cell_height=int(self.height/self.ver_cells)
        self.center=[int(self.cell_width/2),int(self.cell_height/2)]
        self.anim_frame=1
        self.max_anim_time=max_anim_time
        self.anim_time=0
        self.current_frame=[0,0,self.cell_width,self.cell_height]

    def animate(self):
        self.anim_time+=1
        if self.anim_time>=self.max_anim_time:
           self.anim_time=0
           if self.anim_frame<self.hor_cells:
              self.anim_frame+=1
              self.current_frame[0]+=self.cell_width
           else:
              self.anim_frame=1
              self.current_frame[0]=0


class Player():
    def __init__(self,pos):
        Sprite.__init__(self,5,8,PATH+"rambito.png",PATH+"rambito_shadow.png")
        self.shadow.set_alpha(100)
        self.pos=pos
        self.box=[self.pos[0]+48,self.pos[1]+70,30,30]
        self.direction="up"
        self.move_speed=10
        self.xvel=0
        self.yvel=0        
        self.up_frame_pos_y=0
        self.down_frame_pos_y=self.cell_height*4
        self.right_frame_pos_y=self.cell_height*2
        self.left_frame_pos_y=self.cell_height*6

    def update(self,direction):
        if direction=="up":
           self.yvel=-self.move_speed
           self.pos[1]+=self.yvel
           self.box[1]=self.pos[1]+70
           if self.box[1]<0:
              self.pos[1]=-70
           self.current_frame[1]=self.up_frame_pos_y
        elif direction=="down":
           self.yvel=self.move_speed
           self.pos[1]+=self.yvel
           self.box[1]=self.pos[1]+70
           if self.box[1]+self.box[3]>SCREEN_HEIGHT:
              self.pos[1]=SCREEN_HEIGHT-self.box[3]-70
           self.current_frame[1]=self.down_frame_pos_y
        if direction=="right":
           self.xvel=self.move_speed
           self.pos[0]+=self.xvel
           self.box[0]=self.pos[0]+48
           if self.box[0]+self.box[2]>SCREEN_WIDTH:
              self.pos[0]=SCREEN_WIDTH-self.box[2]-48
           self.current_frame[1]=self.right_frame_pos_y
        elif direction=="left":
           self.xvel=-self.move_speed
           self.pos[0]+=self.xvel
           self.box[0]=self.pos[0]+48
           if self.box[0]<0:
              self.pos[0]=-48
           self.current_frame[1]=self.left_frame_pos_y
        animate(self)

    def draw(self,surface):
        surface.blit(self.shadow,self.pos,self.current_frame)            
        surface.blit(self.image,self.pos,self.current_frame)
        
              
class Gun:
    def __init__(self):
        self.bullet_live=Sprite(2,1,PATH+"bullet.png",PATH+"bullet_shadow.png")
        self.bullet_live.shadow.set_alpha(100)
        self.bullet_death=Sprite(3,1,PATH+"bullet_death.png")
        self.bullet=self.bullet_live
        self.center_difference=[self.bullet_live.center[0]-self.bullet_death.center[0],
        self.bullet_live.center[1]-self.bullet_death.center[1]]
        self.up_fire_pos=[83-self.bullet.center[0],37-self.bullet.center[1]]
        self.right_fire_pos=[113-self.bullet.center[0],70-self.bullet.center[1]]
        self.down_fire_pos=[52-self.bullet.center[0],95-self.bullet.center[1]]
        self.left_fire_pos=[18-self.bullet.center[0],70-self.bullet.center[1]]
        self.fire_pos=[0,0]
        self.direction="up"
        self.fire=0
        self.active=0
        self.death=0
        self.move_speed=15
        self.move_x=0
        self.move_y=0
        self.moved_dist=0
        self.max_move_dist=10

    def update(self,player_pos):
        if self.fire:
           if not self.active:
              if self.direction=="up":
                 self.fire_pos=[player_pos[0]+self.up_fire_pos[0],player_pos[1]+self.up_fire_pos[1]]
                 self.move_x=0
                 self.move_y=-self.move_speed
              if self.direction=="down":
                 self.fire_pos=[player_pos[0]+self.down_fire_pos[0],player_pos[1]+self.down_fire_pos[1]]
                 self.move_x=0
                 self.move_y=self.move_speed
              if self.direction=="left":
                 self.fire_pos=[player_pos[0]+self.left_fire_pos[0],player_pos[1]+self.left_fire_pos[1]]
                 self.move_x=-self.move_speed
                 self.move_y=0
              if self.direction=="right":
                 self.fire_pos=[player_pos[0]+self.right_fire_pos[0],player_pos[1]+self.right_fire_pos[1]]
                 self.move_x=self.move_speed
                 self.move_y=0
              self.active=1
                 
           if not self.death:
              self.fire_pos[0]+=self.move_x
              self.fire_pos[1]+=self.move_y
              self.moved_dist+=1
              if self.moved_dist>=self.max_move_dist:
                 self.moved_dist=0
                 self.death=1
                 self.bullet=self.bullet_death
                 self.fire_pos[0]+=self.center_difference[0]
                 self.fire_pos[1]+=self.center_difference[1]
              self.bullet.animate()
              
           elif self.death:
                if self.bullet.anim_frame<self.bullet.hor_cells:
                   self.bullet.animate()
                else:
                   self.fire=0
                   self.death=0
                   self.active=0
                   self.bullet.anim_frame=1
                   self.bullet.current_frame[0]=0
                   self.bullet=self.bullet_live
                   self.fire_pos[0]-=self.center_difference[0]
                   self.fire_pos[1]-=self.center_difference[1]
    def draw(self,surface):
        if self.fire:
           surface.blit(self.bullet.image,self.fire_pos,self.bullet.current_frame)
           if not self.death:
              surface.blit(self.bullet.shadow,self.fire_pos,self.bullet.current_frame)
              

class Enemy:
    group=[]
    image=make_image(PATH+"zombito.png",SCALE)
    shadow=make_image(PATH+"rambito_shadow.png",SCALE)
    shadow.set_alpha(100)
    glow=make_glow_image(PATH+"zombito.png",SCALE)
    
    def __init__(self,pos):
        if not self in Enemy.group:
           Enemy.group.append(self)
        Sprite.__init__(self,5,8,None,None,10)
        self.type="enemy"
        self.image=Enemy.image.convert()
        self.shadow=Enemy.shadow.convert()
        self.pos=pos
        self.shadow_pos=self.pos
        self.glow=Enemy.glow.convert()
        self.glowing=0
        self.up_frame_pos_y=0
        self.up_right_frame_pos_y=self.cell_height
        self.right_frame_pos_y=self.cell_height*2
        self.down_right_frame_pos_y=self.cell_height*3
        self.down_frame_pos_y=self.cell_height*4
        self.down_left_frame_pos_y=self.cell_height*5
        self.left_frame_pos_y=self.cell_height*6
        self.up_left_frame_pos_y=self.cell_height*7
        self.current_frame=[0,self.cell_height*4,self.cell_width,self.cell_height]
        self.direction="down"
        self.move_speed=1
        self.velocity=[0,0]
        self.moved_dist=0
        self.max_dist=200
        self.box=[38,20,50,80]
        self.box2=[48,70,30,30]
        self.make_perimetre()
        self.vitality=3
        self.death=0
        self.dying=0
        self.dying_time=0
        self.temp=[]
        self.blit_ok=1

    def update(self,player_pos,gun,active_actor,active_solid_tile,level_tile_pos):
        if not self.dying:
           self.blit_ok=1 
           self.seek_player(player_pos,active_actor,active_solid_tile,level_tile_pos)
           animate(self)
           self.shadow_pos=self.pos
           if gun.fire:
              enemy_pos=[self.pos[0]+self.box[0],self.pos[1]+self.box[1]]
              fire_pos=[gun.fire_pos[0]+gun.bullet.center[0],gun.fire_pos[1]+gun.bullet.center[1]]
              if fire_pos[0]>enemy_pos[0]and fire_pos[0]<enemy_pos[0]+self.box[2] \
              and fire_pos[1]>enemy_pos[1]and fire_pos[1]<enemy_pos[1]+self.box[3]:
                 if not gun.death:
                    self.glowing=1
                    self.vitality-=1
                    gun.death=1
                    gun.moved_dist=0
                    gun.bullet=gun.bullet_death
                    gun.fire_pos[0]+=gun.center_difference[0]
                    gun.fire_pos[1]+=gun.center_difference[1]
                 if self.vitality<=0:
                    self.dying=1
                    self.anim_frame=1
                    self.max_anim_time=0
                    self.temp=[self.current_frame[0],self.current_frame[1]]
                    self.shadow_pos=[self.pos[0],self.pos[1]]
                    self.current_frame[1]=0
        elif self.dying:
          self.death_sequence(player_pos)
        
    def death_sequence(self,player_pos):
        if self.dying_time<20:
           self.anim_time+=1
           if self.anim_time>=self.max_anim_time:
              self.anim_time=0
              if self.anim_frame<self.ver_cells:
                 self.anim_frame+=1
                 self.current_frame[1]+=self.cell_height
              else:
                 self.anim_frame=1
                 self.current_frame[1]=self.up_frame_pos_y
           if self.dying_time>=19:
              self.current_frame[0]=self.temp[0]
              self.current_frame[1]=self.temp[1]
           if self.dying_time<10:
              self.pos[1]-=5
           else:
              self.pos[1]+=5
           self.dying_time+=1
           
        else:       
          if self.blit_ok:
             self.blit_ok=0
          else:
             self.blit_ok=1
          self.dying_time+=1
          if self.dying_time>=50:
             self.death=1
             self.blit_ok=0
             self.kill()
             
    def draw(self,surface,player):
        if self.blit_ok:
           if self.pos[1]<=player.pos[1]:
              surface.blit(self.shadow,self.shadow_pos,self.current_frame)
              surface.blit(self.image,self.pos,self.current_frame)
              player.draw(surface)
           elif self.pos[1]>player.pos[1]:
              surface.blit(self.shadow,self.shadow_pos,self.current_frame)
              surface.blit(self.image,self.pos,self.current_frame)
           if self.glowing:
              surface.blit(self.glow,self.pos,self.current_frame)
              self.glowing=0
    
    def kill(self):
        Enemy.group.remove(self)
              
    def seek_player(self,player_pos,active_actor,active_solid_tile,level_tile_pos):
        dx=player_pos[0]-self.pos[0]
        dy=player_pos[1]-self.pos[1]
        if abs(dx)>1 or abs(dy)>1:
           vec=normalize3(self.pos,player_pos)
           self.velocity[0]=vec[0]
           self.velocity[1]=vec[1]
           self.collision_walk2(self.velocity[0],0,active_actor,active_solid_tile,level_tile_pos)
           self.collision_walk2(0,self.velocity[1],active_actor,active_solid_tile,level_tile_pos)
           angle=degrees(atan2(-dy,dx))
           if angle<0:
              angle=360+angle
           if angle>=self.perimetre[0] and angle<=360 \
           or angle<=self.perimetre[1] and angle>=0:
              self.current_frame[1]=self.right_frame_pos_y
           elif angle>self.perimetre[1] and angle<self.perimetre[2]:
              self.current_frame[1]=self.up_right_frame_pos_y
           elif angle>=self.perimetre[2] and angle<self.perimetre[3]:
              self.current_frame[1]=self.up_frame_pos_y
           elif angle>=self.perimetre[3] and angle<self.perimetre[4]:
              self.current_frame[1]=self.up_left_frame_pos_y
           elif angle>=self.perimetre[4] and angle<self.perimetre[5]:
              self.current_frame[1]=self.left_frame_pos_y
           elif angle>=self.perimetre[5] and angle<self.perimetre[6]:
              self.current_frame[1]=self.down_left_frame_pos_y
           elif angle>=self.perimetre[6] and angle<self.perimetre[7]:
              self.current_frame[1]=self.down_frame_pos_y
           elif angle>=self.perimetre[7] and angle<self.perimetre[8]:
              self.current_frame[1]=self.down_right_frame_pos_y

    def seek_player2(self,player_pos):
        if player_pos[0]>self.pos[0]:
           self.current_frame[1]=self.right_frame_pos_y
           self.pos[0]+=self.move_speed
        elif player_pos[0]<self.pos[0]:
           self.current_frame[1]=self.left_frame_pos_y
           self.pos[0]-=self.move_speed
        if player_pos[1]>self.pos[1]:
           self.current_frame[1]=self.down_frame_pos_y
           self.pos[1]+=self.move_speed
        elif player_pos[1]<self.pos[1]:
           self.current_frame[1]=self.up_frame_pos_y
           self.pos[1]-=self.move_speed
               
    def collision_walk2(self,xvel,yvel,active_actor,active_solid_tile,level_tile):
        collided=0
        self_rect=[self.pos[0]+self.box2[0]+xvel,self.pos[1]+self.box2[1]+yvel,self.box2[2],self.box2[3]]
        tile_width=64
        tile_height=64
        for actor in active_actor:
            if actor.type=="enemy" and actor!=self and not actor.dying:
               enemy_rect=[actor.pos[0]+actor.box2[0],actor.pos[1]+actor.box2[1],actor.box2[2],actor.box2[3]]
               if rect_collision(self_rect,enemy_rect):      
                  collided=1
                  break
        for i in active_solid_tile:
            tile_rect=[level_tile[i].pos[0],level_tile[i].pos[1],tile_width,tile_height]
            if rect_collision(self_rect,tile_rect):
               collided=1
               break
        if not collided:
           self.pos[0]+=xvel
           self.pos[1]+=yvel

    def left_right_walk(self):
        if not self.direction=="left" and not self.direction=="right":
           self.direction="left"
           self.current_frame[1]=self.left_frame_pos_y
        if self.direction=="left": 
           self.pos[0]-=self.move_speed
           self.moved_dist+=1
        elif self.direction=="right":
           self.pos[0]+=self.move_speed
           self.moved_dist+=1
        if self.moved_dist>=self.max_dist and self.direction=="left":
           self.direction="right"
           self.moved_dist=0
           self.current_frame[1]=self.right_frame_pos_y
        elif self.moved_dist>=self.max_dist and self.direction=="right":
           self.direction="left"
           self.moved_dist=0
           self.current_frame[1]=self.left_frame_pos_y
           
    def make_perimetre(self):
        step=int(360/self.ver_cells)
        self.perimetre=[337]
        for i in range(22,360,step):
            self.perimetre.append(i)


class Npc:
    image=make_image(PATH+"jap.png",SCALE)
    image=image.subsurface(0,512,image.get_width()/5,image.get_height()/8)
    shadow=make_image(PATH+"rambito_shadow.png",SCALE)
    shadow=shadow.subsurface(0,512,shadow.get_width()/5,shadow.get_height()/8)
    shadow.set_alpha(100)
    
    def __init__(self,pos):
        self.type="npc"
        self.image=Npc.image.convert()
        self.shadow=Npc.shadow.convert()
        self.pos=pos
        self.shadow_pos=self.pos
        self.current_frame=[0,512,128,128]
        self.box=[38,20,50,80]
        self.death=0
        self.dialog=["please help us kill zombies" , "we need your help!"]
    def draw(self,surface,player):
        if self.pos[1]<=player.pos[1]:
           surface.blit(self.shadow,self.shadow_pos)
           surface.blit(self.image,self.pos)
           player.draw(surface)
        elif self.pos[1]>player.pos[1]:
           surface.blit(self.shadow,self.shadow_pos)
           surface.blit(self.image,self.pos)

           
