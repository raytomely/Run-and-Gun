import pygame,sys,pickle
from pygame.locals import *
from runngun_classes2 import *
import dialog

pygame.init()

#Open Pygame windos
screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
#title
pygame.display.set_caption("run n gun")

BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
CLOCK=pygame.time.Clock()
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
SCALE=4
PATH="run_n_gun_data/"

class Tile:
    def __init__(self,image_offset,pos,tile_type,tileset_index):
        self.image_offset=image_offset
        self.pos=pos
        self.type=tile_type
        self.tileset_index=tileset_index
        #self.connected_area=None
        #self.connected_area_pos=None
        #self.area_moved_dist=None

class Area:
    def __init__(self,name):
        self.name=name
        self.tile=[]
        self.actor_pos=[]
        self.actor_index=[]


tileset=[pygame.image.load(PATH+"tileset.png").convert(),
         pygame.image.load(PATH+"tileset2.png").convert()]
tileset_width=tileset[0].get_width()
tileset_height=tileset[0].get_height()
for i in range(len(tileset)):
    tileset[i]=pygame.transform.scale(tileset[i],(tileset_width*SCALE,tileset_height*SCALE))
    
tile_width=16*SCALE
tile_height=16*SCALE
scroll_box=Rect(210,130,220,220)
scroll_x=0
scroll_y=0
scrolling=0
actor_type=[Enemy,Npc]

with open('level_3.lvl', 'rb') as file:
     file_loader=pickle.Unpickler(file)
     level=file_loader.load()
     start=file_loader.load()

player=Player(start["pos"])
move_speed=player.move_speed
gun=Gun()
enemy_group=Enemy.group
active_actor=[]
active_solid_tile=[]
dialoging=0
font=pygame.font.SysFont('Arial', 25)
dialogbox = dialog.DialogBox((240*2, 51*2), (0, 0, 0),
    (255, 255, 255), font)

  
for area in level:
    area.actor_group=[]
    for i,pos in enumerate(area.actor_pos):
        index=area.actor_index[i]
        actor=actor_type[index](pos)
        actor.initial_pos=[pos[0],pos[1]]
        area.actor_group.append(actor)

current_area=level[start["area"]]

for tile in current_area.tile:
    tile.pos[0]+=start["moved_dist"][0]
    tile.pos[1]+=start["moved_dist"][1]


top_left_limit=current_area.top_left_limit
bottom_right_limit=current_area.bottom_right_limit


up = down = left = right =  fire = False

#pygame.key.set_repeat(400, 30)

