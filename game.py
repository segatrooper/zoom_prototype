from python_log_indenter import IndentedLoggerAdapter
import sys, pygame, tile, pathlib, logging, datetime, rigid
class Game:
    def __init__(self, size):
        # setup logging
        if not pathlib.Path("./logging/").exists():
            pathlib.Path("./logging").mkdir()
        logging.basicConfig(filename="./logging/logger.txt", level=logging.DEBUG)
        self.log = IndentedLoggerAdapter(logging.getLogger(__name__))
        # set display
        self.log.info(f"setting screen to size={size}")
        self.size = size
        self.screen = pygame.display.set_mode(size)
        self.sample_screen = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()
        self.bgcolor = pygame.Color('blue')
        self.log.info(f"setting background color to {self.bgcolor}")
        
        # camera
        self.cam = (0,0)
        # self.desired_cam and cam are used
        self.cam_x = 0
        self.cam_v = 0.05
        self.cam_zoom = 1
        self.cam_zoom_desired = 2

        # user input
        self.user_inputs = dict()
        self.log.info(f"setting the user_inputs to {self.user_inputs}")
        self.possible_inputs = ("left", "right", "space", "/")
        for i in self.possible_inputs:
            self.user_inputs[i] = False

        # set main character sprite
        self.log.info(f"setting main character sprite")
        self.main_char = rigid.Rigid("./img/$popotawalk_sheet.png", (96, 128), (3,4), self.log, (300, 300), False)
        self.main_char.configure_tile([1], (9,10,11), (6,7,8), (0,1,2), (3,4,5), 0.10)
        self.jumps = 2

        # set statics
        # ground
        self.ground = pygame.Rect(0, size[1] / 2, size[0], size[1] / 2)
        self.statics = []

    def game_loop(self, dt):
        dt = float(dt) / 1000
        self.v = [0,0]
        self.input_handle()
        if self.user_inputs["left"]:
            self.v[0] -= 400
        if self.user_inputs["right"]:
            self.v[0] += 400
        if self.v[0] == 400:
            if self.main_char.orientation != 2:
                self.main_char.change_orientation(2)
        elif self.v[0] == -400:
            if self.main_char.orientation != 4:
                self.main_char.change_orientation(4)
        else:
            if self.main_char.orientation != 0:
                self.main_char.change_orientation(0)
        # print(self.main_char.orientation)
        self.main_char.define_physics(self.v, dt)
        rect, jump_reset = self.main_char.update_position((0, 2000), dt, self.statics, True, self.ground)
        if jump_reset:
            self.jumps = 1
            self.main_char.animate(dt)


        self.desired_cam = [ self.main_char.loc[i] + self.main_char.tile_center[i] - (self.size[i] / 2) for i in range(2)]
        self.cam = [(0.9 * self.cam[i]) + (0.1 * self.desired_cam[i]) for i in range(2)]

        # all the graphics
        self.sample_screen.fill(self.bgcolor)
        self.screen.fill(self.bgcolor)
        pygame.draw.rect(self.sample_screen, (0,255,0), self.ground.move(-1 * int(self.cam[0]), -1 * int(self.cam[1])))
        self.main_char.blitted(self.sample_screen, rect.move(-1 * int(self.cam[0]), -1 * int(self.cam[1])))


        # operating display
        self.sample_screen = pygame.transform.scale(self.sample_screen, [int(self.cam_zoom * i) for i in self.size])
        self.screen.blit(self.sample_screen, (0,0), (self.sample_screen.get_rect().centerx - (self.size[0] // 2), self.sample_screen.get_rect().centery - (self.size[1] // 2), self.size[0], self.size[1]))
        pygame.display.flip()
        self.sample_screen = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()

        # zoom feature
        if self.user_inputs["/"]:
            if self.cam_zoom < self.cam_zoom_desired:
                self.cam_x += self.cam_v
                self.cam_zoom = ((self.cam_zoom_desired - 1) * ((3 * self.cam_x * self.cam_x) - (2 * self.cam_x * self.cam_x * self.cam_x))) + 1
        else:
            if self.cam_zoom > 1:
                self.cam_x -= self.cam_v
                self.cam_zoom = ((self.cam_zoom_desired - 1) * ((3 * self.cam_x * self.cam_x) - (2 * self.cam_x * self.cam_x * self.cam_x))) + 1

    def input_handle(self):
        for event in pygame.event.get():
                    # exiting strategy
                    if event.type == pygame.QUIT: sys.exit()
                    # user keypresses
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.user_inputs["left"] = True
                        elif event.key == pygame.K_RIGHT:
                            self.user_inputs["right"] = True
                        elif event.key == pygame.K_SPACE:
                            if self.jumps > 0:
                                self.jumps -= 1
                                self.v[1] = -800
                        elif event.key == pygame.K_SLASH:
                            self.user_inputs["/"] = not self.user_inputs["/"]
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.user_inputs["left"] = False
                        elif event.key == pygame.K_RIGHT:
                            self.user_inputs["right"] = False
