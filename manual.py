import pygame
import random
import neat
import os

run = True


# Display
WIDTH = 1000
HEIGTH = 500

# Frames per Second
FPS = 60 

# Player 
PLAYER_WIDTH = 50
PLAYER_HEIGTH = 50
PLAYER_THROTTLE = 5

# Color:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Game():
    
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption("Dodging Game")
        self.clock = pygame.time.Clock()
        self.player = pygame.Rect(100, (HEIGTH - PLAYER_HEIGTH)/2, PLAYER_WIDTH, PLAYER_HEIGTH)
        self.obstacle = []
        self.obstacle_timer = 0
        self.score = 0
        
    def Draw(self):
        self.display.fill(BLACK) 
        pygame.draw.rect(self.display, RED, self.player)
        self.Obstacle_Spawner()
      
        pygame.display.update()

    def Obstacle_Spawner(self):
        # Obstacle
        
        if self.obstacle_timer >= 30: # Generate new obstacle every 1 second
            self.obstacle_timer = 0
            if len(self.obstacle) < 10:
                OBSTACLE_WIDTH = random.randint(10, 50)
                OBSTACLE_HEIGTH = random.randint(10, 50)
                OBSTACLE_POSITION = [WIDTH-OBSTACLE_WIDTH, random.randint(0, HEIGTH-OBSTACLE_HEIGTH)]
        
                obstacle_rect = pygame.Rect(OBSTACLE_POSITION[0], OBSTACLE_POSITION[1], OBSTACLE_WIDTH, OBSTACLE_HEIGTH)
                self.obstacle.append(obstacle_rect)
            
        else:
            self.obstacle_timer += 1
            

        for obstacle_rect in self.obstacle:
            pygame.draw.rect(self.display, WHITE, obstacle_rect)
               

    def Player_Movement(self):
          keys = pygame.key.get_pressed()
          if keys[pygame.K_UP] and self.player.y > 0:
            self.player.y -= PLAYER_THROTTLE
          if keys[pygame.K_DOWN] and self.player.y < HEIGTH - PLAYER_HEIGTH:
            self.player.y += PLAYER_THROTTLE

    def Obstacle_Movement(self):
        for obstacle_rect in self.obstacle:
            if obstacle_rect.x >= 0 and not (self.player.colliderect(obstacle_rect)):
                obstacle_rect.x -= 5
                
            elif obstacle_rect.x < 0:
                self.obstacle.pop(0)
                self.score += 1
                
    def Collision_Detection(self):
        for obstacle_rect in self.obstacle:
            if self.player.colliderect(obstacle_rect):
                print("SCORE:" + str(self.score))
                return True       
        return False

    def Reset(self):
        self.clock = pygame.time.Clock()
        self.player = pygame.Rect(100, (HEIGTH - PLAYER_HEIGTH)/2, PLAYER_WIDTH, PLAYER_HEIGTH)
        self.obstacle = []
        self.obstacle_timer = 0
        self.score = 0

    def Loop(self, run):
        
        while run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            self.Draw()
            self.Player_Movement()
            
            self.Obstacle_Movement()
            
            if self.Collision_Detection():
                self.Reset()
            
        pygame.quit()



if __name__ == "__main__":
    game = Game()
    game.Loop(run)

   