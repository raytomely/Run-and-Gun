import pygame,sys,tkinter
from pygame.locals import *
from tkinter import filedialog

pygame.init()

#Ouverture de la fenêtre Pygame
screen = pygame.display.set_mode((640, 480),) #ajoutez RESIZABLE ou FULLSCREEN
#Titre
pygame.display.set_caption("image analyzer")
BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
CLOCK=pygame.time.Clock()
SCREEN_WIDTH=640
SCREEN_HEIGHT=480

tk_root = tkinter.Tk()
tk_root.withdraw()

#os.listdir()
#str.endswith()
#if file[-4:] != '.txt': file += '.txt'

#file_name =filedialog.askopenfilename()

font=pygame.font.SysFont('Arial', 30)

image=0
image2=0
image_pos=[0,0]
image_width=0
image_height=0
move_speed=128
scale_x=0
scale_y=0

square_pos=[0,0]
square2_pos=[0,0]
square_color=(0,200,255)
square_width=64
square_height=64

screen_message=0
message="Welcome"
message_time=50
show_info=1

pygame.key.set_repeat(400, 30)

while True:
    
    #Limitation de vitesse de la boucle
    #30 frames par secondes suffisent
    CLOCK.tick(30)
    
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
           if event.key == K_l:
               
              file_name =filedialog.askopenfilename()
              
              try:
                  image=pygame.image.load(file_name).convert()
                  image2=pygame.image.load(file_name).convert()
                  image_width=image.get_width()
                  image_height=image.get_height()
              except:
                  screen_message=1
                  message="couln't open image"

           elif event.key == K_RETURN:
                print("image width: "+str(image_width)," ","image height: "+str(image_height),"\n"
                      "square width: "+str(square_width)," ","square height: "+str(square_height),"\n"
                      "x: "+str(square_pos[0])," ","y: "+str(square_pos[1]),"\n"+
                      str([square_pos[0],square_pos[1],square_width,square_height]))
                      
           if image!=0:
              if event.key == K_UP:
                 image_pos[1]-=move_speed
              elif event.key == K_DOWN:
                 image_pos[1]+=move_speed
              if event.key == K_LEFT:
                 image_pos[0]-=move_speed
              elif event.key == K_RIGHT:
                 image_pos[0]+=move_speed

              if event.key == K_i:
                 if show_info:
                    show_info=0
                 elif not show_info:
                    show_info=1

              if event.key == K_d:
                 square_width+=1
              elif event.key == K_f:
                 square_width-=1
              if event.key == K_g:
                 square_height+=1
              elif event.key == K_h:
                 square_height-=1
                 
              if event.key == K_e:
                 if scale_x<0:
                    scale_x=0
                 scale_x+=1
                 image=pygame.transform.scale(image2,(image.get_width()+scale_x,image.get_height()))
                 image_width=image.get_width()
                 image_height=image.get_height()
              elif event.key == K_r:
                 if scale_x>0:
                    scale_x=0               
                 if image.get_width()+scale_x-1>0:
                    scale_x-=1
                    image=pygame.transform.scale(image2,(image.get_width()+scale_x,image.get_height()))
                    image_width=image.get_width()
                    image_height=image.get_height()
              if event.key == K_t:
                 if scale_y<0:
                    scale_y=0
                 scale_y+=1
                 image=pygame.transform.scale(image2,(image.get_width(),image.get_height()+scale_y))
                 image_width=image.get_width()
                 image_height=image.get_height()
              elif event.key == K_y:
                 if scale_y>0:
                    scale_y=0                  
                 if image.get_height()+scale_y-1>0:
                    scale_y-=1
                    image=pygame.transform.scale(image2,(image.get_width(),image.get_height()+scale_y))
                    image_width=image.get_width()
                    image_height=image.get_height()

                 
        if image!=0:
           if event.type == MOUSEMOTION:
              square_pos[0]=event.pos[0]
              square_pos[1]=event.pos[1]
           if event.type == MOUSEBUTTONUP:
              square_color=(0,200,255)
           if event.type == MOUSEBUTTONDOWN:
              square_color=(255,200,0)

    screen.fill(BLACK)
    
    if not image:
       text=font.render(("press  L  key to load image"), True, (250,250,0))
       screen.blit(text,(130,210))
       
    if image!=0:
       screen.blit(image,image_pos)
       pygame.draw.rect(screen, square_color, [square_pos[0], square_pos[1], square_width, square_height], 4)
       
       if show_info:
          text=font.render("image width: "+str(image_width), True, (255,255,255))
          screen.blit(text,(0,420))
          text=font.render("image height: "+str(image_height), True, (255,255,255))
          screen.blit(text,(0,445))
          text=font.render("square width: "+str(square_width), True, (255,255,255))
          screen.blit(text,(250,420))
          text=font.render("square height: "+str(square_height), True, (255,255,255))
          screen.blit(text,(250,445))
          text=font.render("x: "+str(square_pos[0]), True, (255,255,255))
          screen.blit(text,(520,420))
          text=font.render("y: "+str(square_pos[1]), True, (255,255,255))
          screen.blit(text,(520,445))
    
    if screen_message:
       text=font.render(message, True, (255,255,255))
       screen.blit(text,(180,250))
 
    pygame.display.flip()
