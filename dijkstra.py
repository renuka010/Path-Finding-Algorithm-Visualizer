import pygame
import math
from queue import PriorityQueue

WIDTH = 1200
HEIGHT=600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Path Finding Algorithm")

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(246,16,79)
GREEN=(135,247,42)
BLUE=(20,224,245)
YELLOW=(242, 253, 76)
ORANGE=(245,178,20)
VIOLET=(187,20,245)
GREY=(148,145,148)
PINK=(248,106,177)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row=row
		self.col=col
		self.x=row*width
		self.y=col*width
		self.color=WHITE
		self.neighbors=[]
		self.width=width
		self.total_rows=total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == YELLOW

	def is_open(self):
		return self.color == ORANGE

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == RED

	def is_end(self):
		return self.color == GREEN

	def reset(self):
		self.color = WHITE

	def make_closed(self):
		self.color = YELLOW

	def make_open(self):
		self.color = ORANGE

	def make_barrier(self):
		self.color = BLACK

	def make_start(self):
		self.color = RED

	def make_end(self):
		self.color = GREEN

	def make_path(self):
		self.color = BLUE

	def draw(self, win):
		pygame.draw.rect(win, self.color,(self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors=[]
		if self.row < 100-1 and not grid[self.row+1][self.col].is_barrier():
			self.neighbors.append(grid[self.row+1][self.col])
		if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
			self.neighbors.append(grid[self.row-1][self.col])
		if self.col < 50-1 and not grid[self.row][self.col+1].is_barrier():
			self.neighbors.append(grid[self.row][self.col+1])
		if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
			self.neighbors.append(grid[self.row][self.col-1])

	def __lt__(self, other):
		return False

def h(p1,p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1-x2)+abs(y1-y2)

def make_grid(rows, cols, width):
	grid = []
	gap=12 

	
	for i in range(cols):
		grid.append([])
		for j in range(rows):
			spot = Spot(i,j,gap,cols)
			grid[i].append(spot)

	return grid

def draw_grid(win, rows, cols, width):
	gap=12
	for i in range(rows):
		pygame.draw.line(win, GREY, (0,i*gap), (width,i*gap))
		for j in range(cols):
			pygame.draw.line(win, GREY, (j*gap,0), (j*gap,width))

def draw(win, grid, rows, cols, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, cols, width)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap=12
	y, x =pos
	row=y//gap
	col=x//gap
	return row,col

def construct_path(came_from, current):
	while current in came_from:
		current=came_from[current]
		current.make_path()

def algorithm(draw, grid, start, end):
	count =0
	unvisited=PriorityQueue()
	unvisited.put((0,count,start))
	came_from ={}
	distance={spot: float("inf") for row in grid for spot in row}
	distance[start]=0

	unvisited_hash = {start}

	while not unvisited.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current=unvisited.get()[2] #popped out of pq
		unvisited_hash.remove(current)

		if current ==end:
			construct_path(came_from, end)
			start.make_start()
			draw()
			return True

		if current != start:
			current.make_closed()

		for neighbor in current.neighbors:
			temp_distance = distance[current]+1

			if temp_distance<distance[neighbor]:
				came_from[neighbor]=current
				distance[neighbor]=temp_distance
				if neighbor not in unvisited_hash:
					count+=1
					unvisited.put((distance[neighbor], count, neighbor))
					unvisited_hash.add(neighbor)
					if neighbor!=end:
						neighbor.make_open()
		draw()

	return False

def main(win, width):
	ROWS=50
	COLS=100
	grid=make_grid(ROWS,COLS,width)

	start=None
	end=None

	run=True

	while run:
		draw(win, grid, ROWS, COLS, width)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				run=False

			if pygame.mouse.get_pressed()[0]: #left mouse click
				pos=pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot= grid[row][col]

				if not start and spot!=end:
					start=spot
					start.make_start()
				elif not end and spot !=start:
					end=spot
					end.make_end()
				elif spot!=end and spot!=start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: #right mouse click
				pos=pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot= grid[row][col]
				if spot==start:
					start=None
				if spot==end:
					end=None
				spot.reset()

			if event.type==pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, COLS, width), grid, start, end)

				if event.key == pygame.K_c:
					start=None
					end=None
					grid=make_grid(ROWS,COLS,width)

	pygame.quit()

main(WIN, WIDTH)