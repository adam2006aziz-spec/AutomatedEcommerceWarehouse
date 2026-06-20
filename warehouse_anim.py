# warehouse_anim.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from warehouse_logic import Warehouse, Order

wh = Warehouse()

# Load up a few dummy orders to start the animation
skus = list(wh.inventory.keys())
for i in range(4):
    o = Order(200 + i, random.choice([1, 2, 3]))
    o.item = wh.inventory[random.choice(skus)]
    wh.add_order(o)

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_title("Warehouse Robot Tracker")

# Draw the map
for r in range(10):
    for c in range(10):
        if wh.grid[r][c] == 1:
            ax.plot(c, r, 's', color='black', markersize=18)
        elif wh.grid[r][c] == 2:
            ax.plot(c, r, 'D', color='green', markersize=14)

robot_dot, = ax.plot([], [], 'o', color='blue', markersize=10, label="Robot")
target_dot, = ax.plot([], [], '*', color='orange', markersize=15, label="Target Item")
text_box = ax.text(4.5, -1.2, "", ha='center', fontsize=10)

ax.set_xlim(-1, 10)
ax.set_ylim(-2, 10)
ax.invert_yaxis()
ax.grid(True, linestyle='--')
ax.legend(loc="upper right")

def update_frame(frame):
    msg = wh.tick()
    
    # Update robot position
    robot_dot.set_data([wh.ry], [wh.rx])

    # Show the current target on the grid
    if wh.current_order is not None:
        tr = wh.current_order.item.row
        tc = wh.current_order.item.col
        target_dot.set_data([tc], [tr])
    else:
        target_dot.set_data([], [])

    if msg:
        text_box.set_text(msg)

    # Randomly inject new orders over time
    if frame % 25 == 0 and frame > 0:
        o = Order(frame, 1) # High priority
        o.item = wh.inventory[random.choice(skus)]
        wh.add_order(o)

    return robot_dot, target_dot, text_box

ani = animation.FuncAnimation(fig, update_frame, frames=100, interval=400, blit=False)
plt.show()