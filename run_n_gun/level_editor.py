import pygame,sys,pickle
from pygame.locals import *

pygame.init()

#Ouverture de la fenêtre Pygame
screen = pygame.display.set_mode((640, 480),) #ajoutez RESIZABLE ou FULLSCREEN
#Titre
pygame.display.set_caption("level editor")
BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
CLOCK=pygame.time.Clock()
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
PATH="run_n_gun_data/"

font=pygame.font.SysFont('Arial', 30)
tileset=pygame.image.load(PATH+"tileset.png").convert()
tileset_pos=[0,0]
move_speed=10

actor=pygame.image.load(PATH+"zombito.png").convert()
alpha_color=actor.get_at((0,0))
actor.set_colorkey(alpha_color)
actor=actor.subsurface(0,0,actor.get_width()/5,actor.get_height()/8)
actor=pygame.transform.scale(actor,(actor.get_width()*4,actor.get_height()*4))
actor_box=[35,20,60,80]
actor_center=[int(actor_box[2]/2),int(actor_box[3]/2)]

tileset_width=tileset.get_width()
tileset_height=tileset.get_height()
scale=4
tileset=pygame.transform.scale(tileset,(tileset_width*scale,tileset_height*scale))

tile_width=16*scale
tile_height=16*scale
hor_tile=(tileset_width*scale)/tile_width
ver_tile=(tileset_height*scale)/tile_height
square_pos=[0,0]
square_size=[tile_width,tile_height]
hiden_square_pos=[0,0]
origin_square=[0,0]
memo_square=[-tile_width,-tile_height,tile_width,tile_height]
square2_pos=[0,0]
square2_size=[tile_width,tile_height]
square_color=(0,200,255)
pointed_tile=[0,0]
selected_tiles=[]
selected_tile_index=0
actor_pos=[0,0]
mouse_pos=[0,0]
screen_mode="select"
edit_mode="tile"
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
hide_bouding_box=0
screen_message=0
message="Welcome"
message_time=50
left_click=False

level_tile=[]
level_tile_pos=[]
level_solid_tile=[]
level_tile_index=[]
level_actor_pos=[]

try:
    with open('level.lvl', 'rb') as file:
         file_loader=pickle.Unpickler(file)
         level_tile=file_loader.load()
         level_tile_pos=file_loader.load()
         file_loader.load()
         level_solid_tile=file_loader.load()
         level_actor_pos=file_loader.load()
