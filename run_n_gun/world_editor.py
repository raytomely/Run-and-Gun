import pygame,sys,pickle
from pygame.locals import *

pygame.init()

#open Pygame window
screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
#title
pygame.display.set_caption("level editor")
BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
CLOCK=pygame.time.Clock()
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
SCALE=4
PATH="run_n_gun_data/"


class Area:
    def __init__(self,name):
        self.name=name
        self.tile=[]
        self.tile_pos=[]
        self.tile_type=[]
        self.tileset_index=[]
        self.actor_pos=[]
        self.actor_index=[]
        self.gate_pos=[]
        self.connected_area=[]
        self.connected_area_pos=[]
        self.area_moved_dist=[]

level=[Area("central area"),Area("north area"),
       Area("south area"),Area("east area"),
       Area("west area"),Area("secret place")]

level_index=0
current_area=level[level_index]

font=pygame.font.SysFont('Arial', 30)

tileset=[pygame.image.load(PATH+"tileset.png").convert(),
         pygame.image.load(PATH+"tileset2.png").convert()]

tileset_width=tileset[0].get_width()
tileset_height=tileset[0].get_height()
for i in range(len(tileset)):
    tileset[i]=pygame.transform.scale(tileset[i],(tileset_width*SCALE,tileset_height*SCALE))
tileset_index=0
current_tileset=tileset[tileset_index]

tileset_pos=[0,0]
move_speed=10

actor=[pygame.image.load(PATH+"zombito.png").convert(),
       pygame.image.load(PATH+"jap.png").convert()]
alpha_color=actor[0].get_at((0,0))
for i in range(len(actor)):
    actor[i].set_colorkey(alpha_color)
    actor[i]=actor[i].subsurface(0,0,actor[i].get_width()/5,actor[i].get_height()/8)
    actor[i]=pygame.transform.scale(actor[i],(actor[i].get_width()*SCALE,actor[i].get_height()*SCALE))
actor_box=[35,20,60,80]
actor_center=[int(actor_box[2]/2),int(actor_box[3]/2)]
actor_index=0
current_actor=actor[actor_index]


hero=pygame.image.load(PATH+"rambito.png").convert()
hero.set_colorkey(alpha_color)
hero=hero.subsurface(0,0,hero.get_width()/5,hero.get_height()/8)
hero=pygame.transform.scale(hero,(hero.get_width()*SCALE,hero.get_height()*SCALE))

start={'pos':[0,0],'area':0,'moved_dist':[0,0]}


tile_width=16*SCALE
tile_height=16*SCALE
hor_tile=(tileset_width*SCALE)/tile_width
ver_tile=(tileset_height*SCALE)/tile_height
square_pos=[0,0]
square_size=[tile_width,tile_height]
hiden_square_pos=[0,0]
origin_square=[0,0]
memo_square=[-1000,-1000,tile_width,tile_height]
square2_pos=[0,0]
square2_size=[tile_width,tile_height]
square_color=(0,200,255)
pointed_tile=[0,0]
selected_tiles=[]
selected_tile_index=0
actor_pos=[0,0]
mouse_pos=[0,0]
screen_mode="select"
edit_modes=["tile","actor","hero"]
edit_mode_index=0
edit_mode=edit_modes[edit_mode_index]
moved_distance_x=0
moved_distance_y=0
moved_distance2_x=0
moved_distance2_y=0
hor_cell=SCREEN_WIDTH/tile_width
ver_cell=SCREEN_HEIGHT/tile_height
pointed_cell=[0,0]
selected_cell=[0,0]
solid_tile=0
solid="no"
hide_bounding_box=0
screen_message=0
message="Welcome"
message_time=50
left_click=False
level_tile_type=["normal","solid","gate"]
tile_type_index=0
tile_type=level_tile_type[tile_type_index]
connected_area=0
connected_area_pos=[0,0]
moved_dist=[0,0]

level_tile=[]
level_tile_pos=[]
level_solid_tile=[]
level_tile_index=[]
level_actor_pos=[]

try:
    with open('level_2.lvl', 'rb') as file:
         file_loader=pickle.Unpickler(file)
         level=file_loader.load()
         start=file_loader.load()
except FileNotFoundError: pass

level_index=0
current_area=level[level_index]


tile_pos=[]
tile_x=0
tile_y=0

