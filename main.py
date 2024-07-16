import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

WIDTH=1000
HEIGHT=500
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fantasy Fight")
clock=pygame.time.Clock()

countdown=3
fight="FIGHT"
last_count=pygame.time.get_ticks()
round_over=False
ROUND_OVER_COOLDOWN=5000

counter_font=pygame.font.Font("fighting game/assests/fonts/FighterFish/FighterFish.otf",150)
player_font=pygame.font.Font("fighting game/assests/fonts/FighterFish/FighterFish.otf",30)

HERO_SIZE=200
HERO_SCALE=2.3
HERO_OFFSET=[100,100]
HERO_DATA=[HERO_SIZE,HERO_SCALE,HERO_OFFSET]
WIZARD_SIZE=250
WIZARD_SCALE=2.2
WIZARD_OFFSET=[125,143]
WIZARD_DATA=[WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]

pygame.mixer.music.load("fighting game/assests/music/Heavy Violence.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-5,0.0,10000)

sword_fx=pygame.mixer.Sound("fighting game/assests/fx/sword.wav")
sword_fx.set_volume(0.5)
magic_fx=pygame.mixer.Sound("fighting game/assests/fx/magic.wav")
magic_fx.set_volume(0.9)
fight_fx=pygame.mixer.Sound("fighting game/assests/fx/Fight.mp3")
fight_fx.set_volume(1.0)
knockout_fx=pygame.mixer.Sound("fighting game/assests/fx/K.O.mp3")
knockout_fx.set_volume(1.0)

background=pygame.image.load("fighting game/assests/images/background/background.gif").convert_alpha()


hero_sheet=pygame.image.load("fighting game/assests/images/icons/Fighters/Martial Hero/Sprites/herospritesheet2.png").convert_alpha()
wizard_sheet=pygame.image.load("fighting game/assests/images/icons/Fighters/wizard/Sprites/wizard.png").convert_alpha()

HERO_ANIMATION_STEPS=[8,8,2,6,6,4,6]
WIZARD_ANIMATION_STEPS=[8,8,2,8,8,3,7]


def draw_background():
    scaled=pygame.transform.scale(background,(WIDTH,HEIGHT))
    screen.blit(scaled,(0,0))

def draw_healthbar(health,x,y):
    ratio=health/100
    pygame.draw.rect(screen,"White",(x-2,y-2,404,34))
    pygame.draw.rect(screen,"Black",(x,y,400,30))
    pygame.draw.rect(screen,"Red",(x,y,ratio*400,30))

def draw_text(text,font,color,x,y):
    img=font.render(text,True,color)
    screen.blit(img,(x,y))




fighter_1=Fighter(1,250,350,False,HERO_DATA,hero_sheet,HERO_ANIMATION_STEPS,sword_fx)
fighter_2=Fighter(2,650,350,True,WIZARD_DATA,wizard_sheet,WIZARD_ANIMATION_STEPS,magic_fx)
   

run=True
while run:
    draw_background()

    draw_healthbar(fighter_1.health,20,20)
    draw_healthbar(fighter_2.health,520,20)
    draw_text("P1",player_font,"Gold",20,55)
    draw_text("P2",player_font,"Gold",890,55)

    clock.tick(60)
    if countdown<0:
        fighter_1.movement(WIDTH,HEIGHT,screen,fighter_2,round_over)
        fighter_2.movement(WIDTH,HEIGHT,screen,fighter_1,round_over)
    elif countdown==0:
        draw_text(fight,counter_font,"Gold",WIDTH/3,HEIGHT/3)
        if (pygame.time.get_ticks()-last_count)>500:
            countdown-=1
            last_count=pygame.time.get_ticks()     
    else:
        draw_text(str(countdown),counter_font,"Gold",WIDTH/2.2,HEIGHT/3)
        if (pygame.time.get_ticks()-last_count)>1000:
            if countdown==1:
                fight_fx.play()    
            countdown-=1
            last_count=pygame.time.get_ticks() 
       
        
    fighter_1.update()
    fighter_2.update()
  
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    if round_over==False:
        if fighter_1.alive==False:
            round_over=True
            knockout_fx.play()
            round_over_time=pygame.time.get_ticks()
        elif fighter_2.alive==False:
            round_over=True
            knockout_fx.play()
            round_over_time=pygame.time.get_ticks()
    else:
        if  round_over==True and fighter_1.health<=0:
                draw_text("P2 WINS",counter_font,"Gold",WIDTH/4,HEIGHT/3)  
        elif round_over==True and fighter_2.health<=0:
                draw_text("P1 WINS",counter_font,"Gold",WIDTH/4,HEIGHT/3)  
        if pygame.time.get_ticks()-round_over_time >ROUND_OVER_COOLDOWN:
            round_over=False
            countdown=4 
            fighter_1=Fighter(1,250,350,False,HERO_DATA,hero_sheet,HERO_ANIMATION_STEPS,sword_fx)
            fighter_2=Fighter(2,650,350,True,WIZARD_DATA,wizard_sheet,WIZARD_ANIMATION_STEPS,magic_fx)      



    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    pygame.display.update()
pygame.quit()

