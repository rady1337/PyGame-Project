# -*- coding: utf-8 -*- 


import pygame
import sqlite3
from random import randint
from sys import path
from math import fabs
from time import sleep, time


# Переменные
x_person = 300
y = 370
score = 0
p_left = False
p_right = False
p_animcount_r = 0
p_animcount_l = 0
z_count = 0
z_kill = 0
bullets = []
zombies = []
bullet_a = [pygame.image.load('img/bullet_l.png'), pygame.image.load('img/bullet_r.png')]
p_stand = [pygame.image.load('img/Hero/s_r.png'), pygame.image.load('img/Hero/s_l.png')]
p_wr = [pygame.image.load('img/Hero/r1.png'), pygame.image.load('img/Hero/r2.png'),
        pygame.image.load('img/Hero/r3.png'), pygame.image.load('img/Hero/r4.png')]

p_wl = [pygame.image.load('img/Hero/l1.png'), pygame.image.load('img/Hero/l2.png'),
        pygame.image.load('img/Hero/l3.png'), pygame.image.load('img/Hero/l4.png')]

z_wr = [pygame.image.load('img/Zombie/r1.png'), pygame.image.load('img/Zombie/r2.png'),
        pygame.image.load('img/Zombie/r3.png'), pygame.image.load('img/Zombie/r4.png'),
        pygame.image.load('img/Zombie/r5.png')]

z_wl = [pygame.image.load('img/Zombie/l1.png'), pygame.image.load('img/Zombie/l2.png'),
        pygame.image.load('img/Zombie/l3.png'), pygame.image.load('img/Zombie/l4.png'),
        pygame.image.load('img/Zombie/l5.png')]


