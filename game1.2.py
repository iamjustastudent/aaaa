import pygame
import random
import time

# 初始化
pygame.init()

#定義按鍵按下                                                                   NEW
keys_pressed = {
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False,
    pygame.K_UP: False,
    pygame.K_DOWN: False
}

# 設置窗口大小和標題
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("接水果游戏")

# 定義顏色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 創建防禦器
class Defender(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([100, 30])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > size[0] - self.rect.width:
            self.rect.x = size[0] - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > size[1] - self.rect.height:
            self.rect.y = size[1] - self.rect.height

# 創建彈幕
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(2, 3)

    def update(self):
        self.rect.y += self.speed

# 創建彈幕群組
bullet_group = pygame.sprite.Group()

# 創建防禦器
defender = Defender(size[0] // 2, size[1] - 50)

# 設置分數和失敗次數
score = 0
fail_count = 0

# 設置字體
font = pygame.font.SysFont( "simhei", 30)

# 遊戲循環
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  #                       NEW
            if event.key in keys_pressed:
                keys_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in keys_pressed:
                keys_pressed[event.key] = False
            '''if event.key == pygame.K_LEFT:            
                defender.move(-10, 0)
            elif event.key == pygame.K_RIGHT:
                defender.move(10, 0)
            elif event.key == pygame.K_UP:
                defender.move(0, -10)
            elif event.key == pygame.K_DOWN:
                defender.move(0, 10)'''

    #更新防禦者的移動速度                                                         NEW
    if keys_pressed[pygame.K_LEFT]:
        defender.move(-10, 0)
    if keys_pressed[pygame.K_RIGHT]:
        defender.move(10, 0)
    '''if keys_pressed[pygame.K_UP]:
        defender.move(0, 0)
    if keys_pressed[pygame.K_DOWN]:
        defender.move(0, 0)'''

    # 創建新的彈幕
    if random.randint(1, 20) == 1:
        x = random.randint(0, size[0] - 10)
        y = 0
        bullet = Bullet(x, y)
        bullet_group.add(bullet)
        
        

    # 更新彈幕位置和檢查防禦
    for bullet in bullet_group:
        bullet.update()
        if bullet.rect.bottom >= size[1]:
            fail_count += 1
            bullet_group.remove(bullet)
        elif bullet.rect.colliderect(defender.rect):
            score += 1
            bullet_group.remove(bullet)

    # 顯示畫面
    screen.fill(WHITE)
    bullet_group.draw(screen)
    screen.blit(defender.image, defender.rect)
    score_text = font.render("SCORE : " + str(score), True, BLACK)
    fail_text = font.render("FAIL TIMES : " + str(fail_count), True, BLACK)
    screen.blit(score_text, [10, 10])
    screen.blit(fail_text, [10, 40])
    pygame.display.flip()

    # 結束遊戲
    if fail_count >= 3:
        running = False

    clock.tick(30)

pygame.quit()

