import pygame
from sys import exit
from random import choice
pygame.init()
pygame.font.init()
pygame.display.set_caption("Wordle")

screen = pygame.display.set_mode((width:=700, height:=670))
clock = pygame.time.Clock()
LETTERS = "abcdefghijklmnopqrstuvwxyz"

arial = pygame.font.SysFont("arial", 50)
arial_big = pygame.font.SysFont("arial", 125)
arial_small = pygame.font.SysFont("arial", 20)
arial_very_small = pygame.font.SysFont("arial", 13)

restart = pygame.transform.scale(pygame.image.load("restart.png").convert_alpha(), (35, 35))
home_img = pygame.transform.scale(pygame.image.load("home.png").convert_alpha(), (35, 35))

class Box:
    def __init__(self, loc):
        self.loc = loc
        self.color = [200, 200, 200]
        self.letter = ""

    def render(self):
        txt = arial.render(self.letter, False, (255, 255, 255))
        pygame.draw.rect(screen, self.color, (*self.loc, 100, 100))
        screen.blit(txt, (self.loc[0]+40, self.loc[1]+15))

def pressed(key, typed):
    if key == "enter":
        return ""
    elif key == "backspace":
        typed = typed[:-1]
        return typed
    if len(typed) > 5:
        return typed
    else:
        typed += key
    return typed

def word_check(word1: str, word2: str):
    global wrong
    rv = []
    while len(word2) < 5:
        word2 += " "
    for i in range(0, 5):
        if word1[i] == word2[i]:
            if word1.count(word2[i]) == 1:
                rv.append(2)
            elif word1.count(word2[i] == 2):
                rv.append(4)
            elif word1.count(word2[i] == 3):
                rv.append(6)
        elif word2[i] in word1:
            if word1.count(word2[i]) == 1:
                rv.append(1)
            elif word1.count(word2[i] == 2):
                rv.append(3)
            elif word1.count(word2[i] == 3):
                rv.append(5)
        else:
            rv.append(0)
            wrong.append(word2[i])
    return rv

def reset():
    global win, lose, word, columns, words_guessed, wrong
    lose = False
    win = False
    words_guessed = 0
    wrong = []
    with open("words.txt", "r") as f:
        word = choice(f.read().splitlines())
    for row in columns:
        for box in row:
            box.letter = ""
            box.color = [200, 200, 200]

with open("words.txt", "r") as f:
    word = choice(f.read().splitlines())

columns = [
    [Box([10, 10]), Box([120, 10]), Box([230, 10]), Box([340, 10]), Box([450, 10])],
    [Box([10, 120]), Box([120, 120]), Box([230, 120]), Box([340, 120]), Box([450, 120])],
    [Box([10, 230]), Box([120, 230]), Box([230, 230]), Box([340, 230]), Box([450, 230])],
    [Box([10, 340]), Box([120, 340]), Box([230, 340]), Box([340, 340]), Box([450, 340])],
    [Box([10, 450]), Box([120, 450]), Box([230, 450]), Box([340, 450]), Box([450, 450])],
    [Box([10, 560]), Box([120, 560]), Box([230, 560]), Box([340, 560]), Box([450, 560])],
]

words_guessed = 0
typed = ""
you = arial.render("You", False, (0, 0, 0))
victory = arial.render("Win!", False, (0, 0, 0))
defeat = arial.render("Lose!", False, (0, 0, 0))
dis = "home"
win = False
lose = False
wrong = []