# Класс для управления базой данных Sqlite
class SQLManage:
    def __init__(self):
        self.db = sqlite3.connect('base.db', check_same_thread=False)
        self.cursor = self.db.cursor()
        with self.db:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS data 
            (id INTEGER PRIMARY KEY,
            score INTEGER)''')
            
    def add_score(self, score):
        with self.db:
            return self.cursor.execute(f'INSERT INTO data (score) VALUES ("{score}")').fetchall()
    
    def check_score(self, score):
        with self.db:
            scores = self.cursor.execute(f'SELECT id FROM data WHERE score = "{score}"').fetchall()
        if scores == []:
            return True
        else:
            return False
    
    def get_score(self):
        with self.db:
            return self.cursor.execute('SELECT score FROM data').fetchall()


# Окно рейтинга
def score_screen():
    pygame.mixer.music.load('music/main.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)
    menu_bg = pygame.image.load('img/menu.jpg')
    show_menu = True
    
    x = 30
    y = 160
    count = 1
    all_ = []
    best = []
    data = {}
    flag = True
    
    scores = sqliter.get_score()
    for score in scores:
        all_.append(score[0])
        
    while True:
        max_ = max(all_)
        best.append(max_)
        all_.pop(all_.index(max_))
        
        if len(best) == 10 or len(all_) == 0:
            break
    
    best.sort(reverse = True)
    
    for one in best:
        text = f'{count}) {one}'
        cords = (x, y)
        count, y = count + 1, y + 50
        data[text] = cords
        
    while show_menu:
        win.blit(menu_bg, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            menu()
        
        for one in data:
            print_text(one, data[one][0], data[one][1], (255, 255, 255), 55)
        
        pygame.display.update()
        clock.tick(60)             
        

# Титры :)            
def credits():
    pygame.mixer.music.load('music/main.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)
    menu_bg = pygame.image.load('img/menu.jpg')
    show_menu = True
    
    y1 = 10
    y2 = 100
    x_text = 400    
    
    while show_menu:
        win.blit(menu_bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            menu()
        
        print_text('CREDITS:', x_text, y1, (0, 30, 80), 100)
        print_text('ALL GAME - Ilya', x_text, y2, (0, 30, 80), 70)
        
        if y1 > 800:
            menu()
        
        y1 += 1
        y2 += 1
        
        pygame.display.update()
        clock.tick(60)        


# Меню 
def menu():
    pygame.mixer.music.load('music/main.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)
    menu_bg = pygame.image.load('img/menu.jpg')
    show_menu = True
    
    start_btn = Button(360, 70)
    score_btn = Button(360, 70)
    credit_btn = Button(360, 70)
    quit_btn = Button(360, 70)  
    
    while show_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        win.blit(menu_bg, (0, 0))
        start_btn.draw(30, 250, 'START GAME', game)
        score_btn.draw(30, 350, 'SCORES', score_screen)
        credit_btn.draw(30, 450, 'CREDITS', credits)
        quit_btn.draw(30, 550, 'EXIT', exit_game)
        
        pygame.display.update()
        clock.tick(60)


# Выход из игры
def exit_game():
    pygame.quit()
    
    
# Главная функция игры
def game():
    global x_person, y, score, p_stand, p_wr, p_wl, p_left, p_right
    global p_animcount_r, p_animcount_l, bullets, zombie, z_kill, z_count
    
    x_person = 300
    y = 370
    p_time = time()
    n_time = 0
    score = 0
    p_left = False
    p_right = False
    die = False
    p_animcount_r = 0
    p_animcount_l = 0
    z_count = 0
    z_kill = 0
    bullets = []
    zombies = []    
    
    bg = pygame.image.load('img/Background/1.jpg')
    cur_p = pygame.image.load('img/Hero/s_r.png')
    cur_p = pygame.transform.scale(cur_p, (250, 250))
    play = True
    clock = pygame.time.Clock()
    
    while play:
        one_tap = 0
        win.blit(bg, (0, 0))
        win.blit(cur_p, (x_person, y))
        
        if p_animcount_l == 3:
            p_animcount_l = 0
        if p_animcount_r == 3:
            p_animcount_r = 0
        
        score_text = 'SCORE: ' + str(score)
        print_text(score_text, 30, 20)        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                
        for zombie in zombies:
            for bullet in bullets:
                if zombie.get_x() == bullet.get_x() or fabs(zombie.get_x() - bullet.get_x()) < 20:
                    zombies.pop(zombies.index(zombie))
                    bullets.pop(bullets.index(bullet))
                    score += 1
                    z_kill += 1        

        for zombie in zombies:
            if zombie.get_x() == x_person or fabs(zombie.get_x() - x_person) < 15:
                die = True        
        
        for bullet in bullets:
            if bullet.x > 1 and bullet.x < 1279:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
        
        if z_kill == z_count:
            z_kill = 0
            z_count += 1
            for i in range(z_count):
                ff = randint(0, 1)
                if ff == 0:
                    ff = -1
                zombies.append(Zombie(ff))
        
        for zombie in zombies:
            if zombie.life:
                zombie.x += zombie.vel
            else:
                zombies.pop(zombies.index(zombie))
                       
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            menu()
        
        if keys[pygame.K_f]:
            if p_right == True or (p_right == False and p_left == False):
                f = 1
            else:
                f = -1
            if len(bullets) < 20 and str(p_time)[-2:] != str(round(time()))[-2:]:
                p_time = round(time())
                bullets.append(Bullet(x_person + 100, 470, f))
                one_tap = 1
        
        if keys[pygame.K_LEFT] and x_person > 1:
            p_right, p_left = False, True
            p_animcount_r = 0
            x_person -= 7
            cur_p = pygame.transform.scale(p_wl[p_animcount_l], (250, 250))
            p_animcount_l += 1
        elif keys[pygame.K_RIGHT] and x_person < 1100:
            p_right, p_left = True, False
            p_animcount_l = 0
            x_person += 7
            cur_p = pygame.transform.scale(p_wr[p_animcount_r], (250, 250))
            p_animcount_r += 1
        else:
            p_animcount_l, p_animcount_r = 0, 0
            if p_right == True and p_left == False:
                cur_p = pygame.transform.scale(p_stand[0], (250, 250))
            elif p_right == False and p_left == True:
                cur_p = pygame.transform.scale(p_stand[1], (250, 250))
            
        for zombie in zombies:
            zombie.draw()
        
        if die:
            if sqliter.check_score(score):
                sqliter.add_score(score)
            print_text('YOU DIED', 450, 300, (255, 255, 255), 60)
            print_text(f'SCORE: {score}', 450, 350, (255, 255, 255), 60)
            pygame.display.update()
            sleep(4)
            menu() 
        
        for bullet in bullets:
            bullet.draw()
            
        pygame.display.update()
        clock.tick(60)
            
    pygame.quit()


# Функция для вывода текста на экран
def print_text(message, x, y, f_color=(255, 255, 255), f_size=40, f_type='UniSans.ttf'):
    font_type = pygame.font.Font(f_type, f_size)
    text = font_type.render(message, True, f_color)
    win.blit(text, (x, y))
    

# Класс для объекта "Пуля"
class Bullet:
    def __init__(self, x, y, f):
        self.x = x
        self.y = y
        self.vel = 10 * f
    
    def draw(self):
        win.blit(pygame.transform.scale(bullet_a[0], (20, 20)), (self.x, self.y))
        #pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), 4)
    
    def get_x(self):
        return self.x
        

# Класс для объекта "Зомби"
class Zombie:
    def __init__(self, f):
        if f == 1:
            self.x = randint(0, 5)
        else:
            self.x = randint(1275, 1280)
        self.y = 370
        self.f = f
        self.vel = randint(1, 3) * f
        self.acount = 0
        self.life = True
    
    def draw(self):
        if self.f == 1:
            win.blit(pygame.transform.scale(z_wr[self.acount], (250, 250)), (self.x, self.y))
        else:
            win.blit(pygame.transform.scale(z_wl[self.acount], (250, 250)), (self.x, self.y))
        
        if self.acount == 4:
            self.acount = 0
        else:
            self.acount += 1
    
    def check_attack(self, x_person):
        if x_person == self.x:
            return 10
        else:
            return 0
    
    def get_x(self):
        return self.x
    
    def get_life(self):
        return self.life
    

# Класс для создания кнопок
class Button:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.i_color = (194, 160, 53)
        self.a_color = (194, 134, 53)
    
    def print_text(self, message, x, y, f_color=(0, 0, 0), f_type='UniSans.ttf', f_size=60):
        font_type = pygame.font.Font(f_type, f_size)
        text = font_type.render(message, True, f_color)
        win.blit(text, (x, y))
   
    def draw(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
                pygame.draw.rect(win, self.a_color, (x, y, self.w, self.h))
                
                if click[0] == 1:
                    if action is not None:
                        action()
        else:
            pygame.draw.rect(win, self.i_color, (x, y, self.w, self.h))
        
        self.print_text(message, x + 10, y + 10)
            

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('The Last Man on Earth')
    win = pygame.display.set_mode((1280, 700))
    
    clock = pygame.time.Clock()
    
    sqliter = SQLManage()
    
    menu()
    