import tkinter as tk
from logic import generate_reference_string, fifo_visual, lru_visual, opt_visual

ALGO_INFOS = {
    "FIFO (First-in-First-Out)": (
        "The FIFO page replacement algorithm manages pages in a queue structure, where the oldest page in "
        "memory the one loaded earliest is replaced first when a page fault occurs. This method does not account"
        "for page usage patterns or frequency, potentially leading to suboptimal performance, including Belady's"
        "anomaly, where increasing the number of frames can result in more page faults."
    ),
    "LRU (Least Recently Used)": (
        "The LRU algorithm replaces the page that has not been used for the longest time, based on the principle of temporal locality. "
        "By tracking recent page accesses, LRU aims to retain pages likely to be used again soon, thereby reducing page faults. "
        "Although effective in practice, implementing true LRU requires maintaining detailed access history, which can impose computational overhead."
    ),
    "OPT (Optimal)": (
        "The Optimal page replacement algorithm replaces the page that will not be used for the longest period in the future. "
        "It serves as a theoretical benchmark since it requires exact knowledge of future page references, which is generally unattainable in real systems. "
        "The Optimal algorithm establishes a lower bound on the number of page faults achievable by any algorithm for a given reference string and frame count."
    )
}

def draw_visual(history, frames, container, title):
    section = tk.LabelFrame(container, text=title, font=("Segoe UI", 14, "bold"), bg="white", fg="#2c3e50", padx=12, pady=12)
    section.pack(pady=15, fill="x", padx=20)
    grid = tk.Frame(section, bg="white")
    grid.pack(fill="x", expand=True)

    for t, (frame_snap, page, fault) in enumerate(history):
        for f in range(frames):
            bg = "#fdecea" if fault and f == len(frame_snap) - 1 else "#e8f6f3"
            val = frame_snap[f] if f < len(frame_snap) else ""
            tk.Label(grid, text=val, width=4, font=("Consolas", 12, "bold"), bg=bg, fg="#34495e", bd=1, relief="ridge").grid(row=f, column=t, padx=3, pady=3)
        tk.Label(grid, text=str(page), font=("Segoe UI", 11, "italic"), fg="#2980b9", bg="white").grid(row=frames, column=t, pady=(8, 0))

def run_all(pages=None):
    frames_str = entry_frames.get().strip()
    if not frames_str:
        result_text.set("⚠️ Please input how many frames.")
        return
    try:
        frames = int(frames_str)
        if frames <= 0:
            raise ValueError
    except ValueError:
        result_text.set("⚠️ Number of frames must be a positive integer.")
        return

    if pages is None:
        inp = entry_ref_string.get().strip()
        if inp:
            try:
                pages = [int(x) for x in inp.split()] if " " in inp else [int(x) for x in inp]
            except ValueError:
                result_text.set("⚠️ Invalid input. Use space separated numbers or a continuous sequence.")
                return
        else:
            pages = generate_reference_string()
            entry_ref_string.delete(0, tk.END)
            entry_ref_string.insert(0, " ".join(map(str, pages)))

    if len(pages) < 20:
        result_text.set("⚠️ Please input at least 20 page references.")
        return

    page_text.set("📘 Reference String: " + " ".join(map(str, pages)))

    fifo_faults, fifo_hist = fifo_visual(pages, frames)
    lru_faults, lru_hist = lru_visual(pages, frames)
    opt_faults, opt_hist = opt_visual(pages, frames)

    result_text.set(f"💥 Page Faults → FIFO: {fifo_faults} | LRU: {lru_faults} | OPT: {opt_faults}")

    for w in visual_frame.winfo_children():
        w.destroy()

    draw_visual(fifo_hist, frames, visual_frame, "FIFO (First-In, First-Out)")
    draw_visual(lru_hist, frames, visual_frame, "LRU (Least Recently Used)")
    draw_visual(opt_hist, frames, visual_frame, "Optimal")

    tk.Label(visual_frame, text="📚 Algorithm Information", font=("Segoe UI", 16, "bold"), bg="white", fg="#34495e").pack(fill="x", pady=(20, 12), padx=20)
    for algo, desc in ALGO_INFOS.items():
        f = tk.Frame(visual_frame, bg="white")
        f.pack(pady=8, padx=50)
        tk.Label(f, text=f"📌 {algo}", font=("Segoe UI", 13, "bold"), bg="white", fg="#27ae60").pack()
        tk.Label(f, text=desc, font=("Segoe UI", 11), bg="white", fg="#34495e", wraplength=800, justify="center").pack(padx=25, pady=(4, 0), fill="x")
        if algo != list(ALGO_INFOS.keys())[-1]:
            tk.Frame(visual_frame, height=1, bg="#dcdde1").pack(fill="x", pady=(8, 0), padx=50)

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def randomize_and_run():
    frames_str = entry_frames.get().strip()
    if not frames_str:
        result_text.set("⚠️ Please enter the number of frames.")
        return
    try:
        frames = int(frames_str)
        if frames <= 0:
            raise ValueError
    except ValueError:
        result_text.set("⚠️ Number of frames must be a positive integer.")
        return

    ref = generate_reference_string()
    entry_ref_string.delete(0, tk.END)
    entry_ref_string.insert(0, " ".join(map(str, ref)))
    run_all()

