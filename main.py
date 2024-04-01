from enum import Enum
import pyxel
import json

W_SCREEN = 230
H_SCREEN = 140

CELLS_TO_CHECK = []
    
class GameAPI:
    json = ""
    def __init__(self):
        json.loads(
        """
        {
            'server': {
                'phase': 'place'
            },
            'player1': {
                'state': 'not_ready',
                'gameboard':[['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','','']]
            },
            'player2': {
                'state': 'not_ready',
                'gameboard':[['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','',''],
                            ['','','','','','','','','','']]
            }
        }
        """) 
    

class InterfaceInGame:
    def __init__(self):
        self.boats = 5
        
    def update(self):
        pass
        
    def draw(self):
        
        # 0 = x
        # 30 = y
        # 40 = w
        # 10 = h
        pyxel.rect( (0+40/2)-(40/2),
                30-(10/2),
                40,10,
                0)
        pyxel.text( (0+40/2)-(pyxel.FONT_WIDTH*len("BOATS"))/2, 30-(10/pyxel.FONT_HEIGHT), "BOATS", 7)
        

        
class Mouse:
    def draw(self): pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 1, 35, 0, 5, 5, 0)

class Button:
    def __init__(self,pos,scale,col,text=None, active=True):
        self.text = text
        self.pos = pos
        self.scale = scale
        self.col = col
        self.setCol = col[0]
        self.state = False
        self.active = active
    
    def update(self):
        if (self.active):
            self.state = self.isColliding()
            if (self.state and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)):
                self.setCol = self.col[2]
            elif (self.state):
                self.setCol = self.col[1]
            else:
                self.setCol = self.col[0]
        else:
            self.state = False
    
    def draw(self):
        if (self.active):
            pyxel.rect( self.pos[0]-(self.scale[0]/2),
                        self.pos[1]-(self.scale[1]/2),
                        self.scale[0],self.scale[1],
                        self.setCol)
            if self.text: 
                    pyxel.text( (self.pos[0])-(pyxel.FONT_WIDTH*len(self.text[0]))/2, self.pos[1]-(self.scale[1]/pyxel.FONT_HEIGHT), self.text[0], self.text[1] )
        
    def isColliding(self):
        return  (self.pos[0]-(self.scale[0]/2)) < pyxel.mouse_x + 1 and \
                (self.pos[0]-(self.scale[0]/2)) + self.scale[0] > pyxel.mouse_x and \
                (self.pos[1]-(self.scale[1]/2)) < pyxel.mouse_y + 1 and \
                (self.pos[1]-(self.scale[1]/2)) + self.scale[1] > pyxel.mouse_y

class Cell:
    def __init__(self, x, y, h, w, state=""):
        self.position = {'x':x, 'y':y}
        self.size = {'h':h, 'w':w}
        self.button = Button([self.position['x']+self.size['w']/2,self.position['y']+self.size['h']/2],
                                [self.size['w'],self.size['h']],[1,11,3])
        self.state = state
    
    def update(self):
        self.button.update()    
        if (self.button.isColliding() and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT)):
            CELLS_TO_CHECK.append(self)
            self.state = 'w' if self.state == '' else ''
    
    def draw(self):
        self.button.draw()
        destroy = False
        if self.state == '' or self.state is None: return
        if self.state[0] == 'x': 
            destroy = True
            self.state = self.state[1:]
        if self.state == 'o':
            pyxel.blt(self.position['x'], self.position['y'], 1, 12, 0, 11, 11, 6)
        elif self.state == 'w':
            pyxel.blt(self.position['x'], self.position['y'], 1, 0, 0, 11, 11, 6)
        elif self.state in ['<','n']:
            pyxel.blt(self.position['x']+1 if self.state == '<' else self.position['x'], 
                        self.position['y']+1, 1, 
                        0 if self.state=='<' else 0, 
                        12 if self.state == '<' else 23, 
                        11 if self.state == '<' else 10, 
                        10 if self.state == '<' else 11, 6)
        elif self.state in ['=','||']:
            pyxel.blt(self.position['x']-1 if self.state=='=' else self.position['x'],
                        self.position['y']+1 if self.state=='=' else self.position['y']-1, 1, 
                        11 if self.state=='=' else 0, 
                        12 if self.state=='=' else 35,
                        13 if self.state=='=' else 10,
                        10 if self.state=='=' else 13 , 6)
        elif self.state in ['>','u']:
            pyxel.blt(self.position['x']-1 if self.state=='>' else self.position['x'],
                        self.position['y']+1 if self.state=='>' else self.position['y']-1,1,
                        24 if self.state=='>' else 0,
                        12 if self.state=='>' else 48,
                        10 if self.state=='>' else 10,
                        10 if self.state=='>' else 10, 6)
        if destroy:
            self.state = 'x'+self.state
            pyxel.blt(self.position['x'], self.position['y'], 1, 24, 0, 11, 11, 6)
            
    def part_of_terrain(self):
        return self.state == 'o' or (len(self.state)>0 and self.state[0] == 'x')
    
    def part_of_boat(self):
        return self.vertical_part_of_boat() or self.horizontal_part_of_boat()    
    
    def horizontal_part_of_boat(self):
        return self.state in ['<','>','=','w',
                              'x<','x>','x=','xw']
    
    def vertical_part_of_boat(self):
        return self.state in ['n','u','||','w'
                              'xn','xu','x||','xw']

