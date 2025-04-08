import tkinter as tk
from tkinter import messagebox

def convert_size(size, from_unit, to_unit, magnification=1):
    # Conversion factors to millimeters (mm)
    conversion_factors = {
        'mm': 1,
        'cm': 10,
        'm': 1000,
        'inches': 25.4,
        'feet': 304.8,
        'um': 0.001  # Micrometers to mm
    }
    
    # Check for valid units
    if from_unit not in conversion_factors or to_unit not in conversion_factors:
        return None
    
    # Convert the size to millimeters
    size_in_mm = size * conversion_factors[from_unit]
    
    # Apply magnification as a divisor
    magnified_size_in_mm = size_in_mm / magnification
    
    # Convert the magnified size from mm to the desired unit
    converted_size = magnified_size_in_mm / conversion_factors[to_unit]
    
    return converted_size

def calculate():
    try:
        size = float(size_entry.get())
        from_unit = from_unit_var.get()
        to_unit = to_unit_var.get()
        magnification = float(magnification_entry.get()) if magnification_entry.get() else 1
        
        result = convert_size(size, from_unit, to_unit, magnification)
        
        if result is not None:
            result_label.config(text=f"Real Life size: {result:.2f} {to_unit}")
        else:
            messagebox.showerror("Error", "Invalid unit provided.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")

# Set up the main application window
root = tk.Tk()
root.title("Specimen Size Converter")

# Labels and Entries
tk.Label(root, text="Size of the specimen:").grid(row=0, column=0)
size_entry = tk.Entry(root)
size_entry.grid(row=0, column=1)

tk.Label(root, text="Current unit:").grid(row=1, column=0)
from_unit_var = tk.StringVar(value='mm')
from_unit_options = ['mm', 'cm', 'm', 'inches', 'feet', 'um']
from_unit_menu = tk.OptionMenu(root, from_unit_var, *from_unit_options)
from_unit_menu.grid(row=1, column=1)

tk.Label(root, text="Unit to convert to:").grid(row=2, column=0)
to_unit_var = tk.StringVar(value='um')
to_unit_menu = tk.OptionMenu(root, to_unit_var, *from_unit_options)
to_unit_menu.grid(row=2, column=1)

tk.Label(root, text="Magnification factor (default is 1):").grid(row=3, column=0)
magnification_entry = tk.Entry(root)
magnification_entry.grid(row=3, column=1)

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.grid(row=4, columnspan=2)

# Result label
result_label = tk.Label(root, text="")
result_label.grid(row=5, columnspan=2)

# Replace 'myenv' with your desired environment name


# Start the Tkinter event loop
root.mainloop()