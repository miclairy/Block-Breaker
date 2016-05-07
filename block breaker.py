import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Block(pygame.sprite.Sprite):
    '''block objects initailise'''
    
    def __init__(self, colour, width, height):        
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        
class Ball(pygame.sprite.Sprite):
    '''makes ball'''
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
    
        pygame.draw.ellipse(self.image, WHITE, [0, 0, 10, 10])     
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 300
        self.speed_x = 3
        self.speed_y = 3
        
    def move(self, blocks_hit, paddle, score):
        '''moves and handles collisions'''
        
        if self.rect.x <= 0 or self.rect.x >= 800:
            self.speed_x *= -1
        if self.rect.y <= 0:
            self.speed_y *= -1
        
        if pygame.sprite.collide_rect(self, paddle) == True:
            #self.speed_x *= -1
            self.speed_y *= -1        
        
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        
        
class Paddle(pygame.sprite.Sprite):
    '''makes paddle'''
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 7])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 385
        self.rect.y = 550
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self):
        '''makes it follow the mouse x'''
        
        mouse_postion = pygame.mouse.get_pos()
        self.rect.x = mouse_postion[0]
   
                    
class Game(object):
    ''''game at start'''
    
    def __init__(self):
        '''initializes the game'''
        self.score = 0
        caption = "Block Breaker | Score: {}".format(self.score)
        pygame.display.set_caption(caption)        
        self.game_over = False
        self.blocks = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        
        offset_y = -30
        offset_x = -40
        for sprite in range(5):
            offset_y += 30
            offset_x = 0
            for sprite in range(14):
                red = random.randrange(10, 255)
                green = random.randrange(10, 255)
                blue = random.randrange(10, 255)
                colour = (red, green, blue)        
                block = Block(colour, 40, 20)
                
                offset_x += 50
                block.rect.x = 10+offset_x
                block.rect.y = 10+offset_y
                
                self.blocks.add(block)
                self.sprites.add(block)
        self.paddle = Paddle()
        self.sprites.add(self.paddle)
        self.ball = Ball()
        self.sprites.add(self.ball)
                
    def process_events(self):
        '''processes the events and closes window if needed'''
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                return True
            if event.type == pygame.KEYDOWN and self.game_over:
                if event.key == pygame.K_y:
                    self.__init__()

        return False
    
    def logic(self, screen):
        '''updates screen with collisions'''
        blocks_hit = pygame.sprite.spritecollide(self.ball, self.blocks, True)
        if not self.game_over:
            '''move stuff'''            
            
            self.ball.move(blocks_hit, self.paddle, self.score)
            self.paddle.move()
            
        for block in blocks_hit:
            self.score += 10
            caption = "Block Breaker | Score: {}".format(self.score)
            pygame.display.set_caption(caption)
           
            if block.rect.y < self.ball.rect.y < block.rect.y + 20:
                self.ball.speed_y *= -1
            else:
                self.ball.speed_x *= -1            
            #self.ball.rect.x += self.ball.speed_x
            #self.ball.rect.y += self.ball.speed_y
            
        if len(self.blocks) == 0:
            self.game_over = True
            
        
        if self.ball.rect.y > 600:
            self.game_over = True
        
                
    def display_frame(self, screen):
        ''''display everything'''
        screen.fill(BLACK)
        
        if not self.game_over:
            self.sprites.draw(screen)
        else:
            self.sprites.draw(screen)
            if len(self.blocks) == 0:
                self.display_won(screen)
            if self.ball.rect.y > 600:
                self.display_lost(screen)
        
        pygame.display.flip()
        
    def display_won(self, screen):
        
        font = pygame.font.SysFont('Calibri', 45, True, False)
        won_text = font.render("You Won", True, WHITE)
        font_small = pygame.font.SysFont('Calibri', 30, False, False)
        play_again = font_small.render("Play again? y/n", True, WHITE)

        screen.blit(won_text, [300, 200]) 
        screen.blit(play_again, [300 , 300])
       
        score_txt = font_small.render("Score: " + str(self.score), True, WHITE)
        screen.blit(score_txt, [330, 250])   
        
        pygame.display.flip()
        
    def display_lost(self, screen):
        
        font = pygame.font.SysFont('Calibri', 45, True, False)
        lost_text = font.render("You Lost", True, WHITE)
        font_small = pygame.font.SysFont('Calibri', 30, False, False)
        play_again = font_small.render("Play again? y/n", True, WHITE)

        screen.blit(lost_text, [300, 200]) 
        screen.blit(play_again, [300 , 300])
       
        score_txt = font_small.render("Score: " + str(self.score), True, WHITE)
        screen.blit(score_txt, [330, 250])   
        
        pygame.display.flip()
        
        
        
def main():
    
    pygame.init()        
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Block Breaker")
    pygame.mouse.set_visible(False)     
    done = False       
    clock = pygame.time.Clock()
    
    game = Game()
       
    while not done:
        
        done = game.process_events()
        game.logic(screen)
        game.display_frame(screen)     
        
        clock.tick(60)
    
    pygame.quit()
    

if __name__ == "__main__":
    main()