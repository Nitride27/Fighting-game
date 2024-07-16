import pygame

class Fighter():
    def __init__(self,player, x, y, flip, data, sprite_sheet, animation_steps,sound):
        self.player=player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 70, 100))
        self.vel_y = 0
        self.run = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit=False
        self.health = 100
        self.alive=True

    def load_images(self,sprite_sheet,animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img = pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale))
                temp_list.append(temp_img)
            animation_list.append(temp_list)
        return animation_list

    def movement(self,swidth,sheight,surface,target,round_over):
        SPEED=5
        dx=0
        dy=0
        GRAVITY=2
        self.run=False
        self.attack_type=0

        key = pygame.key.get_pressed()
        if  self.attacking==False and self.alive==True and round_over==False:
            if self.player==1:
                if key[pygame.K_a]:
                    dx=-SPEED
                    self.run=True
                    self.flip=True

                if key[pygame.K_d]:
                    dx=SPEED
                    self.run=True
                    self.flip=False

                if key[pygame.K_w] and self.jump==False:
                    self.jump=True
                    self.vel_y=-32

                if key[pygame.K_f] or key[pygame.K_g]:
                    if self.attack_cooldown==0:
                        if key[pygame.K_f]:
                            self.attack_type=1
                        if key[pygame.K_g]:
                            self.attack_type=2
                        self.attack(surface,target)

            if self.player==2:
                if key[pygame.K_LEFT]:
                    dx=-SPEED
                    self.run=True
                    self.flip=True

                if key[pygame.K_RIGHT]:
                    dx=SPEED
                    self.run=True
                    self.flip=False

                if key[pygame.K_UP] and self.jump==False:
                    self.jump=True
                    self.vel_y=-32

                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    if self.attack_cooldown==0:
                        if key[pygame.K_KP1]:
                            self.attack_type=1
                        if key[pygame.K_KP2]:
                            self.attack_type=2
                        self.attack(surface,target)            


        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx=-self.rect.left

        if self.rect.right + dx > swidth:
            dx=swidth - self.rect.right

        if self.rect.bottom + dy > sheight - 50:
            self.jump=False
            self.vel_y=0
            dy=sheight - 50 - self.rect.bottom

        if self.attack_cooldown >0:
            self.attack_cooldown -= 1

        self.rect.x += dx
        self.rect.y += dy


    def update(self):
        if self.health<=0:
            self.health=0
            self.alive=False
            self.update_action(6)
        elif self.hit==True:
           self.update_action(5)
        elif self.attacking==True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump==True:
            self.update_action(2)
        elif self.run==True:
            self.update_action(1)
        else:
            self.update_action(0)
        
        animation_time=60
        self.image=self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_time:
            self.frame_index += 1
            self.update_time=pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive==False:
                self.frame_index=len(self.animation_list[self.action]) - 1
            else:
                self.frame_index=0
                if self.action==3 or self.action==4:
                    self.attacking=False
                    self.attack_cooldown=10
                if self.action==5:
                    self.hit=False
                    self.attacking=False
                    self.attack_cooldown=10    

     

    def attack(self,surface,target):
        if self.attack_cooldown==0:
            self.attacking=True
            self.attack_sound.play()
            attack_rect=pygame.Rect(self.rect.centerx - (2* self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attack_rect.colliderect(target.rect):
                target.hit=True
                if self.attack_type==1:
                    target.health -= 3
                elif self.attack_type==2:
                    target.health-=8   

           
        
     

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

      

    def draw(self,surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.centerx - (self.offset[0] * self.image_scale), self.rect.centery - (self.offset[1] * self.image_scale)))

       