root = tk.Tk()
try:
    root.iconbitmap("5882873.ico")
except tk.TclError:
    pass
root.title("📊 Page Replacement Visualizer")
root.geometry("1150x780")
root.configure(bg="#f5f7fa")

def center_win():
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

root.after(0, center_win)

header = tk.Frame(root, bg="#34495e", pady=12)
header.pack(fill="x")
tk.Label(header, text="Page Replacement Visualizer", font=("Segoe UI", 26, "bold"), fg="#ecf0f1", bg="#34495e").pack()

input_frame = tk.Frame(root, bg="#ecf0f1", pady=12)
input_frame.pack(fill="x", padx=15)

tk.Label(input_frame, text="Frames:", font=("Segoe UI", 13), bg="#ecf0f1", fg="#2c3e50").pack(side="left")
entry_frames = tk.Entry(input_frame, width=6, font=("Segoe UI", 13))
entry_frames.pack(side="left", padx=7)

tk.Label(input_frame, text="Reference String:", font=("Segoe UI", 13), bg="#ecf0f1", fg="#2c3e50").pack(side="left", padx=(20,7))
entry_ref_string = tk.Entry(input_frame, width=42, font=("Segoe UI", 13))
entry_ref_string.pack(side="left", padx=5, fill="x", expand=True)

tk.Button(input_frame, text="Run", font=("Segoe UI", 12, "bold"), bg="#2980b9", fg="white", activebackground="#1c5980", relief="flat", padx=12, pady=6, command=run_all).pack(side="left", padx=12)
tk.Button(input_frame, text="Randomize", font=("Segoe UI", 12, "bold"), bg="#27ae60", fg="white", activebackground="#1b7730", relief="flat", padx=12, pady=6, command=randomize_and_run).pack(side="left")

result_text = tk.StringVar()
page_text = tk.StringVar()
tk.Label(root, textvariable=result_text, font=("Segoe UI", 14, "bold"), fg="#e67e22", bg="#f5f7fa", anchor="w", padx=20, pady=15).pack(fill="x")

visual_container = tk.Frame(root, bg="white")
visual_container.pack(fill="both", expand=True, padx=(15,0), pady=(0,10))

canvas = tk.Canvas(visual_container, bg="white", highlightthickness=0)
scrollbar = tk.Scrollbar(visual_container, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

scrollable_frame = tk.Frame(canvas, bg="white", padx=10, pady=10)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

visual_frame = scrollable_frame
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

root.mainloop()
