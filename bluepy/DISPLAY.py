import pygame
import threading



class DisplayArrow:
    def __init__(self, arrow_display, wait):

        self.arrow_display=arrow_display
        self.wait=wait

    def Go(self):
        pygame.init()

        display_width = 800
        display_height = 600

        # color are rgb
        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)

        gameDisplay = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption('A  bit Racey')
        clock = pygame.time.Clock()  # specific game clock

        print("porco cane")
        while True:

            if not self.arrow_display.empty():

                arrow = self.arrow_display.get()

                print(str(arrow))
                direction = arrow["direction"]
                color = arrow["color"]

                print("\n")
                print("dir_q.get " + direction)
                print("ARROW->ppp3")
                print("\n")
                directory = "arrow/Tot/"
                arrowImg = pygame.image.load(directory + color + "_" + direction + ".png")  # loading of the image, that have to be in the same directory of the script, or we have to put the path
                if direction == "sx":

                    x = (850)
                    y = (100)
                elif direction == "dx":

                    x = (-750)
                    y = (100)
                elif direction == "up":
                    x = (200)
                    y = (450)
                elif direction == "back":
                    x = (200)
                    y = (-650)

                # let's decide the quit command

                x_change = 0
                y_change = 0

                crashed = False  # I suppose that I don't have chrash

                # infinite loop until I don't have a crash
                while not crashed:

                    # create a list of events that are going to happen
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            crashed = True  # break the loop
                        # print(event)  # to see all the event that are happening

                    if direction == "sx":
                        x_change = -5
                        x += x_change

                    elif direction == "dx":
                        x_change = 5
                        x += x_change


                    elif direction == "up":
                        y_change = -5
                        y += y_change

                    elif direction == "back":
                        y_change = 5
                        y += x_change

                    gameDisplay.fill(black)  # I fill the display whithe and then I put the arrow, not the contrary
                    gameDisplay.blit(arrowImg, (x, y))
                    # arrow(x,y)

                    if x >= 1050 and direction == "dx":
                        x = 0
                        crashed = True

                    elif x <= -400 and direction == "sx":
                        x = 800

                        crashed = True

                    elif y <= -400 and direction == "up":
                        y = 400

                        crashed = True

                    elif y >= 800 and direction == "back":
                        y = 0

                        crashed = True

                    pygame.display.update()  # or pygame.display.flip(), always update the entire surface
                    # ygame.display.update()---> if you put the parameter you just update one object, instead if you don't put anything you'll update all the window

                    # move the frame on, we need to define how fast we do this, frame per second

                    clock.tick(130)  # the number that you put is frame per second (bigger the number, faster the program is)
                print("-------------------WAIT GO ----------------------")
                self.wait.put("go")



