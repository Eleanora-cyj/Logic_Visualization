from src.global_definition import *

class Node(object):
    def __init__(self, name, position, radius):
        self.name = name
        # connections: fanin, fanout
        self.fanin_left = self.fanin_right = None
        self.fanouts = []
        self.edges = []
        self.logic = []
        self.x, self.y = self.position = position
        self.radius = radius
        self.highlight = False
        self.endanger = False
        self.level = None

    def is_over(self, position):
        x, y = position
        if self.x < x-self.radius:
            return False
        if self.x > x+self.radius:
            return False
        if self.y < y-self.radius:
            return False
        if self.y > y+self.radius:
            return False
        return True

    def move_to(self, position):
        self.x, self.y = self.position = position

class Edge(object):
    def __init__(self, lower_node, higher_node, pin_index):
        self.lower_node = lower_node
        self.higher_node = higher_node
        self.pin_index = pin_index # left: 1; right: 2
        self.highlight = False
        self.endanger = False

class Graph_box:
    def __init__(self, screen):
        # get the window DPI and set the size of box
        infoObject = pygame.display.Info()
        screen_width = infoObject.current_w
        screen_height = infoObject.current_h
        self.width, self.height = int(screen_width*0.4), int(screen_height*0.6)
        self.position = self.left, self.top = int(screen_width*0.05), int(screen_height*0.05)
        self.screen = screen
        self.max_level = 10
        self.node_size = int(self.height/self.max_level)/3
        self.area = 0
        self.moving_node = None
        self.endanger_node = None
        self.model_name = 'example'
        
        # nodes 
        self.nodes = []
        # connnections
        self.connnections = []

    def paint_node(self, node):
        x, y = node.position
        # priority: red > white > gray
        if node.endanger is True:
            color = RED
        elif node.highlight is True:
            color = WHITE
        else:
            color = GRAY
        # paint input
        if node.fanin_left == None and node.fanin_right == None:
            pygame.draw.arc(self.screen, color, [x-self.node_size,y-self.node_size,self.node_size*2,self.node_size*2], 1.57*0, 1.57*2, 1)
            bot_start, bot_end = [
                (x-self.node_size,  y),
                (x+self.node_size,  y),
            ]
            pygame.draw.line(self.screen, color, bot_start, bot_end, 1)
            leg_start, leg_end = [
                (x,  y-self.node_size),
                (x,  y-self.node_size*1.5),
            ]
            pygame.draw.line(self.screen, color, leg_start, leg_end, 1)
            return

        # the and gate
        pygame.draw.arc(self.screen, color, [x-self.node_size,y-self.node_size,self.node_size*2,self.node_size*2], 1.57*0, 1.57*2, 1)
        points = [
            (x-self.node_size,  y),
            (x-self.node_size,  y+self.node_size),
            (x+self.node_size,  y+self.node_size),
            (x+self.node_size,  y)
        ]
        pygame.draw.lines(self.screen, color, False, points, 1)
        leg1_start, leg1_end = [
            (x-self.node_size/2,  y+self.node_size),
            (x-self.node_size/2,  y+self.node_size*1.5),
        ]
        leg2_start, leg2_end = [
            (x+self.node_size/2,  y+self.node_size),
            (x+self.node_size/2,  y+self.node_size*1.5),
        ]
        leg3_start, leg3_end = [
            (x,  y-self.node_size),
            (x,  y-self.node_size*1.5),
        ]
        pygame.draw.line(self.screen, color, leg1_start, leg1_end, 1)
        pygame.draw.line(self.screen, color, leg2_start, leg2_end, 1)
        pygame.draw.line(self.screen, color, leg3_start, leg3_end, 1)

    def paint_edge(self, edge):
        # figure out the position:
        lower_x, lower_y = edge.lower_node.position
        lower_node_pos = [
            lower_x,  lower_y-self.node_size*1.5,
        ]
        higher_x, higher_y = edge.higher_node.position
        if edge.pin_index == 1:
            higher_node_pos = [
                higher_x-self.node_size/2,  higher_y+self.node_size*1.5,
            ]
        elif edge.pin_index == 2:
            higher_node_pos = [
                higher_x+self.node_size/2,  higher_y+self.node_size*1.5,
            ]
        else:
            return
        # priority: red > white > gray
        if edge.endanger is True:
            color = RED
        elif edge.highlight is True:
            color = WHITE
        else:
            color = DARK_GRAY
        pygame.draw.line(self.screen, color, lower_node_pos, higher_node_pos, 1)

    def paint(self):
        # paint grid
        grid_size = int(self.height/self.max_level)
        grid_width = int(self.width/grid_size)
        grid_height = int(self.height/grid_size)
        for _ in range(grid_height+1):
            start, end = [
                (self.left, self.top+_*grid_size),
                (self.left+self.width, self.top+_*grid_size)
            ]
            pygame.draw.line(self.screen, DARK_GREEN, start, end, 1)
        for _ in range(grid_width+1):
            start, end = [
                (self.left+_*grid_size, self.top),
                (self.left+_*grid_size, self.top+self.height)
            ]
            pygame.draw.line(self.screen, DARK_GREEN, start, end, 1)
        # paint boundary
        pygame.draw.rect(self.screen, GREEN, Rect(
            self.left-10, self.top-10, self.width+20, self.height+20), 1)
        # paint nodes
        for node in self.nodes:
            self.paint_node(node)
        # paint connections
        for connection in self.connnections:
            self.paint_edge(connection)

    def zoom_in(self):
        if self.max_level == 1:
            return
        self.max_level -= 1
        self.node_size = int(self.height/self.max_level)/3
        grid_size = int(self.height/self.max_level)
        # round it to the closest grid point
        for node in self.nodes:
            x, y = node.position
            grid_position = [
                round((x-self.left)/grid_size)*grid_size+self.left,
                round((y-self.top)/grid_size)*grid_size+self.top
            ]
            node.position = grid_position

    def zoom_out(self):
        self.max_level += 1
        self.node_size = int(self.height/self.max_level)/3
        grid_size = int(self.height/self.max_level)
        # round it to the closest grid point
        for node in self.nodes:
            x, y = node.position
            grid_position = [
                round((x-self.left)/grid_size)*grid_size+self.left,
                round((y-self.top)/grid_size)*grid_size+self.top
            ]
            node.position = grid_position

    def add_node(self, position):
        node = Node(
            name = 'node{0}'.format(self.area),
            radius = self.node_size,
            position = position
        )
        self.nodes.append(node)
        self.area += 1
        return node

    def add_empty_node(self):
        node = self.add_node([0, 0])
        node.logic = None
        return node

    def delete_node(self, node):
        while len(node.edges) > 0:
            self.delete_connection(node.edges[0])
        if node in self.nodes:
            if len(node.edges) is 0:
                self.nodes.remove(node)
                self.area -= 1

    def add_connection(self, lower_node, higher_node):
        # priority: left > right
        lower_node.fanouts.append(higher_node)
        if higher_node.fanin_left == None:
            pin_index = 1
            higher_node.fanin_left = lower_node
        elif higher_node.fanin_right == None:
            pin_index = 2
            higher_node.fanin_right = lower_node
        else:
            return False
        edge = Edge(
            lower_node = lower_node,
            higher_node = higher_node,
            pin_index = pin_index
        )
        lower_node.edges.append(edge)
        higher_node.edges.append(edge)
        if edge not in self.connnections:
            self.connnections.append(edge)
        return True
    
    def delete_connection(self, edge):
        if edge in self.connnections:
            self.connnections.remove(edge)
        if edge.lower_node is not None:
            edge.lower_node.edges.remove(edge)
            edge.lower_node.fanouts.remove(edge.higher_node)
        if edge.higher_node is not None:
            edge.higher_node.edges.remove(edge)
            if edge.pin_index == 1:
                edge.higher_node.fanin_left = None
            if edge.pin_index == 2:
                edge.higher_node.fanin_right = None

    def assign_level(self, node, current_level):
        # if reached the leaf
        if node.logic is None:
            node.level = current_level
            return current_level
        return max(
            self.assign_level(node.fanin_left,  current_level+1),
            self.assign_level(node.fanin_right, current_level+1)
        )
    def assign_grid_position(self, node, current_location):
        x, y = current_location
        grid_size = int(self.height/self.max_level)
        node.position = [
            x*grid_size+self.left,
            y*grid_size+self.top
        ]
        if node.fanin_left is not None:
            self.assign_grid_position(node.fanin_left, [x-1,y+1])
        if node.fanin_left is not None:
            self.assign_grid_position(node.fanin_right, [x+1,y+1])

    def read_blif(self, file):
        # clean up all the nodes:
        self.nodes.clear()
        self.connnections.clear()
        self.moving_node = None
        self.endanger_node = None
        # first run: initialize all nodes and logic
        nodes = {}
        outputs = []
        while True:
            line = file.readline().split()
            while line[-1] == '\\':
                line.pop()
                for word in file.readline().split():
                    line.append(word)
            if line[0] == '.inputs':
                for inputs in line[1:]:
                    if inputs not in self.nodes:
                        nodes[inputs] = self.add_empty_node()
            if line[0] == '.outputs':
                for output in line[1:]:
                    outputs.append(output)
            if line[0] == '.end':
                break
            if line[0] == '#':
                continue
            if line[0] == '.model':
                self.model_name = line[1]
            if line[0] == '.names':
                left, right, output = line[1:]
                if left not in nodes:
                    nodes[left] = self.add_empty_node()
                if right not in nodes:
                    nodes[right] = self.add_empty_node()
                if output not in nodes:
                    nodes[output] = self.add_empty_node()
                # should be <0/1><0/1> 1
                nodes[output].logic = [ int(_) for _ in file.readline()[0] ]
        # second run: initialize all the connections
        file.seek(0)
        while True:
            line = file.readline().split()
            while line[-1] == '\\':
                line.pop()
                for word in file.readline().split():
                    line.append(word)
            if line[0] == '.end':
                break
            elif line[0] == '.names':
                left, right, output = line[1:]
                nodes[left].fanouts.append(nodes[output])
                nodes[right].fanouts.append(nodes[output])
                nodes[output].fanin_left  = nodes[left]
                nodes[output].fanin_right = nodes[right]
                self.add_connection(nodes[left] , nodes[output])
                self.add_connection(nodes[right], nodes[output])
                placeholder = file.readline()
            else:
                continue
        file.close()
        # zoom to be able to host all the nodes
        if len(outputs) == 1:
            root = nodes[outputs[0]]
            graph_level = self.assign_level(root, 1)
            self.max_level = max(6, graph_level+2)
            grid_size   = int(self.height/self.max_level)
            grid_width  = int(self.width/grid_size)
            grid_height = int(self.height/grid_size)
            self.assign_grid_position(root, [round(grid_width/2), 1]) # in the middle of first row
        else:
            raise NotImplementedError

    def write_blif(self, file):
        # set input and output
        inputs = []
        outputs = []
        nodes = []
        # label all inputs
        for node in self.nodes:
            if node.fanin_right == None and node.fanin_left == None:
                if len(node.fanouts) == 0:
                    return False
                inputs.append(node.name)
            elif node.fanin_left != None and node.fanin_right != None:
                nodes.append(node)
            else:
                return False
            if len(node.fanouts) == 0:
                outputs.append(node.name)
        print('.model '+self.model_name, file=file)
        print('.inputs ' + ' '.join(inputs), file=file)
        print('.outputs ' + ' '.join(outputs), file=file)
        for node in nodes:
            print('.names ' 
                + node.fanin_left.name + ' '
                + node.fanin_right.name + ' '
                + node.name, file=file)
            print('11 1', file=file)
        print('.end', file=file)
        file.close()

    def is_over(self, position):
        x, y = position
        if x < self.left:
            return False
        if x > self.left+self.width:
            return False
        if y < self.top:
            return False
        if y > self.top+self.height:
            return False
        return True

    def on_left_down(self, position):
        # do nothing if out side the boundary
        if self.is_over(position) is False:
            return None
        x, y = position
        grid_size = int(self.height/self.max_level)
        # round it to the closest grid point
        grid_position = [
            round((x-self.left)/grid_size)*grid_size+self.left,
            round((y-self.top)/grid_size)*grid_size+self.top
        ]
        # if not empty then select that node
        for node in self.nodes:
            if node.is_over(position):
                self.moving_node = node
                node.highlight = True
                return 'Left Down: {0} is selected'.format(node.name)
        # if empty then create a new one
        new_node = self.add_node(grid_position)
        return 'Left Down: {0} is added'.format(new_node.name)

    def on_left_up(self, position):
        # do nothing if already none
        if self.moving_node is None:
            return
        x, y = position
        grid_size = int(self.height/self.max_level)
        # round it to the closest grid point
        grid_position = [
            round((x-self.left)/grid_size)*grid_size+self.left,
            round((y-self.top)/grid_size)*grid_size+self.top
        ]
        self.moving_node.move_to(grid_position)
        self.moving_node.highlight = False
        self.moving_node = None

    def on_right_down(self, position):
        # do nothing if out side the boundary
        if self.is_over(position) is False:
            return None
        # if not empty then select that node
        x, y = position
        grid_size = int(self.height/self.max_level)
        # round it to the closest grid point
        grid_position = [
            round((x-self.left)/grid_size)*grid_size+self.left,
            round((y-self.top)/grid_size)*grid_size+self.top
        ]
        for node in self.nodes:
            if node.is_over(grid_position):
                node.endanger = True
                self.endanger_node = node
                return 'Right Down: {0} is endanger'.format(node.name)
    
    def on_right_up(self, position):
        # do nothing if already none
        if self.endanger_node is None:
            return
        x, y = position
        grid_size = int(self.height/self.max_level)
        # round it to the closest grid point
        grid_position = [
            round((x-self.left)/grid_size)*grid_size+self.left,
            round((y-self.top)/grid_size)*grid_size+self.top
        ]
        for node in self.nodes:
            if node.is_over(grid_position):
                # if click on the same node then delete it
                if node.endanger == True:
                    node.endanger = False
                    message = 'Right Up: {0} is deleted'.format(node.name)
                    self.delete_node(node)
                    self.endanger_node = None
                    return message
                # if not clicking on the same node then link it
                self.endanger_node.endanger = False
                self.add_connection(
                    lower_node = self.endanger_node,
                    higher_node = node
                )
        self.endanger_node.endanger = False
        self.endanger_node = None

    def loop(self):
        position = pygame.mouse.get_pos()
        x, y = position
        grid_size = int(self.height/self.max_level)
        # round it to the closest grid point
        grid_position = [
            round((x-self.left)/grid_size)*grid_size+self.left,
            round((y-self.top)/grid_size)*grid_size+self.top
        ]
        # initilize
        for node in self.nodes:
            node.highlight = False
            for _ in range(len(node.edges)):
                node.edges[_].highlight = False
        # light up if mouse is over that node
        for node in self.nodes:
            if node.is_over(grid_position):
                node.highlight = True
                for _ in range(len(node.edges)):
                    node.edges[_].highlight = True
        if self.moving_node is None:
            return
        self.moving_node.move_to(pygame.mouse.get_pos())

