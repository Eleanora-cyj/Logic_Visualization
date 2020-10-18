from src.global_definition import *

class Text_box:
    def __init__(self, screen):
        # get the window DPI and set the size of box
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.width, self.height = int(screen_width*0.9), int(screen_height*0.2)
        self.position = self.left, self.top = int(screen_width*0.05), int(screen_height*0.70)
        self.max_line = 10
        self.text_buffer = [
            '=== Textbox Initialization ===',
            '  Hi! This is {0}, ver: {1}'.format(GUI_NAME, VERSION),
            '  The demo is successfully initialized.  ',
            '  Now you can use the textbox  ',
        ]
        self.input_buffer = ''
        self.screen = screen
        self.font_size = int(self.height/self.max_line)

    def insert_user(self, string):
        # reserve 1 line for the input display
        if len(self.text_buffer) == self.max_line-1:
            self.text_buffer = self.text_buffer[1:]
        self.text_buffer.append('user> '+string)

    def insert_text(self, string):
        # reserve 1 line for the input display
        if len(self.text_buffer) == self.max_line-1:
            self.text_buffer = self.text_buffer[1:]
        self.text_buffer.append('     '+string)

    def insert_log(self, string):
        # reserve 1 line for the input display
        if len(self.text_buffer) == self.max_line-1:
            self.text_buffer = self.text_buffer[1:]
        self.text_buffer.append('  ::  '+string)

    def insert_file(self, file):
        lines = file.readlines()
        for line in lines:
            self.insert_text(line[:-1]) # get rid of \n

    def print_help(self):
        help_text = [
            '=== HELP TEXT ===',
            'Hi! This is {0}, ver: {1}, looking for help?'.format(GUI_NAME, VERSION),
            '    Mouse LeftClick: create a new node or drag an existing node.',
            '    Mouse RightClick: delete a node or drag to link two nodes'
        ]
        for text in help_text:
            self.insert_text(text)

    def store_buffer(self):
        command = self.input_buffer
        self.insert_user(self.input_buffer)
        self.input_buffer = ''
        return command

    def paint(self):
        pygame.draw.rect(self.screen, GREEN, Rect(
            self.left-10, self.top-10, self.width+20, self.height+20), 1)
        offset = 0
        line_number = 0
        # paint all the text
        font = pygame.font.SysFont('Arial', self.font_size)
        for text in self.text_buffer:
            text_rect = font.render('[{0}]  '.format(
                line_number)+text, True, GREEN, None)
            position = self.left, self.top+offset
            self.screen.blit(text_rect, position)
            offset += self.font_size
            line_number += 1
        # paint input buffer
        text_rect = font.render('>>   {0}_'.format(
            self.input_buffer), True, WHITE, None)
        position = self.left, self.top+self.height-self.font_size
        self.screen.blit(text_rect, position)
