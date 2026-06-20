# warehouse_logic.py
import random

class Item:
    def __init__(self, sku, name, r, c):
        self.sku = sku
        self.name = name
        self.row = r
        self.col = c

class Order:
    def __init__(self, order_id, prio):
        self.id = order_id
        self.prio = prio # 1 is Next Day, 3 is Standard
        self.item = None # Just one item per order to keep it simple

class Warehouse:
    def __init__(self):
        # 10x10 grid. 0=floor, 1=shelf, 2=dispatch
        self.grid = [[0]*10 for i in range(10)]
        self.dispatch = (0, 5)
        self.grid[0][5] = 2

        # Setup the shelves
        for r in range(2, 9, 3):
            for c in range(1, 9):
                self.grid[r][c] = 1

        self.inventory = {}
        self.queue = []
        self.done = []
        self.load_items()

        # Robot variables
        self.rx = 0 # row
        self.ry = 0 # col
        self.state = "idle"
        self.path = []
        self.current_order = None

    def load_items(self):
        # Setting up e-commerce inventory
        data = [
            ("CUR-BLK", "Blackout Curtains", 2, 2),
            ("BED-Q", "Queen Bedding Set", 2, 6),
            ("ROD-STL", "Steel Curtain Rod", 5, 3),
            ("DEC-PIL", "Throw Pillow", 5, 7),
            ("RUG-8X10", "Living Room Rug", 8, 4)
        ]
        for d in data:
            self.inventory[d[0]] = Item(d[0], d[1], d[2], d[3])

    def add_order(self, order):
        self.queue.append(order)
        self.sort_orders()

    def sort_orders(self):
        # Basic bubble sort by priority
        n = len(self.queue)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.queue[j].prio > self.queue[j+1].prio:
                    self.queue[j], self.queue[j+1] = self.queue[j+1], self.queue[j]

    def get_path(self, start, target):
        # Breadth First Search for routing
        q = [(start, [start])]
        visited = [start]

        while len(q) > 0:
            curr, path = q.pop(0)
            if curr == target:
                return path
            
            r, c = curr
            moves = [(-1,0), (1,0), (0,-1), (0,1)] # up, down, left, right
            for m in moves:
                nr = r + m[0]
                nc = c + m[1]

                # Ensure it stays inside the grid bounds
                if 0 <= nr < 10 and 0 <= nc < 10:
                    # Can move onto floor OR the target shelf
                    if self.grid[nr][nc] != 1 or (nr, nc) == target:
                        if (nr, nc) not in visited:
                            visited.append((nr, nc))
                            new_path = list(path)
                            new_path.append((nr, nc))
                            q.append(((nr, nc), new_path))
        return []

    def tick(self):
        # Moves the robot one step and returns a status message
        if self.state == "idle":
            if len(self.queue) > 0:
                self.current_order = self.queue.pop(0)
                target = (self.current_order.item.row, self.current_order.item.col)
                self.path = self.get_path((self.rx, self.ry), target)
                self.state = "moving"
                return "Processing Order #" + str(self.current_order.id)
            return "Waiting for orders..."
        
        elif self.state == "moving":
            if len(self.path) > 0:
                next_step = self.path.pop(0)
                self.rx, self.ry = next_step
                return "Moving to " + str(self.current_order.item.sku)
            else:
                self.path = self.get_path((self.rx, self.ry), self.dispatch)
                self.state = "returning"
                return "Item grabbed! Returning to dispatch."

        elif self.state == "returning":
            if len(self.path) > 0:
                next_step = self.path.pop(0)
                self.rx, self.ry = next_step
                return "Returning to dispatch..."
            else:
                self.done.append(self.current_order)
                msg = "Order #" + str(self.current_order.id) + " completed."
                self.current_order = None
                self.state = "idle"
                return msg