class GameBoard:
    def __init__(self, gameboard) -> None:
        self.gameboard = gameboard; self.cells = []; self.planes = []
        self.init_cells()
        
    def update(self):
        [plane.update() for plane in self.planes]
        self.cell_logic_set_parts()
                            
    def cell_logic_set_parts(self):
        [[cell.update() for cell in cells] for cells in self.cells]
        
        if len(CELLS_TO_CHECK)>0:
            [self.reset_around_cells(irow, icol) for cell in CELLS_TO_CHECK for irow, cell_row in enumerate(self.cells) for icol, cell in enumerate(cell_row) if cell == self.cells[irow][icol]]
            
            # [self.planes.append(Plane(cell)) if not cell.part_of_terrain() else None for cell in CELLS_TO_CHECK]
            
            CELLS_TO_CHECK.clear()
            
        for irow, cell_row in enumerate(self.cells):
            for icol, cell in enumerate(cell_row):
                if cell.state == 'w':
                    self.set_cell_state(cell, irow, icol)
                    
    def search_cell_around(self, irow, icol):
        find_cells = False
        for row in [-1,0,1]:
            for col in [-1,0,1]:
                if row == 0 and col == 0: continue
                if row in [-1,1] and col in [-1,1]: continue
                if irow+row < 0 or irow+row >= len(self.cells) or icol+col < 0 or icol+col >= len(self.cells[0]): continue
                if self.cells[irow+row][icol+col].part_of_boat():
                    find_cells = True
        return find_cells        
                            
    def set_cell_state(self, cell:Cell, irow, icol):
        if not self.search_cell_around(irow, icol): cell.state = 'w'; return
        
        if icol-1 < 0 or icol+1 >= len(self.cells[0]): 
            if icol-1 > 0 and self.cells[irow][icol-1].horizontal_part_of_boat(): cell.state = '>'; return
            if icol+1 < len(self.cells[0]) and self.cells[irow][icol+1].horizontal_part_of_boat(): cell.state = '<'; return
            
            if irow-1 >= 0 and irow+1 < len(self.cells): 
                if self.cells[irow+1][icol].vertical_part_of_boat() or self.cells[irow-1][icol].vertical_part_of_boat():
                    if self.cells[irow+1][icol].vertical_part_of_boat() and self.cells[irow-1][icol].vertical_part_of_boat(): 
                        self.set_cell_state(self.cells[irow+1][icol],irow+1,icol)
                        if self.cells[irow+1][icol].vertical_part_of_boat() and self.cells[irow-1][icol].vertical_part_of_boat(): cell.state = '||'; return
                    if self.cells[irow+1][icol].vertical_part_of_boat() and not self.cells[irow-1][icol].vertical_part_of_boat(): 
                        self.set_cell_state(self.cells[irow+1][icol],irow+1,icol)
                        if self.cells[irow+1][icol].vertical_part_of_boat(): cell.state = 'n'; return
                    if self.cells[irow-1][icol].vertical_part_of_boat() and not self.cells[irow+1][icol].vertical_part_of_boat():
                        if self.cells[irow-1][icol].vertical_part_of_boat(): cell.state = 'u'; return
            if cell.state != 'w': return
        
        if irow-1 < 0 or irow+1 >= len(self.cells):
            if irow-1 < 0: 
                cell.state = 'n' if self.cells[irow+1][icol].vertical_part_of_boat() else 'w'
            else: 
                cell.state = 'u' if self.cells[irow-1][icol].vertical_part_of_boat() else 'w'
            if icol-1 > 0 and icol+1 < len(self.cells[0]): 
                if self.cells[irow][icol+1].horizontal_part_of_boat() or self.cells[irow][icol-1].horizontal_part_of_boat():
                    if self.cells[irow][icol+1].horizontal_part_of_boat() and self.cells[irow][icol-1].horizontal_part_of_boat(): cell.state = '='; return
                    if self.cells[irow][icol+1].horizontal_part_of_boat() and not self.cells[irow][icol-1].horizontal_part_of_boat(): cell.state = '<'; return
                    if self.cells[irow][icol-1].horizontal_part_of_boat() and not self.cells[irow][icol+1].horizontal_part_of_boat(): cell.state = '>'; return
            if cell.state != 'w': return
        
        if icol-1 >= 0 and icol+1 < len(self.cells[0]): 
            if self.cells[irow][icol+1].horizontal_part_of_boat() or self.cells[irow][icol-1].horizontal_part_of_boat():
                if self.cells[irow][icol+1].horizontal_part_of_boat() and self.cells[irow][icol-1].horizontal_part_of_boat(): cell.state = '='; return
                if self.cells[irow][icol+1].horizontal_part_of_boat() and not self.cells[irow][icol-1].horizontal_part_of_boat(): cell.state = '<'; return
                if self.cells[irow][icol-1].horizontal_part_of_boat() and not self.cells[irow][icol+1].horizontal_part_of_boat(): cell.state = '>'; return
            
        if irow-1 >= 0 and irow+1 < len(self.cells): 
            if self.cells[irow+1][icol].vertical_part_of_boat() or self.cells[irow-1][icol].vertical_part_of_boat():
                if self.cells[irow+1][icol].vertical_part_of_boat() and self.cells[irow-1][icol].vertical_part_of_boat(): 
                    self.set_cell_state(self.cells[irow+1][icol],irow+1,icol)
                    if self.cells[irow+1][icol].vertical_part_of_boat() and self.cells[irow-1][icol].vertical_part_of_boat(): cell.state = '||'; return
                if self.cells[irow+1][icol].vertical_part_of_boat() and not self.cells[irow-1][icol].vertical_part_of_boat(): 
                    self.set_cell_state(self.cells[irow+1][icol],irow+1,icol)
                    if self.cells[irow+1][icol].vertical_part_of_boat(): cell.state = 'n'; return
                if self.cells[irow-1][icol].vertical_part_of_boat() and not self.cells[irow+1][icol].vertical_part_of_boat():
                    if self.cells[irow-1][icol].vertical_part_of_boat(): cell.state = 'u'; return
        
    def reset_around_cells(self, irow, icol):
        for row in [-1,0,1]:
            for col in [-1,0,1]:
                if row == 0 and col == 0: continue
                if row in [-1,1] and col in [-1,1]: continue
                if irow+row < 0 or irow+row >= len(self.cells) or icol+col < 0 or icol+col >= len(self.cells[0]): continue
                if self.cells[irow+row][icol+col].part_of_boat(): self.cells[irow+row][icol+col].state = 'w'
    
    def draw(self):
        self.draw_grid()
        [[cell.draw() for cell in cells] for cells in self.cells]
        [plane.draw() for plane in self.planes]
        
    def draw_grid(self):
        x_range = {'x1':self.cells[0][0].position['x'],'x2':self.cells[-1][-1].position['x']+self.cells[0][0].size['w']-1}
        y_range = {'y1':self.cells[0][0].position['y'],'y2':self.cells[-1][-1].position['y']+self.cells[0][0].size['h']-1}
        for cells_x in [cell.position['x']-1 for cell in self.cells[0][1:]]:
            pyxel.line(cells_x,y_range['y1'],cells_x,y_range['y2'],8)
        for cells_y in [cell[0].position['y']-1 for cell in self.cells[1:]]:
            pyxel.line(x_range['x1'],cells_y,x_range['x2'],cells_y,8)
        pyxel.rectb(x_range['x1']-1,y_range['y1']-1,x_range['x2']-x_range['x1']+3,y_range['y2']-y_range['y1']+3,8)
        
    def init_cells(self):
        w_cell = (W_SCREEN-30)/len(self.gameboard[0])
        h_cell = (H_SCREEN-30)/len(self.gameboard)
        h_cell = w_cell if w_cell < h_cell else h_cell
        w_cell = h_cell if h_cell < w_cell else w_cell
        padding_x = max(0,((W_SCREEN-w_cell*len(self.gameboard[0]))/2)-5)
        padding_y = max(0,((H_SCREEN-h_cell*len(self.gameboard))/2)-5)
        for iy, y in enumerate([j*h_cell for j in range(len(self.gameboard))]):
            self.cells.append([Cell(x+padding_x+(1*ix),y+padding_y+(1*iy),h_cell,w_cell,self.gameboard[iy][ix]) 
                for ix, x in enumerate([j*w_cell for j in range(len(self.gameboard[0]))])])

