# warehouse_hmi.py
import tkinter as tk
import threading
import time
import random
from warehouse_logic import Warehouse, Order

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce Warehouse Dashboard")
        self.root.geometry("600x400")

        self.wh = Warehouse()
        self.running = True
        self.order_count = 101

        # Build simple UI elements
        self.status_lbl = tk.Label(root, text="System starting...", font=("Arial", 12))
        self.status_lbl.pack(pady=10)

        self.btn = tk.Button(root, text="Trigger Random Order", command=self.make_order)
        self.btn.pack(pady=5)

        self.pending_lbl = tk.Label(root, text="Pending Orders: 0")
        self.pending_lbl.pack()
        
        self.done_lbl = tk.Label(root, text="Orders Finished: 0")
        self.done_lbl.pack()

        tk.Label(root, text="Queue Log:").pack(anchor="w", padx=20)
        self.listbox = tk.Listbox(root, width=70)
        self.listbox.pack(padx=20, pady=5)

        # Start the background thread for the simulation
        self.thread = threading.Thread(target=self.run_sim)
        self.thread.start()
        self.update_ui()

    def make_order(self):
        skus = list(self.wh.inventory.keys())
        choice = random.choice(skus)
        
        prio = random.choice([1, 2, 3])
        o = Order(self.order_count, prio)
        o.item = self.wh.inventory[choice]
        
        self.wh.add_order(o)
        self.order_count += 1
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for o in self.wh.queue:
            text = "Order #" + str(o.id) + " | Priority: " + str(o.prio) + " | SKU: " + o.item.sku
            self.listbox.insert(tk.END, text)
        
        self.pending_lbl.config(text="Pending Orders: " + str(len(self.wh.queue)))
        self.done_lbl.config(text="Orders Finished: " + str(len(self.wh.done)))

    def run_sim(self):
        while self.running:
            msg = self.wh.tick()
            if msg:
                self.current_msg = msg
            time.sleep(0.4)

    def update_ui(self):
        if hasattr(self, 'current_msg'):
            self.status_lbl.config(text=self.current_msg)
            self.refresh_list()
        # Call this function again after 200ms
        self.root.after(200, self.update_ui)

    def on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()