import tkinter as tk
from tkinter import ttk
import math
from dna_digestion import digest_dna, viral_genome, restriction_enzymes

class ElectrophoresisGel:
    def __init__(self, root):
        self.root = root
        self.root.title("DNA Electrophoresis Simulation")
        
        # Constants for gel visualization
        self.GEL_WIDTH = 400
        self.GEL_HEIGHT = 500
        self.LANE_WIDTH = 60
        self.WELL_HEIGHT = 30
        
        # Create canvas for gel visualization
        self.canvas = tk.Canvas(root, width=self.GEL_WIDTH, height=self.GEL_HEIGHT, bg='lightgray')
        self.canvas.pack(pady=10)
        
        # Control panel
        self.control_frame = ttk.Frame(root)
        self.control_frame.pack(pady=10)
        
        # Run button
        self.run_button = ttk.Button(self.control_frame, text="Run Gel", command=self.run_simulation)
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        self.reset_button = ttk.Button(self.control_frame, text="Reset", command=self.reset_simulation)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Get DNA fragments from digestion
        self.fragments = digest_dna(viral_genome, restriction_enzymes)
        
        # Initialize gel
        self.draw_gel()
        
    def draw_gel(self):
        """Draw the basic gel structure with wells"""
        # Draw gel outline
        self.canvas.create_rectangle(50, 0, self.GEL_WIDTH-50, self.GEL_HEIGHT, 
                                   fill='#agarose', outline='black')
        
        # Draw wells
        for i in range(2):  # 2 lanes - one for fragments, one for ladder
            x = 100 + (i * self.LANE_WIDTH)
            self.canvas.create_rectangle(x, 10, x + 40, self.WELL_HEIGHT,
                                       fill='black')
            
    def calculate_migration_distance(self, fragment_length):
        """Calculate migration distance based on fragment length"""
        # Inverse relationship between length and distance
        # Shorter fragments travel further (less friction)
        base_distance = self.GEL_HEIGHT - 100
        # Using natural log to create non-linear relationship
        migration = base_distance * (1 - (math.log(fragment_length) / math.log(max(len(f[0]) for f in self.fragments))))
        return min(max(migration, 50), self.GEL_HEIGHT - 50)
    
    def run_simulation(self):
        """Simulate DNA fragment migration"""
        # DNA ladder for size reference (in base pairs)
        ladder = [10000, 8000, 6000, 4000, 2000, 1000, 500, 200]
        
        # Draw ladder in first lane
        x = 100
        for size in ladder:
            y = self.calculate_migration_distance(size)
            self.canvas.create_rectangle(
                x, y-2, x + 40, y+2,
                fill='gray', outline='dark gray'
            )
            self.canvas.create_text(
                x - 20, y,
                text=f"{size}bp",
                font=('Arial', 8),
                fill='black'
            )
        
        # Draw fragments in second lane
        x = 100 + self.LANE_WIDTH
        for fragment, start, end, gc_content in self.fragments:
            fragment_length = len(fragment)
            y = self.calculate_migration_distance(fragment_length)
            
            # Draw band
            self.canvas.create_rectangle(
                x, y-2, x + 40, y+2,
                fill='purple', outline='dark purple'
            )
            
            # Add length label
            self.canvas.create_text(
                x + 50, y,
                text=f"{fragment_length}bp",
                font=('Arial', 8),
                fill='black'
            )
    
    def reset_simulation(self):
        """Clear the gel and redraw the basic structure"""
        self.canvas.delete("all")
        self.draw_gel()

if __name__ == "__main__":
    root = tk.Tk()
    app = ElectrophoresisGel(root)
    root.mainloop()