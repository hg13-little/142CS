import pygame
import pygwidgets
import random
import sys

pygame.init()

#window
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fishing Game")

clock = pygame.time.Clock()

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
WATER = (0,100,200)
HOOK_COLOR = (220,220,220)

#states
START, PLAYING, GAME_OVER = "start", "playing", "game_over"
gameState = START

#hook
hookX = WIDTH // 2
hookY = 100
hookSpeed = 6
hookState = "ready"

#game variables
score = 0
gameTime = 35
startTicks = 0

#ui
scoreDisplay = pygwidgets.DisplayText(window, (10, 10), "Score: 0", fontSize=30)
timeDisplay = pygwidgets.DisplayText(window, (650, 10), "Time: 35", fontSize=30)

startButton = pygwidgets.TextButton(window, (325, 250), "Start Game")
restartButton = pygwidgets.TextButton(window, (300, 250), "Restart")
quitButton = pygwidgets.TextButton(window, (300, 320), "Quit")

#classes

class Fish:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(200, HEIGHT - 50)
        self.size = random.randint(10, 40)
        self.points = max(1, min(10, self.size // 4))
        self.speed = random.choice([-2, -1, 1, 2])
        self.color = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
        self.type = "normal"

        if random.random() < 0.2:
            self.type = "slow"
            self.color = (180,180,180)

    def move(self):
        self.x += self.speed
        if self.x <= 0 or self.x >= WIDTH - self.size * 2:
            self.speed *= -1

    def draw(self):
        pygame.draw.ellipse(window, self.color,
                            (self.x, self.y, self.size*2, self.size))

        pygame.draw.polygon(window, self.color, [
            (self.x, self.y + self.size//2),
            (self.x - self.size//2, self.y),
            (self.x - self.size//2, self.y + self.size)
        ])

        pygame.draw.circle(window, BLACK,
                           (self.x + self.size*2 - 5, self.y + self.size//2), 2)

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.size*2, self.size)


class Bubble:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = HEIGHT
        self.size = random.randint(2, 5)
        self.speed = random.uniform(1, 3)

    def move(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.circle(window, (200,220,255),
                           (int(self.x), int(self.y)), self.size)



def drawGradient():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(100 * (1 - ratio))
        g = int(150 * (1 - ratio))
        b = 255
        pygame.draw.line(window, (r,g,b), (0,y), (WIDTH,y))


def drawScene():
    drawGradient()

    pygame.draw.rect(window, WATER, (0,150,WIDTH,HEIGHT))

    pygame.draw.polygon(window, (139,69,19),
                        [(280,140),(520,140),(480,170),(320,170)])

    pygame.draw.circle(window, (255,220,180), (400,100), 12)
    pygame.draw.line(window, BLACK, (400,112),(400,140),3)
    pygame.draw.line(window, BLACK, (400,120),(430,110),3)

    pygame.draw.line(window, (90,60,30), (430,110),(hookX,hookY),3)


def drawHook(x, y):
    pygame.draw.line(window, HOOK_COLOR, (x,100),(x,y),2)

    rect = pygame.Rect(x-10,y,20,20)
    pygame.draw.arc(window, HOOK_COLOR, rect, 0, 3.14, 3)

    pygame.draw.line(window, HOOK_COLOR,
                     (x+10,y+10),(x+5,y+15),2)


def resetGame():
    global hookX, hookY, hookSpeed, hookState, score, fishList, bubbles, startTicks
    hookX = WIDTH // 2
    hookY = 100
    hookSpeed = 6
    hookState = "ready"
    score = 0
    fishList = [Fish() for _ in range(15)]
    bubbles = [Bubble() for _ in range(20)]
    startTicks = pygame.time.get_ticks()



fishList = []
bubbles = []

#main loop

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if gameState == START:
            if startButton.handleEvent(event):
                gameState = PLAYING
                resetGame()

        elif gameState == GAME_OVER:
            if restartButton.handleEvent(event):
                gameState = PLAYING
                resetGame()
            if quitButton.handleEvent(event):
                pygame.quit()
                sys.exit()

        elif gameState == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and hookState == "ready":
                    hookState = "dropping"

    #start
    if gameState == START:
        window.fill(WHITE)
        title = pygwidgets.DisplayText(window, (250,150), "Fishing Game", fontSize=50)
        title.draw()
        startButton.draw()

    #gameplay
    elif gameState == PLAYING:
        drawScene()

        keys = pygame.key.get_pressed()

        #movement
        if keys[pygame.K_a]: hookX -= 5
        if keys[pygame.K_d]: hookX += 5
        if keys[pygame.K_w]: hookY -= 5
        if keys[pygame.K_s]: hookY += 5

        hookX = max(0, min(WIDTH, hookX))
        hookY = max(100, min(HEIGHT, hookY))

        #hook animation
        if hookState == "dropping":
            hookY += hookSpeed
            if hookY >= HEIGHT - 10:
                hookState = "rising"

        elif hookState == "rising":
            hookY -= hookSpeed
            hookRect = pygame.Rect(hookX-5, hookY, 10, 10)

            for fish in fishList[:]:
                if hookRect.colliderect(fish.getRect()):
                    score += fish.points

                    if fish.type == "slow":
                        hookSpeed = max(2, hookSpeed - 2)

                    fishList.remove(fish)
                    fishList.append(Fish())

            if hookY <= 100:
                hookState = "ready"
                hookSpeed = 6

        #bubbles
        for bubble in bubbles:
            bubble.move()
            bubble.draw()
            if bubble.y < 150:
                bubbles.remove(bubble)
                bubbles.append(Bubble())

        #fish
        for fish in fishList:
            fish.move()
            fish.draw()

        drawHook(hookX, hookY)

        #clock/timer
        seconds = (pygame.time.get_ticks() - startTicks) / 1000
        remainingTime = max(0, int(gameTime - seconds))

        scoreDisplay.setValue(f"Score: {score}")
        timeDisplay.setValue(f"Time: {remainingTime}")

        scoreDisplay.draw()
        timeDisplay.draw()

        if remainingTime <= 0:
            gameState = GAME_OVER

    #end
    elif gameState == GAME_OVER:
        window.fill(WHITE)
        endText = pygwidgets.DisplayText(window, (220,150),
                                         f"Game Over! Score: {score}",
                                         fontSize=40)
        endText.draw()
        restartButton.draw()
        quitButton.draw()

    pygame.display.update()
    clock.tick(60)