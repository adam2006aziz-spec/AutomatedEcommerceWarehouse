# Automated Ecommerce Ware-house simulation 

## What is this?
It's a Python simulation of an automated e-commerce warehouse. The program runs a virtual robot that navigates around a grid of shelves to pick up items and complete orders. I also added a priority system, so urgent orders (like Next-Day delivery) automatically get bumped to the front of the queue.

## How it works
I split the project into three main files to keep the core logic separate from the graphics:

* `warehouse_logic.py`: This is the "brain" of the project. It holds the 10x10 grid, the inventory dictionary, and the algorithms. I used **Breadth-First Search (BFS)** so the robot can find the shortest path around the shelves without crashing, and **Bubble Sort** to organize the order queue by priority.
* `warehouse_hmi.py`: This is the control panel. It uses Tkinter to show a live dashboard of pending and completed orders. It runs the main logic in the background using threading so the UI window doesn't freeze up while the robot is "working".
* `warehouse_anim.py`: This is the visualizer. It uses Matplotlib to draw the grid and animate the robot physically moving to grab the target items and drop them off at the dispatch station.

## How to Run It

You will need Python installed, plus the `matplotlib` library for the animation script.

1. Install matplotlib (if you don't already have it):
   ```bash
   pip install matplotlib