while True:
    clock.tick(60)
    screen.fill((255, 255, 255))
    if dis == "home":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                dis = "game"

        screen.blit(arial_big.render("W", False, (128, 194, 255)), (width/2-65, 0))
        screen.blit(arial_big.render("O", False, (128, 194, 255)), (width/2-55, 100))
        screen.blit(arial_big.render("R", False, (128, 194, 255)), (width/2-50, 200))
        screen.blit(arial_big.render("D", False, (128, 194, 255)), (width/2-45, 300))
        screen.blit(arial_big.render("L", False, (128, 194, 255)), (width/2-40, 400))
        screen.blit(arial_big.render("E", False, (128, 194, 255)), (width/2-45, 500))

    elif dis == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.KEYDOWN:
                # 97 - 122
                if event.key == pygame.K_BACKSPACE:
                    typed = pressed("backspace", typed)
                elif event.key == pygame.K_SPACE:
                    typed = pressed("X", typed)
                elif event.key == pygame.K_RETURN:
                    if win or lose:
                        continue
                    if typed == word:
                        match = word_check(word, typed)
                        typed = pressed("enter", typed)
                        for index, box in enumerate(columns[words_guessed]):
                            if match[index] == 0:
                                box.color = [150, 150, 150]
                            elif match[index] == 1:
                                box.color = [255, 255, 0]
                            elif match[index] == 2:
                                box.color = [0, 255, 0]
                            elif match[index] == 3:
                                box.color = [0, 255, 255]
                            elif match[index] == 4:
                                box.color = [0, 200, 0]
                            elif match[index] == 5:
                                box.color = [0, 200, 200]
                            elif match[index] == 6:
                                box.color = [0, 100, 0]
                        win  = True
                    elif words_guessed == 5:
                        match = word_check(word, typed)
                        typed = pressed("enter", typed)
                        for index, box in enumerate(columns[words_guessed]):
                            if match[index] == 0:
                                box.color = [150, 150, 150]
                            elif match[index] == 1:
                                box.color = [255, 255, 0]
                            elif match[index] == 2:
                                box.color = [0, 255, 0]
                            elif match[index] == 3:
                                box.color = [0, 255, 255]
                            elif match[index] == 4:
                                box.color = [0, 200, 0]
                            elif match[index] == 5:
                                box.color = [0, 200, 200]
                            elif match[index] == 6:
                                box.color = [0, 100, 0]
                        lose = True
                    else:
                        match = word_check(word, typed)
                        typed = pressed("enter", typed)
                        for index, box in enumerate(columns[words_guessed]):
                            if match[index] == 0:
                                box.color = [150, 150, 150]
                            elif match[index] == 1:
                                box.color = [255, 255, 0]
                            elif match[index] == 2:
                                box.color = [0, 255, 0]
                            elif match[index] == 3:
                                box.color = [0, 255, 255]
                            elif match[index] == 4:
                                box.color = [0, 200, 0]
                            elif match[index] == 5:
                                box.color = [0, 200, 200]
                            elif match[index] == 6:
                                box.color = [0, 100, 0]
                        words_guessed += 1
                else:
                    for i in range(97, 123):
                        if event.key == i:
                            typed = pressed(LETTERS[i-97], typed)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] >= 200 and pos[1] <= 235:
                    if pos[0] >= width-125 and pos[0] <= width-90:
                        reset()
                    elif pos[0] >= width-70 and pos[0] <= width-35:
                        reset()
                        dis = "home"
        
        for row in columns:
            for box in row:
                box.render()

        if words_guessed <= 5:
            for index, box in enumerate(columns[words_guessed]):
                if box.letter == "":
                    box.color = [200, 200, 200]
                try:
                    if lose or win:
                        raise Exception("safe")
                    box.letter = typed[index]
                    if typed[index] in wrong:
                        box.color = [150, 150 ,150]
                    else:
                        box.color = [200, 200, 200]
                except IndexError:
                    box.letter = ""
                except Exception:
                    pass

        re = pygame.draw.rect(screen, (128, 0, 255), (width-125, 200, 35, 35))
        screen.blit(restart, (width-125, 200))
        home = pygame.draw.rect(screen, (128, 0, 255), (width-70, 200, 35, 35))
        screen.blit(home_img, (width-70, 200))
        pygame.draw.rect(screen, (150, 150, 150), (width-130, 275, 25, 25)), screen.blit(arial_small.render("Wrong", False, (100, 100, 100)),(width-95, 275))
        par1_box = pygame.draw.rect(screen, (255, 255, 0), (width-130, 325, 25, 25)), screen.blit(arial_small.render("Present", False, (100, 100, 100)),(width-95, 325))
        par2_box = pygame.draw.rect(screen, (255, 128, 0), (width-130, 375, 25, 25)), screen.blit(arial_very_small.render("Present Twice", False, (100, 100, 100)),(width-95, 380))
        par3_box = pygame.draw.rect(screen, (128, 64, 0), (width-130, 425, 25, 25)), screen.blit(arial_very_small.render("Present Thrice", False, (100, 100, 100)),(width-95, 430))
        com1_box = pygame.draw.rect(screen, (0, 255, 0), (width-130, 475, 25, 25)), screen.blit(arial_small.render("Correct", False, (100, 100, 100)),(width-95, 475))
        com2_box = (pygame.draw.rect(screen, (0, 200, 0), (width-130, 525, 25, 25)), 
        screen.blit(arial_very_small.render("Correct", False, (100, 100, 100)),(width-95, 520)),
        screen.blit(arial_very_small.render("Occurs Twice", False, (100, 100, 100)), (width-95, 535))
        )
        com3_box = (pygame.draw.rect(screen, (0, 100, 0), (width-130, 575, 25, 25)), 
        screen.blit(arial_very_small.render("Correct", False, (100, 100, 100)),(width-95, 570)), 
        screen.blit(arial_very_small.render("Occurs Twice", False, (100, 100, 100)), (width-95, 585))
        )

        if win:
            screen.blit(you, (width-115, 50))
            screen.blit(victory ,(width-115, 100))
        if lose:
            lose_txt=arial_small.render(f"Word was {word}", False, (0, 0, 0))
            screen.blit(you, (width-115, 50))
            screen.blit(defeat, (width-120, 100))
            screen.blit(lose_txt, (width-140, 250))

        if not(win or lose):
            screen.blit(arial.render("Guess", False, (128, 194, 255)), (width-135, 20))
            screen.blit(arial.render("The", False, (128, 194, 255)), (width-115, 70))
            screen.blit(arial.render("Word!", False, (128, 194, 255)), (width-125, 120))

    pygame.display.update()