import pygame
import sys

from VANYA import fieldSize, ff

BLACK = (29, 51, 74)
WHITE = (255, 255, 255)
blockSize = 30
WINDOW_WIDTH = fieldSize * blockSize
WINDOW_HEIGHT = fieldSize * blockSize
def render():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)

    while True:
        drawGrid(blockSize)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def drawGrid(blockSize):
#Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)



render()