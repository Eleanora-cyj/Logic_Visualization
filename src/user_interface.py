from src.text_box import *
from src.graph_box import *

class UI(object):
    def __init__(self):
        '''
        1. initialize the screen
        2. set the width and hight
        3. load the background image
        4. initialize all the elements
            - log textbox
            - network graphbox
        '''
        pygame.init()
        infoObject = pygame.display.Info()
        screen_width = infoObject.current_w
        screen_height = infoObject.current_h
        self.size = screen_width, screen_height
        self.version = '1.0'
        self.screen = pygame.display.set_mode(
            self.size,
            flags=pygame.FULLSCREEN
        )
        self.background = pygame.image.load('img/background.jpg')
        pygame.display.set_caption('VE450 Demo{0}'.format(self.version))

        # text box
        self.buffer = ''
        self.text_box = Text_box(self.screen)

        # graph box
        self.graph_box = Graph_box(self.screen)

    def log(self, message):
        self.text_box.insert_log(message)

    def parse_command(self, command):
        if command == 'quit':
            sys.exit()
        if command == 'exit':
            sys.exit()
        if command == 'help':
            self.text_box.print_help()
        if command.startswith('write'):
            tokens = command.split(' ')
            if len(tokens) < 2:
                return
            with open(tokens[1], 'w') as f:
                return_value = self.graph_box.write_blif(f)
            self.text_box.insert_text('write output to file {0}'.format(tokens[1]))
            if return_value == False:
                self.text_box.insert_text('network failed, please check your connections')
            else:
                with open(tokens[1], 'r') as f:
                    self.text_box.insert_file(f)
        if command.startswith('read'):
            tokens = command.split(' ')
            if len(tokens) < 2:
                return
            with open(tokens[1], 'r') as f:
                return_value = self.graph_box.read_blif(f)
            self.text_box.insert_text('read output from file {0}'.format(tokens[1]))
            if return_value == False:
                self.text_box.insert_text('network failed')
            else:
                self.text_box.insert_text('success!')

    def get_event(self):
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                sys.exit()
            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left botton
                if event.button == 1:
                    mouse_position = pygame.mouse.get_pos()
                    message = self.graph_box.on_left_down(mouse_position)
                    if message is not None:
                        self.log(message)
                # right botton
                if event.button == 3:
                    mouse_position = pygame.mouse.get_pos()
                    message = self.graph_box.on_right_down(mouse_position)
                    if message is not None:
                        self.log(message)
                # scroll up
                if event.button == 4:
                    self.graph_box.zoom_in()
                    pass
                # scroll down
                if event.button == 5:
                    self.graph_box.zoom_out()
                    pass
                return True
            # mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_position = pygame.mouse.get_pos()
                    self.graph_box.on_left_up(mouse_position)
                if event.button == 3:
                    mouse_position = pygame.mouse.get_pos()
                    self.graph_box.on_right_up(mouse_position)
                return True
            # key board
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    # parse the command
                    command = self.text_box.store_buffer()
                    self.parse_command(command)
                elif event.key == pygame.K_SPACE:
                    self.text_box.input_buffer += ' '
                elif event.key == pygame.K_BACKSPACE:
                    self.text_box.input_buffer = self.text_box.input_buffer[:-1]
                else:
                    self.text_box.input_buffer += pygame.key.name(event.key)
            return False

    def run_click(self, position):
        pass

    def paint(self):

        # background image
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.background, [0, 0])

        # textbox
        self.text_box.paint()

        # graphbox
        self.graph_box.paint()

        pygame.display.flip()

    def loop(self):
        self.graph_box.loop()

    def run(self):
        while(True):
            self.get_event()
            self.paint()
            self.loop()
            