except FileNotFoundError: pass


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
    
    #Limitation de vitesse de la boucle
    #30 frames par secondes suffisent
    CLOCK.tick(30)
    
    move_x=0;move_y=0

    if screen_message:
       message_time-=1
       if message_time<=0:
          message_time=50
          screen_message=0
    
    for event in pygame.event.get():    #Attente des événements
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
                     
           elif screen_mode=="edit":
              if event.key == K_UP:
                 moved_distance2_y+=tile_height
              elif event.key == K_DOWN:
                 moved_distance2_y-=tile_height
              if event.key == K_RIGHT:
                 moved_distance2_x-=tile_width
              elif event.key == K_LEFT:
                 moved_distance2_x+=tile_width
                 
              elif event.key == K_d:
                 if solid_tile:
                    solid_tile=0
                    solid="no"
                 elif not solid_tile :
                    solid_tile=1
                    solid="yes"
                    
              elif event.key == K_h:
                 if hide_bouding_box:
                    hide_bouding_box=0
                 elif not hide_bouding_box:
                    hide_bouding_box=1

              elif event.key == K_e:
                 if edit_mode=="tile":
                    edit_mode="actor"
                    screen_message=1
                    message="  Actor  Edit"
                 elif edit_mode=="actor":
                    edit_mode="tile"
                    screen_message=1
                    message="  Tile  Edit"

              elif event.key == K_c:
                 level_tile.clear()
                 level_tile_pos.clear()
                 level_solid_tile.clear()
                 #level_tile_index.clear()
                 level_actor_pos.clear()
                 screen_message=1
                 message="Level  Cleared"
                 
              elif event.key == K_RETURN:
                  level_solid_tile_index=[]
                  for i in range(len(level_tile)):
                      if level_solid_tile[i]==1:
                         level_solid_tile_index.append(i)
                  with open('level.lvl', 'wb') as file:
                       file_saver=pickle.Pickler(file)
                       file_saver.dump(level_tile)
                       file_saver.dump(level_tile_pos)
                       file_saver.dump(level_solid_tile_index)
                       file_saver.dump(level_solid_tile)
                       #file_saver.dump(level_tile_index)
                       file_saver.dump(level_actor_pos)
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
                      
           elif screen_mode=="edit" and edit_mode=="actor":
              mouse_pos=event.pos

                                    
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
              if not [selected_cell[0],selected_cell[1]] in level_tile_pos:
                 level_tile.append([tile[0],tile[1]])
                 level_tile_pos.append([selected_cell[0],selected_cell[1]])
                 level_solid_tile.append(solid_tile)
                 #level_tile_index.append(selected_tile_index)
       #elif event.button == 3:
       elif buttons[2]:
          selected_cell[0]=pointed_cell[0]-moved_distance2_x
          selected_cell[1]=pointed_cell[1]-moved_distance2_y
          #selected_cell=pointed_cell
          for i in range(len(level_tile_pos)):
              if [selected_cell[0],selected_cell[1]]==level_tile_pos[i]:
                 del level_tile_pos[i]
                 del level_tile[i]
                 del level_solid_tile[i]
                 #del level_tile_index[i]
                 break
                
    elif screen_mode=="edit" and edit_mode=="actor":
       if buttons[0]:
          actor_pos[0]=mouse_pos[0]-moved_distance2_x-actor_box[0]
          actor_pos[1]=mouse_pos[1]-moved_distance2_y-actor_box[1]
          if not [actor_pos[0],actor_pos[1]] in level_actor_pos:
             level_actor_pos.append([actor_pos[0],actor_pos[1]])
       elif buttons[2]:
          for i,pos in enumerate(level_actor_pos):
             pos_x=pos[0]+actor_box[0]+moved_distance2_x
             pos_y=pos[1]+actor_box[1]+moved_distance2_y
             if mouse_pos[0]>pos_x and mouse_pos[0]<pos_x+actor_box[2] \
             and mouse_pos[1]>pos_y and mouse_pos[1]<pos_y+actor_box[3]:
                 del level_actor_pos[i]
                 
    screen.fill(BLACK)
    if screen_mode=="select":
       screen.blit(tileset,tileset_pos)
       pygame.draw.rect(screen, (200,200,200), [memo_square[0], memo_square[1], memo_square[2], memo_square[3]], 4)
       pygame.draw.rect(screen, square_color, [square_pos[0], square_pos[1], square_size[0], square_size[1]], 4)

    elif screen_mode=="edit":
       if edit_mode=="tile":
          pygame.draw.rect(screen, (0,200,255), [square2_pos[0], square2_pos[1], square2_size[0], square2_size[1]], 4)
          for tile in selected_tiles:
              screen.blit(tileset,(square2_pos[0]+tile[2],square2_pos[1]+tile[3]),(tile[0],tile[1],tile_width,tile_height))
       for i in range(len(level_tile)):
           pos_x=level_tile_pos[i][0]+moved_distance2_x
           pos_y=level_tile_pos[i][1]+moved_distance2_y
           if pos_x>=0 and pos_x<SCREEN_WIDTH and pos_y>=0 and pos_y<SCREEN_HEIGHT:
              screen.blit(tileset,(level_tile_pos[i][0]+moved_distance2_x,level_tile_pos[i][1]+moved_distance2_y),
              (level_tile[i][0],level_tile[i][1],tile_width,tile_height))
              if level_solid_tile[i] and not hide_bouding_box:
                 pygame.draw.rect(screen, (255,200,0), [pos_x, pos_y, tile_width, tile_height], 4)
       if edit_mode=="actor":
          for pos in level_actor_pos:
              pos_x=pos[0]+moved_distance2_x
              pos_y=pos[1]+moved_distance2_y
              if pos_x>=0 and pos_x<SCREEN_WIDTH and pos_y>=0 and pos_y<SCREEN_HEIGHT:
                 screen.blit(actor,(pos_x,pos_y))
          screen.blit(actor,(mouse_pos[0]-actor_box[0],mouse_pos[1]-actor_box[1]))
                  
       text=font.render(("x:"+str(moved_distance2_x)), True, (250,250,250))
       screen.blit(text,(0,420))
       text=font.render(("y:"+str(moved_distance2_y)), True, (250,250,250))
       screen.blit(text,(0,445))
       text=font.render(("solide tile: "+solid), True, (250,250,0))
       screen.blit(text,(450,445))
       
    if screen_message:
       text=font.render(message, True, (255,250,255))
       screen.blit(text,(230,220))
       
    pygame.display.flip()
    
           
