import tkinter as tk
from logic import (
    generate_reference_string,
    parse_reference_string,
    fifo_visual,
    lru_visual,
    opt_visual,
)


def draw_visual(history, frames_count, container, title):
    section = tk.LabelFrame(
        container, text=title, font=("Segoe UI", 14, "bold"),
        bg="#f0f0f0", padx=10, pady=10
    )
    section.pack(pady=15, fill="x", padx=20)

    grid = tk.Frame(section, bg="#f0f0f0")
    grid.pack(expand=True, fill="x")

    for t, (frame_snapshot, page, fault) in enumerate(history):
        for f in range(frames_count):
            bg_color = "#ffdddd" if fault and f == len(frame_snapshot) - 1 else "#e0f7fa"
            value = frame_snapshot[f] if f < len(frame_snapshot) else ""
            tk.Label(
                grid, text=value, width=4, font=("Arial", 12, "bold"),
                bg=bg_color, fg="#333", bd=2, relief="solid"
            ).grid(row=f, column=t, padx=2, pady=2)

        tk.Label(
            grid, text=str(page), font=("Arial", 11),
            fg="#007acc", bg="#f0f0f0"
        ).grid(row=frames_count, column=t, pady=(5, 0))



def run_all(pages=None):
    try:
        frames_count = int(entry_frames.get())
        if frames_count <= 0:
            raise ValueError("Number of frames must be greater than 0.")

        pages = pages or parse_reference_string(entry_ref_string.get().strip()) or generate_reference_string()

        if not pages:
            result_text.set("⚠️ Invalid reference string format.")
            return


        page_text.set("📘 Reference String: " + " ".join(map(str, pages)))
        fifo_faults, fifo_hist = fifo_visual(pages, frames_count)
        lru_faults, lru_hist = lru_visual(pages, frames_count)
        opt_faults, opt_hist = opt_visual(pages, frames_count)


        result_text.set(
            f"💥 Page Faults → FIFO: {fifo_faults} | LRU: {lru_faults} | OPT: {opt_faults}"
        )


        for widget in visual_frame.winfo_children():
            widget.destroy()


        draw_visual(fifo_hist, frames_count, visual_frame, "FIFO (First-In, First-Out)")
        draw_visual(lru_hist, frames_count, visual_frame, "LRU (Least Recently Used)")
        draw_visual(opt_hist, frames_count, visual_frame, "Optimal")

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    except Exception as e:
        result_text.set(f"⚠️ Error: {str(e)}")


def randomize_and_run():
    ref = generate_reference_string()
    entry_ref_string.delete(0, tk.END)
    entry_ref_string.insert(0, " ".join(str(x) for x in ref))
    run_all(ref)


root = tk.Tk()
try:
    root.iconbitmap("5882873.ico")
except Exception as e:
    print("⚠️ Could not load icon:", e)

root.title("📊 Page Replacement Visualizer")
root.geometry("1100x750")
root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())


header = tk.Frame(root, bg="#ecf0f1", pady=10)
header.pack(fill="x")

tk.Label(
    header, text="Page Replacement Visualizer",
    font=("Segoe UI", 24, "bold"), fg="#3498db", bg="#ecf0f1"
).pack()


input_frame = tk.Frame(root, bg="#ecf0f1", pady=10)
input_frame.pack(fill="x", padx=15)

tk.Label(input_frame, text="Frames:", font=("Arial", 12), bg="#ecf0f1").pack(side="left")
entry_frames = tk.Entry(input_frame, width=5, font=("Arial", 12))
entry_frames.pack(side="left", padx=5)

tk.Label(input_frame, text="Reference String:", font=("Arial", 12), bg="#ecf0f1").pack(side="left", padx=(15, 5))
entry_ref_string = tk.Entry(input_frame, width=40, font=("Arial", 12))
entry_ref_string.pack(side="left", padx=5, fill="x", expand=True)

tk.Button(
    input_frame, text="Run", font=("Arial", 10, "bold"),
    bg="#3498db", fg="white", command=run_all
).pack(side="left", padx=10)

tk.Button(
    input_frame, text="Randomize", font=("Arial", 10, "bold"),
    bg="#2ecc71", fg="white", command=randomize_and_run
).pack(side="left")


page_text = tk.StringVar()
result_text = tk.StringVar()

tk.Label(root, textvariable=page_text, font=("Courier New", 11), bg="#ecf0f1", fg="#555").pack(anchor="w", padx=15)
tk.Label(root, textvariable=result_text, font=("Arial", 16, "bold"), fg="#e67e22", bg="#ecf0f1").pack(anchor="w", padx=15, pady=(5, 0))

canvas = tk.Canvas(root, bg="#ecf0f1", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True, padx=15, pady=(0, 15))

scrollable_frame = tk.Frame(canvas, bg="#ecf0f1", padx=10, pady=10)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units")) 
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   

visual_frame = scrollable_frame

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


root.mainloop()
