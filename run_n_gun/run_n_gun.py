import pygame,sys,pickle
from pygame.locals import *
from runngun_classes import *

pygame.init()

#Open Pygame window
screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
#title
pygame.display.set_caption("run n gun")

BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
CLOCK=pygame.time.Clock()
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
PATTH="run_n_gun_data/"

sprite_sheet=pygame.image.load(PATTH+"rambito.png").convert()
shadow=pygame.image.load(PATTH+"rambito_shadow.png").convert()
tileset=pygame.image.load(PATTH+"tileset.png").convert()
alpha_color=sprite_sheet.get_at((0,0))
sprite_sheet.set_colorkey(alpha_color)
shadow.set_colorkey(alpha_color)
shadow.set_alpha(100)
player_pos=[320,240]
player_box=[player_pos[0]+48,player_pos[1]+70]#[45,55]
player_box_width=30#40
player_box_height=30#40
player_direction="up"
move_speed=10
scrol_box=[210,130]
scrol_box_width=220
scrol_box_height=220
scrol_x=0
scrol_y=0
scroling=0
up_limit=576

gun=Gun()
enemy_group=Enemy.group
active_enemy=[]
active_solid_tile=[]

with open('level.lvl', 'rb') as file:
     file_loader=pickle.Unpickler(file)
     level_tile=file_loader.load()
     level_tile_pos=file_loader.load()
     level_solid_tile_index=file_loader.load()
     file_loader.load()
     for pos in file_loader.load():
         Enemy(pos)

top_left_limit=min(level_tile_pos)
bottom_right_limit=max(level_tile_pos)

for i in range(len(level_tile_pos)):
    if top_left_limit==level_tile_pos[i]:
       top_left_limit=i
    elif bottom_right_limit==level_tile_pos[i]:
       bottom_right_limit=i
       
sheet_width=sprite_sheet.get_width()
sheet_height=sprite_sheet.get_height()
hor_cells=5
ver_cells=8
scale=4
sprite_sheet = pygame.transform.scale(sprite_sheet, (sheet_width*scale, sheet_height*scale))
shadow = pygame.transform.scale(shadow, (sheet_width*scale, sheet_height*scale))
cell_width=int(sprite_sheet.get_width()/hor_cells)
cell_height=int(sprite_sheet.get_height()/ver_cells)


tile_width=16*scale
tile_height=16*scale
tileset_width=tileset.get_width()
tileset_height=tileset.get_height()
tileset=pygame.transform.scale(tileset,(tileset_width*scale,tileset_height*scale))

up_frame_pos_y=0
down_frame_pos_y=cell_height*4
right_frame_pos_y=cell_height*2
left_frame_pos_y=cell_height*6
anim_frame=1
max_anim_time=3
anime_time=0
frame_pos_x=0
frame_pos_y=up_frame_pos_y

up = down = left = right = False

def colide(x_pos,y_pos,width,height,x_pos2,y_pos2):
    colision=0
    if x_pos2>x_pos and x_pos2<x_pos+width and y_pos2>y_pos and y_pos2<y_pos+height:
       colision=1
    return colision

pygame.key.set_repeat(400, 30)