for i in range(int(ver_tile)):
    tile_x=0
    for j in range(int(hor_tile)):
        tile_pos.append([tile_x,tile_y])
        tile_x+=tile_width
    tile_y+=tile_height

cell_pos=[]
cell_x=0
cell_y=0

for i in range(int(ver_cell)):
    cell_x=0
    for j in range(int(hor_cell)):
        cell_pos.append([cell_x,cell_y])
        cell_x+=tile_width
    cell_y+=tile_height

                          
pygame.key.set_repeat(400, 30)

while True:
    
    #loop speed limitation
    #30 frames per second is enought
    CLOCK.tick(30)
    
    move_x=0;move_y=0

    if screen_message:
       message_time-=1
       if message_time<=0:
          message_time=50
          screen_message=0
    
    for event in pygame.event.get():    #wait for events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
           if screen_mode=="select":
              if event.key == K_UP:
                 tileset_pos[1]-=move_speed
                 move_y-=move_speed
                 moved_distance_y-=move_speed
                 memo_square[1]-=move_speed
              elif event.key == K_DOWN:
                 tileset_pos[1]+=move_speed
                 move_y+=move_speed
                 moved_distance_y+=move_speed
                 memo_square[1]+=move_speed
              if event.key == K_RIGHT:
                 tileset_pos[0]+=move_speed
                 move_x+=move_speed
                 moved_distance_x+=move_speed
                 memo_square[0]+=move_speed
              elif event.key == K_LEFT:
                 tileset_pos[0]-=move_speed
                 move_x-=move_speed
                 moved_distance_x-=move_speed
                 memo_square[0]-=move_speed

              if move_x!=0 or move_y!=0:
                 for i in range(len(tile_pos)):
                     tile_pos[i][0]+=move_x
                     tile_pos[i][1]+=move_y
                     
              if event.key == K_o:
                 if tileset_index<len(tileset)-1:
                    tileset_index+=1
                 else:
                    tileset_index=0
                 current_tileset=tileset[tileset_index]
                 tileset_pos=[0,0]
                 moved_distance_x=0
                 moved_distance_y=0
                 memo_square[0]=-1000
                 memo_square[1]=-1000
                 square2_size=[tile_width,tile_height]
                 selected_tiles=[]

                     
           elif screen_mode=="edit":
              if event.key == K_UP:
                 moved_distance2_y+=tile_height
              elif event.key == K_DOWN:
                 moved_distance2_y-=tile_height
              if event.key == K_RIGHT:
                 moved_distance2_x-=tile_width
              elif event.key == K_LEFT:
                 moved_distance2_x+=tile_width
                 
              elif event.key == K_t:
                 if tile_type_index<len(level_tile_type)-1:
                    tile_type_index+=1
                    tile_type=level_tile_type[tile_type_index]
                 else:
                    tile_type_index=0
                    tile_type=level_tile_type[tile_type_index]
                    
              elif event.key == K_h:
                 if hide_bouding_box:
                    hide_bouding_box=0
                 elif not hide_bouding_box:
                    hide_bouding_box=1

              elif event.key == K_e:
                 if edit_mode_index<len(edit_modes)-1:
                    edit_mode_index+=1
                 else:
                    edit_mode_index=0
                 edit_mode=edit_modes[edit_mode_index]
                 screen_message=1
                 message="  "+edit_mode.title()+"  Edit" 


              elif event.key == K_n:
                   connected_area=level_index
                   connected_area_pos=[mouse_pos[0],mouse_pos[1]]
                   moved_dist=[moved_distance2_x,moved_distance2_y]
                   screen_message=1
                   message="Area  Selected"
           
              elif event.key == K_l:
                 if level_index<len(level)-1:
                    level_index+=1
                    current_area=level[level_index]
                    screen_message=1
                    message=current_area.name
                    moved_distance2_x=0
                    moved_distance2_y=0
              elif event.key == K_p:
                 if level_index>0:
                    level_index-=1
                    current_area=level[level_index]
                    screen_message=1
                    message=current_area.name
                    moved_distance2_x=0
                    moved_distance2_y=0

              elif event.key == K_o:
                 if edit_mode=="actor":
                    if actor_index<len(actor)-1:
                       actor_index+=1
                       current_actor=actor[actor_index]
                    else:
                       actor_index=0
                       current_actor=actor[actor_index]

              elif event.key == K_c:
                 current_area.tile.clear()
                 current_area.tile_pos.clear()
                 current_area.tile_type.clear()
                 current_area.tileset_index.clear()
                 current_area.gate_pos.clear()
                 current_area.connected_area.clear()
                 current_area.connected_area_pos.clear()
                 current_area.area_moved_dist.clear()
                 #level_tile_index.clear()
                 current_area.actor_pos.clear()
                 current_area.actor_index.clear()
                 screen_message=1
                 message="Level  Cleared"
                 
              elif event.key == K_RETURN:
                  #level_solid_tile_index=[]
                  for area in level:
                      area.solid_tile_index=[]
                      if len(area.tile_pos)>0:
                         top_left_limit=min(area.tile_pos)
                         bottom_right_limit=max(area.tile_pos)
                         for i in range(len(area.tile_pos)):
                             if top_left_limit==area.tile_pos[i]:
                                area.top_left_limit=i
                             elif bottom_right_limit==area.tile_pos[i]:
                                area.bottom_right_limit=i
                      for i in range(len(area.tile)):
                          if area.tile_type[i]=="solid":
                             area.solid_tile_index.append(i)
                  with open('level_2.lvl', 'wb') as file:
                       file_saver=pickle.Pickler(file)
                       file_saver.dump(level)
                       file_saver.dump(start)
                  screen_message=1
                  message="Level  Saved"
                           
           if event.key == K_s:
              if screen_mode=="select":
                 screen_mode="edit"
                 screen_message=1
                 message="Edit  Screen"
              elif screen_mode=="edit":
                 screen_mode="select"
                 screen_message=1
                 message="Select  Screen"

                               
        if event.type == MOUSEMOTION:
           mouse_pos=event.pos
           if screen_mode=="select":
              if not left_click:
                 for index,pos in enumerate(tile_pos):
                     if event.pos[0]>pos[0]and event.pos[0]<pos[0]+tile_width \
                     and event.pos[1]>pos[1]and event.pos[1]<pos[1]+tile_height:
                         square_pos[0]=pos[0]
                         square_pos[1]=pos[1]
                         hiden_square_pos[0]=square_pos[0]
                         hiden_square_pos[1]=square_pos[1]
                         origin_square[0]=square_pos[0]
                         origin_square[1]=square_pos[1]
                         #square_pos=pos
                         pointed_tile[0]=pos[0]
                         pointed_tile[1]=pos[1]
                         #pointed_tile=pos
                         selected_tile_index=index
                         
              elif left_click: 
                 if event.pos[0]>hiden_square_pos[0]+tile_width:
                    if square_pos[0]==origin_square[0]:
                       square_size[0]+=tile_width
                       hiden_square_pos[0]+=tile_width
                    else:
                       square_pos[0]+=tile_width
                       square_size[0]-=tile_width
                       hiden_square_pos[0]+=tile_width
                 if event.pos[1]>hiden_square_pos[1]+tile_height:
                    if square_pos[1]==origin_square[1]:
                       square_size[1]+=tile_height
                       hiden_square_pos[1]+=tile_height
                    else:
                       square_pos[1]+=tile_height
                       square_size[1]-=tile_height
                       hiden_square_pos[1]+=tile_height
                 if event.pos[0]<hiden_square_pos[0]:
                    if hiden_square_pos[0]!=square_pos[0]:
                       square_size[0]-=tile_width
                       hiden_square_pos[0]-=tile_width
                    else:
                       square_pos[0]-=tile_width
                       square_size[0]+=tile_width
                       hiden_square_pos[0]-=tile_width
                 if event.pos[1]<hiden_square_pos[1]:
                    if hiden_square_pos[1]!=square_pos[1]:
                       square_size[1]-=tile_height
                       hiden_square_pos[1]-=tile_height
                    else:
                       square_pos[1]-=tile_height
                       square_size[1]+=tile_height
                       hiden_square_pos[1]-=tile_height
                      
           elif screen_mode=="edit" and edit_mode=="tile":
              for pos in cell_pos:
                  if event.pos[0]>pos[0]and event.pos[0]<pos[0]+tile_width \
                  and event.pos[1]>pos[1]and event.pos[1]<pos[1]+tile_height:
                      square2_pos[0]=pos[0]
                      square2_pos[1]=pos[1]
                      #square2_pos=pos
                      pointed_cell[0]=pos[0]
                      pointed_cell[1]=pos[1]
                      #pointed_cell=pos
              
                                    
        if event.type == MOUSEBUTTONUP:
           if screen_mode=="select":
              if event.button == 1:
                 left_click=False
                 square_color=(0,200,255)
                 selected_tiles=[]
                 pointed_tile[0]=square_pos[0]
                 pointed_tile[1]=square_pos[1]
                 for y in range(0,square_size[1],tile_height):
                     pointed_tile[0]=square_pos[0]
                     for x in range(0,square_size[0],tile_width):
                         selected_tile_x=pointed_tile[0]-moved_distance_x
                         selected_tile_y=pointed_tile[1]-moved_distance_y
                         selected_tiles.append([selected_tile_x,selected_tile_y,x,y])
                         pointed_tile[0]+=tile_width
                     pointed_tile[1]+=tile_height
                 square2_size[0]=square_size[0]
                 square2_size[1]= square_size[1]
                 memo_square[0]=square_pos[0]
                 memo_square[1]=square_pos[1]
                 memo_square[2]=square_size[0]
                 memo_square[3]=square_size[1]
                 square_size[0]= tile_width
                 square_size[1]=tile_height
                 square_pos[0]=hiden_square_pos[0]
                 square_pos[1]=hiden_square_pos[1]                            
              
        if event.type == MOUSEBUTTONDOWN:
           if screen_mode=="select":
              if event.button == 1:
                 left_click=True
                 square_color=(255,200,0)
                 #selected_tile=pointed_tile
                 
                 
    buttons=pygame.mouse.get_pressed()
    
    if screen_mode=="edit" and edit_mode=="tile": 
       #if event.button == 1:
       if buttons[0]:
          for tile in selected_tiles:
              selected_cell[0]=pointed_cell[0]-moved_distance2_x+tile[2]
              selected_cell[1]=pointed_cell[1]-moved_distance2_y+tile[3]
              #selected_cell=pointed_cell
              if not [selected_cell[0],selected_cell[1]] in current_area.tile_pos:
                 current_area.tile.append([tile[0],tile[1]])
                 current_area.tile_pos.append([selected_cell[0],selected_cell[1]])
                 current_area.tile_type.append(tile_type)
                 current_area.tileset_index.append(tileset_index)
                 #level_tile_index.append(selected_tile_index)
                 if tile_type=="gate":
                    current_area.gate_pos.append([selected_cell[0],selected_cell[1]])
                    current_area.connected_area.append(connected_area)
                    current_area.connected_area_pos.append(connected_area_pos)
                    current_area.area_moved_dist.append(moved_dist)
             
       #elif event.button == 3:
       elif buttons[2]:
          selected_cell[0]=pointed_cell[0]-moved_distance2_x
          selected_cell[1]=pointed_cell[1]-moved_distance2_y
          #selected_cell=pointed_cell
          for i in range(len(current_area.tile_pos)):
              if [selected_cell[0],selected_cell[1]]==current_area.tile_pos[i]:
                 if current_area.tile_type[i]=="gate":
                    for j in range(len(current_area.gate_pos)):
                        if [selected_cell[0],selected_cell[1]]==current_area.gate_pos[j]:
                           del current_area.gate_pos[j]
                           del current_area.connected_area[j]
                           del current_area.connected_area_pos[j]
                           del current_area.area_moved_dist[j]
                           break
                 del current_area.tile_pos[i]
                 del current_area.tile[i]
                 del current_area.tile_type[i]
                 del current_area.tileset_index[i]
                 #del level_tile_index[i]
                 break
                
    elif screen_mode=="edit" and edit_mode=="actor":
       if buttons[0]:
          actor_pos[0]=mouse_pos[0]-moved_distance2_x-actor_box[0]
          actor_pos[1]=mouse_pos[1]-moved_distance2_y-actor_box[1]
          if not [actor_pos[0],actor_pos[1]] in current_area.actor_pos:
             current_area.actor_pos.append([actor_pos[0],actor_pos[1]])
             current_area.actor_index.append(actor_index)
       elif buttons[2]:
          for i,pos in enumerate(current_area.actor_pos):
             pos_x=pos[0]+actor_box[0]+moved_distance2_x
             pos_y=pos[1]+actor_box[1]+moved_distance2_y
             if mouse_pos[0]>pos_x and mouse_pos[0]<pos_x+actor_box[2] \
             and mouse_pos[1]>pos_y and mouse_pos[1]<pos_y+actor_box[3]:
                 del current_area.actor_pos[i]
                 del current_area.actor_index[i]

    elif screen_mode=="edit" and edit_mode=="hero":
       if buttons[0]:
          start['pos'][0]=mouse_pos[0]
          start['pos'][1]=mouse_pos[1]
          start['area']=level_index
          start['moved_dist'][0]=moved_distance2_x
          start['moved_dist'][1]=moved_distance2_y
       elif buttons[2]:
          if mouse_pos[0]>start['pos'][0] and mouse_pos[0]<start['pos'][0]+hero.get_width() \
          and mouse_pos[1]>start['pos'][1] and mouse_pos[1]<start['pos'][1]+hero.get_height():
             start['pos']=[0,0]
             start['area']=0
             start['moved_dist']=[0,0]

             
                 
    screen.fill(BLACK)
    if screen_mode=="select":
       screen.blit(current_tileset,tileset_pos)
       pygame.draw.rect(screen, (200,200,200), [memo_square[0], memo_square[1], memo_square[2], memo_square[3]], 4)
       pygame.draw.rect(screen, square_color, [square_pos[0], square_pos[1], square_size[0], square_size[1]], 4)

    elif screen_mode=="edit":
       if edit_mode=="tile":
          pygame.draw.rect(screen, (0,200,255), [square2_pos[0], square2_pos[1], square2_size[0], square2_size[1]], 4)
          for tile in selected_tiles:
              screen.blit(current_tileset,(square2_pos[0]+tile[2],square2_pos[1]+tile[3]),(tile[0],tile[1],tile_width,tile_height))
       for i in range(len(current_area.tile)):
           pos_x=current_area.tile_pos[i][0]+moved_distance2_x
           pos_y=current_area.tile_pos[i][1]+moved_distance2_y
           if pos_x>=0 and pos_x<SCREEN_WIDTH and pos_y>=0 and pos_y<SCREEN_HEIGHT:
              screen.blit(tileset[current_area.tileset_index[i]],(pos_x,pos_y),
              (current_area.tile[i][0],current_area.tile[i][1],tile_width,tile_height))
              if current_area.tile_type[i]=="solid" and not hide_bounding_box:
                 pygame.draw.rect(screen, (255,200,0), [pos_x, pos_y, tile_width, tile_height], 4)
              elif current_area.tile_type[i]=="gate" and not hide_bounding_box:
                 pygame.draw.rect(screen, (0,200,255), [pos_x, pos_y, tile_width, tile_height], 4)
                 
       if edit_mode=="actor":
          for i,pos in enumerate(current_area.actor_pos):
              pos_x=pos[0]+moved_distance2_x
              pos_y=pos[1]+moved_distance2_y
              if pos_x>=-128 and pos_x<SCREEN_WIDTH and pos_y>=-128 and pos_y<SCREEN_HEIGHT:
                 screen.blit(actor[current_area.actor_index[i]],(pos_x,pos_y))
          screen.blit(current_actor,(mouse_pos[0]-actor_box[0],mouse_pos[1]-actor_box[1]))

       if edit_mode=="hero":
          screen.blit(hero,(mouse_pos[0],mouse_pos[1]))
          pygame.draw.rect(screen, (0,200,255), [mouse_pos[0]+48,mouse_pos[1]+70,30,30], 4)
          if level_index==start['area']:
             pos_x=start['pos'][0]-start['moved_dist'][0]+moved_distance2_x
             pos_y=start['pos'][1]-start['moved_dist'][1]+moved_distance2_y
             screen.blit(hero,(pos_x,pos_y))
          
       text=font.render(("x:"+str(moved_distance2_x)), True, (250,250,250))
       screen.blit(text,(0,420))
       text=font.render(("y:"+str(moved_distance2_y)), True, (250,250,250))
       screen.blit(text,(0,445))
       text=font.render(("tile type: "+tile_type), True, (250,250,0))
       screen.blit(text,(400,445))
              
    if screen_message:
       text=font.render(message, True, (255,250,255))
       screen.blit(text,(230,220))
       
    pygame.display.flip()
    
           