while True:
    
    #loop speed limitation
    #30 frames per second is enought
    CLOCK.tick(30)
    
    scroll_x=0
    scroll_y=0
    scrolling=0
    active_actor=[]
    active_solid_tile=[]
    
    for event in pygame.event.get():    #wait for events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == KEYDOWN:
           if event.key == K_UP:
              up=True
           elif event.key == K_DOWN:
              down=True
           if event.key == K_RIGHT:
              right=True
           elif event.key == K_LEFT:
              left=True
           if event.key == K_f:
              fire=True
              
           if dialoging:
              if not dialogbox.over():
                 dialogbox.progress()
              else:
                 dialoging=0
            
        if event.type == KEYUP:
           if event.key == K_UP:
              up=False
              player.yvel=0
           elif event.key == K_DOWN:
              down=False
              player.yvel=0
           if event.key == K_RIGHT:
              right=False
              player.xvel=0
           elif event.key == K_LEFT:
              left=False
              player.xvel=0
           if event.key == K_f:
              fire=False
              
           player.anim_frame=1
           player.current_frame[0]=0
           player.anim_time=0
           
                            
    #Movement controls

    if up:
       gun.direction="up"
       player.update("up")
       if current_area.tile[top_left_limit].pos[1]<=-move_speed:
          if player.box[1]<scroll_box.top:
             player.pos[1]+=move_speed
             scroll_y+=move_speed
             scrolling=1       
     
    elif down:
       gun.direction="down"
       player.update("down")
       if current_area.tile[bottom_right_limit].pos[1]>=(SCREEN_HEIGHT+move_speed)-tile_height:
          if player.box[1]+player.box[3]>scroll_box.bottom:
             player.pos[1]-=move_speed
             scroll_y-=move_speed
             scrolling=1       
                
    if right:
       gun.direction="right"
       player.update("right")
       if current_area.tile[bottom_right_limit].pos[0]>=(SCREEN_WIDTH+move_speed)-tile_width:
          if player_box[0]+player_box[2]>scroll_box.right:
             player.pos[0]-=move_speed
             scroll_x-=move_speed
             scrolling=1       

    elif left:
       gun.direction="left"
       player.update("left")
       if current_area.tile[top_left_limit].pos[0]<=-move_speed:
          if player.box[0]<scroll_box.left:
             player.pos[0]+=move_speed
             scroll_x+=move_speed
             scrolling=1
                                 
    if fire:
       if not gun.fire:
          gun.fire=1
          
    if gun.fire:
       gun.update(player.pos)

       
    for actor in current_area.actor_group:
        if not actor.death:
           if scrolling:
              actor.pos[0]+=scroll_x
              actor.pos[1]+=scroll_y
           if actor.pos[0]>=-128 and actor.pos[0]<SCREEN_WIDTH+128 \
           and actor.pos[1]>=-128 and actor.pos[1]<SCREEN_HEIGHT+128:
              active_actor.append(actor)
           else:
              actor.blit_ok=0
        else:
           current_area.actor_group.remove(actor)
              

              
    screen.fill(BLACK)
    for i in range(len(current_area.tile)):
        tile=current_area.tile[i]
        if scrolling:
           tile.pos[0]+=scroll_x
           tile.pos[1]+=scroll_y
        if tile.pos[0]>=-tile_width and tile.pos[0]<SCREEN_WIDTH \
        and tile.pos[1]>=-tile_height and tile.pos[1]<SCREEN_HEIGHT:
           screen.blit(tileset[tile.tileset_index],tile.pos,tile.image_offset)
            
           if tile.type=="solid":

              active_solid_tile.append(i)
           
              if left or right or up or down:
                 tile_rect=[tile.pos[0],tile.pos[1],tile_width,tile_height]
                 if rect_collision(player.box,tile_rect):
                    player.pos[0]-=player.xvel
                    player.pos[1]-=player.yvel
                    player.box[0]=player.pos[0]+48
                    player.box[1]=player.pos[1]+70
                    #break
              if gun.fire:
                 if collide([gun.fire_pos[0]+gun.bullet.center[0],gun.fire_pos[1]+gun.bullet.center[1]],
                 [tile.pos[0],tile.pos[1],tile_width,tile_height]):
                    gun.fire_pos[0]-=gun.move_x
                    gun.fire_pos[1]-=gun.move_y
                    if not gun.death:
                       gun.moved_dist=gun.max_move_dist
           
           elif tile.type=="gate":
              
              if left or right or up or down:
                 tile_rect=[tile.pos[0],tile.pos[1],tile_width,tile_height]
                 if rect_collision(player.box,tile_rect):
                    player.pos=[tile.connected_area_pos[0],tile.connected_area_pos[1]]
                    player.box[0]=player.pos[0]+48
                    player.box[1]=player.pos[1]+70
                    moved_dist=tile.area_moved_dist
                    current_area=level[tile.connected_area]
                    top_left_limit=current_area.top_left_limit
                    bottom_right_limit=current_area.bottom_right_limit
                    old_moved_dist=[current_area.tile[top_left_limit].pos[0],current_area.tile[top_left_limit].pos[1]]
                    for tile  in current_area.tile:
                        tile.pos[0]+=moved_dist[0]-old_moved_dist[0]
                        tile.pos[1]+=moved_dist[1]-old_moved_dist[1]
                    for actor in current_area.actor_group:
                        actor.pos[0]=actor.initial_pos[0]
                        actor.pos[1]=actor.initial_pos[1]

                     
    for actor in active_actor:
        if actor.type=="enemy":
           actor.update(player.pos,gun,active_actor,active_solid_tile,current_area.tile)
        else:
           if left or right or up or down:
              actor_rect=[actor.pos[0]+actor.box[0],actor.pos[1]+actor.box[1],actor.box[2],actor.box[3]]
              if rect_collision(player.box,actor_rect):
                 player.pos[0]-=player.xvel
                 player.pos[1]-=player.yvel
                 player.box[0]=player.pos[0]+48
                 player.box[1]=player.pos[1]+70
                 if not dialoging:
                    dialoging=1
                    dialogbox.set_dialog(actor.dialog)
           
    active_actor.sort(key=lambda x:x.pos[1])
           
                                   
    player.draw(screen)
        
    for actor in active_actor:
        actor.draw(screen,player)
           
    if gun.fire:
       gun.draw(screen)
       
    dialogbox.draw(screen, (8, 8))
    
    pygame.display.flip()