while True:
    
    #loop speed limitation
    #30 frames per second is enought
    CLOCK.tick(30)
    
    scrol_x=0
    scrol_y=0
    scroling=0
    active_enemy=[]
    active_solid_tile=[]
    
    for event in pygame.event.get():    #wait for events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == KEYUP:
           anim_frame=1
           frame_pos_x=0
           anime_time=0
           up = down = left = right = False
           
    #Movement controls
    keys = pygame.key.get_pressed()

    if keys[K_UP]:
       up=True
       gun.direction="up"
       player_pos[1]-=move_speed
       if player_pos[1]<0:
          player_pos[1]=0
       frame_pos_y=up_frame_pos_y
       anime_time+=1
       if anime_time>=max_anim_time:
          anime_time=0
          if anim_frame<hor_cells:
             anim_frame+=1
             frame_pos_x+=cell_width
          else:
             anim_frame=2
             frame_pos_x=cell_width
       if up:
          if level_tile_pos[top_left_limit][1]<=-move_speed:
             if player_box[1]<scrol_box[1]:
                player_pos[1]+=move_speed
                scrol_y+=move_speed
                scroling=1
     
    elif keys[K_DOWN]:
       down=True
       gun.direction="down"
       player_pos[1]+=move_speed
       if player_pos[1]>SCREEN_HEIGHT-cell_height:
          player_pos[1]=SCREEN_HEIGHT-cell_height
       frame_pos_y=down_frame_pos_y
       anime_time+=1
       if anime_time>=max_anim_time:
          anime_time=0
          if anim_frame<hor_cells:
             anim_frame+=1
             frame_pos_x+=cell_width
          else:
             anim_frame=2
             frame_pos_x=cell_width
       if down:
          if level_tile_pos[bottom_right_limit][1]>=(SCREEN_HEIGHT+move_speed)-tile_height:
             if player_box[1]+player_box_height>scrol_box[1]+scrol_box_height:
                player_pos[1]-=move_speed
                scrol_y-=move_speed
                scroling=1
                
    if keys[K_RIGHT]:
       right=True
       gun.direction="right"
       player_pos[0]+=move_speed
       if player_pos[0]>SCREEN_WIDTH-cell_width:
          player_pos[0]=SCREEN_WIDTH-cell_width
       frame_pos_y=right_frame_pos_y
       anime_time+=1
       if anime_time>=max_anim_time:
          anime_time=0
          if anim_frame<hor_cells:
             anim_frame+=1
             frame_pos_x+=cell_width
          else:
             anim_frame=2
             frame_pos_x=cell_width
       if right:
          if level_tile_pos[bottom_right_limit][0]>=(SCREEN_WIDTH+move_speed)-tile_width:
             if player_box[0]+player_box_width>scrol_box[0]+scrol_box_width:
                player_pos[0]-=move_speed
                scrol_x-=move_speed
                scroling=1

    elif keys[K_LEFT]:
       left=True
       gun.direction="left"
       player_pos[0]-=move_speed
       if player_pos[0]<0:
          player_pos[0]=0
       frame_pos_y=left_frame_pos_y
       anime_time+=1
       if anime_time>=max_anim_time:
          anime_time=0
          if anim_frame<hor_cells:
             anim_frame+=1
             frame_pos_x+=cell_width
          else:
             anim_frame=2
             frame_pos_x=cell_width
       if left:
          if level_tile_pos[top_left_limit][0]<=-move_speed:
             if player_box[0]<scrol_box[0]:
                player_pos[0]+=move_speed
                scrol_x+=move_speed
                scroling=1
                
    if keys[K_f]:
       gun.fire=1

    if up or down or left or right:
       player_box=[player_pos[0]+48,player_pos[1]+70]
       

    if gun.fire:
       gun.update(player_pos)
       
    for enemy in enemy_group:
        if not enemy.death:
           if scroling:
              enemy.pos[0]+=scrol_x
              enemy.pos[1]+=scrol_y
           if enemy.pos[0]>=-128 and enemy.pos[0]<SCREEN_WIDTH+128 \
           and enemy.pos[1]>=-128 and enemy.pos[1]<SCREEN_HEIGHT+128:
              active_enemy.append(enemy)
           else:
              enemy.blit_ok=0
              


    
    screen.fill(BLACK)
    for i in range(len(level_tile_pos)):
        if scroling:
           level_tile_pos[i][0]+=scrol_x
           level_tile_pos[i][1]+=scrol_y
        if level_tile_pos[i][0]>=-tile_width and level_tile_pos[i][0]<SCREEN_WIDTH \
        and level_tile_pos[i][1]>=-tile_height and level_tile_pos[i][1]<SCREEN_HEIGHT:
            screen.blit(tileset,level_tile_pos[i],(level_tile[i][0],level_tile[i][1],tile_width,tile_height))


    for i in level_solid_tile_index:
        
        if level_tile_pos[i][0]>=-tile_width and level_tile_pos[i][0]<SCREEN_WIDTH+tile_width \
        and level_tile_pos[i][1]>=-tile_height and level_tile_pos[i][1]<SCREEN_HEIGHT+tile_height:

           active_solid_tile.append(i)
            
           if up:
              tile_pos_x=level_tile_pos[i][0]
              tile_pos_y=level_tile_pos[i][1]
              if colide(tile_pos_x,tile_pos_y,tile_width,tile_height,player_box[0],player_box[1]) \
              or colide(tile_pos_x,tile_pos_y,tile_width,tile_height,player_box[0]+player_box_width,player_box[1]):
                 player_pos[1]+=move_speed
           elif down:
              tile_pos_x=level_tile_pos[i][0]
              tile_pos_y=level_tile_pos[i][1]

              if colide(tile_pos_x,tile_pos_y,tile_width,tile_height,player_box[0],player_box[1]+player_box_height) \
              or colide(tile_pos_x,tile_pos_y,tile_width,tile_height,player_box[0]+player_box_width,player_box[1]+player_box_height):
                 player_pos[1]-=move_speed
           if right:
              tile_pos_x=level_tile_pos[i][0]
              tile_pos_y=level_tile_pos[i][1]
              if colide(tile_pos_x,tile_pos_y,tile_width,tile_height,player_box[0]+player_box_width,player_box[1]) \
              or colide(tile_pos_x,tile_pos_y,tile_width,tile_height,player_box[0]+player_box_width,player_box[1]+player_box_height):
                 player_pos[0]-=move_speed
           elif left:
              tile_pos_x=level_tile_pos[i][0]
              tile_pos_y=level_tile_pos[i][1]
              if colide(tile_pos_x,tile_pos_y,tile_width,tile_height,player_box[0],player_box[1]) \
              or colide(tile_pos_x,tile_pos_y,tile_width,tile_height,player_box[0],player_box[1]+player_box_height):
                 player_pos[0]+=move_speed
           if gun.fire:
              if colide(level_tile_pos[i][0],level_tile_pos[i][1],tile_width,tile_height,
              gun.fire_pos[0]+gun.bullet.center[0],gun.fire_pos[1]+gun.bullet.center[1]):
                 gun.fire_pos[0]-=gun.move_x
                 gun.fire_pos[1]-=gun.move_y
                 if not gun.death:
                    gun.moved_dist=gun.max_move_dist

            
    screen.blit(shadow,player_pos,(frame_pos_x,frame_pos_y,cell_width,cell_height))            
    screen.blit(sprite_sheet,player_pos,(frame_pos_x,frame_pos_y,cell_width,cell_height))
    
    for enemy in active_enemy:
        enemy.update(player_pos,gun,active_enemy,active_solid_tile,level_tile_pos)
    active_enemy.sort(key=lambda x:x.pos[1])
    
    for enemy in active_enemy:
        if enemy.blit_ok:
           if enemy.pos[1]<=player_pos[1]:
              screen.blit(shadow,enemy.shadow_pos,enemy.current_frame)
              screen.blit(enemy.image,enemy.pos,enemy.current_frame)
              screen.blit(shadow,player_pos,(frame_pos_x,frame_pos_y,cell_width,cell_height))            
              screen.blit(sprite_sheet,player_pos,(frame_pos_x,frame_pos_y,cell_width,cell_height))
           elif enemy.pos[1]>player_pos[1]:
              screen.blit(shadow,enemy.shadow_pos,enemy.current_frame)
              screen.blit(enemy.image,enemy.pos,enemy.current_frame)
           if enemy.glowing:
              screen.blit(enemy.glow,enemy.pos,enemy.current_frame)
              enemy.glowing=0
        
              
    if gun.fire:
       screen.blit(gun.bullet.image,gun.fire_pos,gun.bullet.current_frame)
       if not gun.death:
          screen.blit(gun.bullet.shadow,gun.fire_pos,gun.bullet.current_frame)

    pygame.display.flip()


