import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from pile_calculation import calculate_pile_capacity


def show_info():
    messagebox.showinfo("Cohesion Multiplier Info",
                        "Cohesion = k * Ncorrected (KPa)\nWhere k = 2.4 to 4 for softer to stiffer clay,\ninput the value of k according to your soil condition.")


def show_disclaimer():
    disclaimer_window = tk.Tk()  # Start with the disclaimer window as the root
    disclaimer_window.title("Disclaimer")
    disclaimer_window.geometry("400x250")

    disclaimer_message = ("This software is designed to calculate the capacity of a single pile using empirical "
                          "relationships based on SPT N values and soil type. It is intended for use when detailed "
                          "soil property information, such as cohesion or angle of friction, is unavailable or unreliable. "
                          "If precise soil properties are known, it is recommended to use more accurate calculation methods.")

    disclaimer_label = tk.Label(disclaimer_window, text=disclaimer_message, wraplength=350, justify="left")
    disclaimer_label.pack(padx=20, pady=20)

    agree_button = ttk.Button(disclaimer_window, text="Agree and Continue",
                              command=lambda: start_application(disclaimer_window))
    agree_button.pack(pady=10)

    disclaimer_window.mainloop()


def start_application(disclaimer_window):
    disclaimer_window.destroy()  # Close the disclaimer window
    initialize_gui()  # Start the main application


def focus_next_widget_in_column(event):
    """Move focus to the next widget in the same column when Enter key is pressed."""
    widget = event.widget
    row = int(widget.grid_info()['row'])
    col = int(widget.grid_info()['column'])
    next_widget = widget.master.grid_slaves(row=row + 1, column=col)
    if next_widget:
        next_widget[0].focus_set()
    return "break"


def create_rows():
    try:
        layer_number = int(layer_number_entry.get())
        for widget in table_frame.winfo_children():
            widget.destroy()  # Clear any existing rows

        # Headers for the input table with units
        headers = ["Layer No.", "Depth (m)", "Soil Type", "Field SPT"]
        for j, header in enumerate(headers):
            ttk.Label(table_frame, text=header, style="Header.TLabel").grid(row=1, column=j, padx=6, pady=6)

        global layer_no_entries, depth_entries, soil_type_entries, field_spt_entries
        layer_no_entries = []
        depth_entries = []
        soil_type_entries = []
        field_spt_entries = []

        for i in range(layer_number):
            # Layer No.
            layer_no_label = ttk.Label(table_frame, text=f"{i + 1}", style="TLabel")
            layer_no_label.grid(row=i + 2, column=0, padx=6, pady=6)
            layer_no_entries.append(layer_no_label)

            # Depth (m)
            depth_entry = ttk.Entry(table_frame, style="TEntry")
            depth_entry.grid(row=i + 2, column=1, padx=6, pady=6)
            depth_entry.bind("<Return>", focus_next_widget_in_column)
            depth_entries.append(depth_entry)

            # Soil Type (Cohesive or Cohesionless)
            soil_type_var = tk.StringVar(value="Cohesionless")
            soil_type_menu = ttk.OptionMenu(table_frame, soil_type_var, "Cohesionless", "Cohesionless", "Cohesive")
            soil_type_menu.grid(row=i + 2, column=2, padx=6, pady=6)
            soil_type_menu.bind("<Return>", focus_next_widget_in_column)
            soil_type_entries.append(soil_type_var)

            # Field SPT
            field_spt_entry = ttk.Entry(table_frame, style="TEntry")
            field_spt_entry.grid(row=i + 2, column=3, padx=6, pady=6)
            field_spt_entry.bind("<Return>", focus_next_widget_in_column)
            field_spt_entries.append(field_spt_entry)

        # Show the Calculate button and Restart button above the input table
        calculate_button.grid(row=0, column=2, padx=8, pady=12)
        restart_button.grid(row=0, column=3, padx=8, pady=12)

        # Change the "Let's Begin" button to a "Restart" button
        create_button.grid_remove()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for the number of layers.")


def calculate_pile_capacity_gui():
    try:
        layer_number = int(layer_number_entry.get())
        diameter_pile = float(diameter_pile_entry.get())
        factor_of_safety = float(factor_of_safety_entry.get())
        k_value = float(k_value_entry.get())  # User-defined multiplier for cohesion

        table_data = np.zeros((layer_number, 3), dtype=object)

        for i in range(layer_number):
            table_data[i, 0] = soil_type_entries[i].get()  # Soil Type
            table_data[i, 1] = float(depth_entries[i].get())  # Depth (m)
            table_data[i, 2] = float(field_spt_entries[i].get())  # Field SPT

        results = calculate_pile_capacity(
            layer_number, table_data, diameter_pile, factor_of_safety, k_value)  # Pass k_value to the function

        display_results(results)

    except Exception as e:
        messagebox.showerror("Input Error", f"An error occurred: {e}")


def display_results(results):
    for widget in results_table_frame.winfo_children():
        widget.destroy()  # Clear any existing results

    headers = ["Depth (m)", "Ultimate End Bearing(kN)", "Ultimate Skin Friction(kN)",
               "Allowable Pile Resistance,Qa (kN /kip)"]
    for j, header in enumerate(headers):
        ttk.Label(results_table_frame, text=header, style="Header.TLabel").grid(row=1, column=j, padx=6, pady=6)

    for i, result in enumerate(results):
        Q_a_kN = result[3]
        Q_a_kip = Q_a_kN * 0.224809  # Convert kN to kip

        ttk.Label(results_table_frame, text=f"{result[0]:.2f}", style="TLabel").grid(row=i + 2, column=0, padx=6,
                                                                                     pady=6)
        ttk.Label(results_table_frame, text=f"{result[2]:.2f} kN", style="TLabel").grid(row=i + 2, column=1, padx=6,
                                                                                        pady=6)
        ttk.Label(results_table_frame, text=f"{result[1]:.2f} kN", style="TLabel").grid(row=i + 2, column=2, padx=6,
                                                                                        pady=6)
        ttk.Label(results_table_frame, text=f"{Q_a_kN:.2f} kN ({Q_a_kip:.2f} kip)", style="TLabel").grid(row=i + 2,
                                                                                                         column=3,
                                                                                                         padx=6, pady=6)