class Plane:
    def __init__(self, cell:Cell):
        self.cell = cell
        self.position = {'x': 0, 'y': cell.position['y']-cell.size['h']/2} 
    def update(self):
        self.position['x'] += 1
        if self.position['x']+13 == self.cell.position['x']: self.cell.state = 'x'+self.cell.state if self.cell.part_of_boat() else 'o'
    def attack(self):
        pass
    def draw(self):
        pyxel.blt(self.position['x'], self.position['y'], 1, 0, 59, 26, 22, 6)

class App:
    def __init__(self, player):
        pyxel.init(W_SCREEN, H_SCREEN, title=f"Sea Battles | Player #{player}")
        pyxel.load("./sea.pyxres")
        self.mouse = Mouse()
        pyxel.colors[1] = 0x259CD7
        pyxel.colors[3] = 0x175E96
        pyxel.colors[8] = 0xBAD7EC
        pyxel.colors[11] = 0x67a7d6
        pyxel.colors[12] = 0x780717
        pyxel.colors[14] = 0xD95666
        # pyxel.colors[13] = 0xcfdcfc
        # pyxel.colors[2] = 0x1C75BD
        self.player = player
        self.gameboard = GameBoard([["" for _ in range(10)] for _ in range(10)])
        self.interface_in_game = InterfaceInGame()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.gameboard.update()

    def draw(self):
        pyxel.cls(1)
        self.gameboard.draw()
        self.mouse.draw()
        self.interface_in_game.draw()
App(player=1)