def restart_process():
    # Clear only the input table fields and keep everything else intact
    for entry in depth_entries:
        entry.delete(0, tk.END)
    for entry in field_spt_entries:
        entry.delete(0, tk.END)
    for var in soil_type_entries:
        var.set("Cohesionless")


def initialize_gui():
    global layer_number_entry, diameter_pile_entry, factor_of_safety_entry, k_value_entry
    global calculate_button, create_button, restart_button, results_table_frame, table_frame
    global depth_entries, field_spt_entries, soil_type_entries

    root = tk.Tk()
    root.title("Single Pile Capacity Calculator")

    # Set the theme and style
    style = ttk.Style()

    style.configure("TLabel", padding=(10, 5))
    style.configure("TButton", padding=(20, 10))
    style.configure("TEntry", padding=(5, 5))
    style.configure("TCheckbutton", padding=(10, 5))
    style.configure("TFrame", padding=(20, 10))
    style.configure("TLabelframe", padding=(20, 10))
    style.configure("TCombobox", padding=(5, 5))

    style.configure("TLabel", font=("Helvetica", 10), foreground="#000000")  # Black text
    style.configure("Header.TLabel", font=("Helvetica", 10, "bold"), foreground="#000000")  # Black header text
    style.configure("TButton", font=("Helvetica", 10, "bold"), background="#4F81BD", foreground="black")  # Button style
    style.configure("TEntry", relief="solid", borderwidth=1)
    style.configure("TFrame", background="#FFFFFF")  # Frame background

    root.configure(bg="#F0F0F0")

    # Create a main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    # Create a Canvas
    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Add a Scrollbar to the Canvas
    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the Canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create another frame inside the Canvas
    second_frame = tk.Frame(canvas)

    # Add that new frame to a window in the canvas
    canvas.create_window((0, 0), window=second_frame, anchor="nw")

    # Bind mouse wheel to scroll
    second_frame.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    # Input fields for layer number, pile diameter, factor of safety, and pile length with units
    factor_of_safety_label = ttk.Label(second_frame, text="Factor of Safety:", style="TLabel")
    factor_of_safety_label.grid(row=0, column=0, padx=6, pady=6)
    factor_of_safety_entry = ttk.Entry(second_frame, style="TEntry")
    factor_of_safety_entry.grid(row=0, column=1, padx=6, pady=6)

    layer_number_label = ttk.Label(second_frame, text="Number of Layers:", style="TLabel")
    layer_number_label.grid(row=1, column=0, padx=6, pady=6)
    layer_number_entry = ttk.Entry(second_frame, style="TEntry")
    layer_number_entry.grid(row=1, column=1, padx=6, pady=6)

    diameter_pile_label = ttk.Label(second_frame, text="Pile Diameter (m):", style="TLabel")
    diameter_pile_label.grid(row=2, column=0, padx=6, pady=6)
    diameter_pile_entry = ttk.Entry(second_frame, style="TEntry")
    diameter_pile_entry.grid(row=2, column=1, padx=6, pady=6)

    # New input for k-value (Cohesion multiplier) with embedded input and info button
    k_value_frame = ttk.Frame(second_frame)
    k_value_frame.grid(row=3, column=0, columnspan=3, padx=6, pady=6, sticky="w")

    k_value_label = ttk.Label(k_value_frame, text="Cohesion = ", style="TLabel")
    k_value_label.pack(side=tk.LEFT)

    k_value_entry = ttk.Entry(k_value_frame, width=5, style="TEntry")
    k_value_entry.pack(side=tk.LEFT)

    k_value_label_suffix = ttk.Label(k_value_frame, text=" * Ncorrected (KPa)", style="TLabel")
    k_value_label_suffix.pack(side=tk.LEFT)

    info_button = ttk.Button(k_value_frame, text="Info", command=show_info, style="TButton", width=4)
    info_button.pack(side=tk.LEFT, padx=6)

    # "Let's Begin" button, which will convert to "Restart" after being pressed
    create_button = ttk.Button(second_frame, text="Let's Begin", command=create_rows, style="TButton")
    create_button.grid(row=4, column=0, columnspan=2, padx=8, pady=12)

    # Table for soil profile data
    table_frame = ttk.Frame(second_frame, style="TFrame")
    table_frame.grid(row=5, column=0, columnspan=5, padx=6, pady=6)

    # Results table for calculated values, placed beside the input table
    results_table_frame = ttk.Frame(second_frame, style="TFrame")
    results_table_frame.grid(row=5, column=6, columnspan=5, padx=6, pady=6)

    # Calculate button placed beside the Restart button, above the input table
    calculate_button = ttk.Button(second_frame, text="Calculate Pile Capacity", command=calculate_pile_capacity_gui,
                                  style="TButton")
    restart_button = ttk.Button(second_frame, text="Refresh", command=restart_process, style="TButton")

    # Update the greetings section at the bottom of the GUI
    greetings_label = ttk.Label(second_frame, text="For any query: irfan.buet18@gmail.com, imrozekhan169@gmail.com",
                                style="TLabel", justify="center", font=("Helvetica", 10, "italic"))
    greetings_label.grid(row=7, column=0, columnspan=10, padx=8, pady=12)

    root.mainloop()


# Start the application with the disclaimer
show_disclaimer()