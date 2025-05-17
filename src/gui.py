import tkinter as tk
from logic import (
    generate_reference_string,
    parse_reference_string,
    fifo_visual,
    lru_visual,
    opt_visual,
)

ALGO_INFOS = {
    "FIFO": (
        "The FIFO (First-In, First-Out) page replacement algorithm operates on a straightforward principle: the page that has resided in memory for the longest duration is the first to be replaced. "
        "Imagine a queue where pages enter when they are needed and exit from the front when a new page needs to be loaded. "
        "While simple to implement, FIFO doesn't consider the frequency or recency of page usage. A frequently used page that happened to be loaded early will be replaced just like a rarely used one. "
        "This can lead to a phenomenon known as Belady's anomaly, where increasing the number of available frames might paradoxically increase the number of page faults in certain scenarios."
    ),
    "LRU": (
        "The LRU (Least Recently Used) page replacement algorithm is based on the principle of locality of reference, which suggests that pages that have been used recently are likely to be used again in the near future. "
        "LRU works by keeping track of the last time each page in memory was accessed. When a page fault occurs and a replacement is needed, LRU evicts the page that has not been used for the longest period. "
        "This strategy generally performs well because it prioritizes keeping actively used pages in memory. However, implementing LRU perfectly can be complex and might require significant overhead to track the usage history of each page."
    ),
    "OPT": (
        "The Optimal (OPT) page replacement algorithm, sometimes referred to as MIN (Minimum), is a theoretical benchmark for page replacement algorithms. "
        "When a page fault occurs, OPT looks into the future and replaces the page that will not be used for the longest period of time. In other words, it has perfect foresight of the future page reference string. "
        "Because it requires knowledge of future page requests, OPT is not practically implementable in a real-world operating system. However, it serves as an invaluable tool for comparing the performance of other page replacement algorithms in simulations. "
        "The performance of OPT represents the absolute minimum number of page faults that can occur for a given reference string and number of frames."
    )
}

def draw_visual(history, frames_count, container, title):
    section = tk.LabelFrame(
        container,
        text=title,
        font=("Segoe UI", 14, "bold"),
        bg="#ffffff",
        fg="#2c3e50",
        padx=12,
        pady=12,
        bd=2,
        relief="groove"
    )
    section.pack(pady=15, fill="x", padx=20)

    grid = tk.Frame(section, bg="#ffffff")
    grid.pack(expand=True, fill="x")

    for t, (frame_snapshot, page, fault) in enumerate(history):
        for f in range(frames_count):
            bg_color = "#fdecea" if fault and f == len(frame_snapshot) - 1 else "#e8f6f3"
            value = frame_snapshot[f] if f < len(frame_snapshot) else ""
            tk.Label(
                grid,
                text=value,
                width=4,
                font=("Consolas", 12, "bold"),
                bg=bg_color,
                fg="#34495e",
                bd=1,
                relief="ridge"
            ).grid(row=f, column=t, padx=3, pady=3)

        tk.Label(
            grid,
            text=str(page),
            font=("Segoe UI", 11, "italic"),
            fg="#2980b9",
            bg="#ffffff"
        ).grid(row=frames_count, column=t, pady=(8, 0))


def run_all(pages=None):
    try:
        frames_input = entry_frames.get().strip()
        if not frames_input:
            result_text.set("⚠️ Please input how many frames.")
            return

        frames_count = int(frames_input)
        if frames_count <= 0:
            raise ValueError("Number of frames must be greater than 0.")

        user_input = entry_ref_string.get().strip()
        if user_input:
            try:
                pages = [int(p) for p in user_input]
            except ValueError:
                result_text.set("⚠️ Invalid input. Enter numbers separated by spaces (e.g., 1 2 3 ...) or as a sequence (e.g., 123...). Minimum 20 references.")
                return
        else:
            pages = generate_reference_string()
            entry_ref_string.delete(0, tk.END)
            entry_ref_string.insert(0, " ".join(str(x) for x in pages))

        if not pages:
            result_text.set("⚠️ Please input a reference string (e.g., 1 2 3 ...).")
            return

        if len(pages) < 20:
            result_text.set("⚠️ Please input at least 20 page references separated by spaces (e.g., 1 2 3 ...) or as a sequence (e.g., 123...).")
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

        info_title_label = tk.Label(
            visual_frame,
            text="📚 Algorithm Information",
            font=("Segoe UI", 16, "bold"),
            bg="#ffffff",
            fg="#34495e",
            anchor="center"
        )
        info_title_label.pack(fill="x", pady=(20, 12), padx=20)

        for algo, desc in ALGO_INFOS.items():
            algo_frame = tk.Frame(visual_frame, bg="white")
            algo_frame.pack(pady=8, padx=50)
            algo_frame.columnconfigure(0, weight=1)

            title = tk.Label(
                algo_frame,
                text=f"📌 {algo}",
                font=("Segoe UI", 13, "bold"),
                bg="white",
                fg="#27ae60",
                anchor="center"
            )
            title.pack()
            title.columnconfigure(0, weight=1)

            desc_label = tk.Label(
                algo_frame,
                text=desc,
                font=("Segoe UI", 11),
                bg="white",
                fg="#34495e",
                wraplength=800,
                justify="center",
                anchor="center"
            )
            desc_label.pack(padx=25, pady=(4, 0), fill="x")
            desc_label.columnconfigure(0, weight=1)

            if algo != list(ALGO_INFOS.keys())[-1]:
                sep = tk.Frame(visual_frame, height=1, bg="#dcdde1")
                sep.pack(fill="x", pady=(8, 0), padx=50)
                sep.columnconfigure(0, weight=1)

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    except ValueError as ve:
        result_text.set(f"⚠️ Error: {ve}")
    except Exception as e:
        result_text.set(f"⚠️ An unexpected error occurred: {str(e)}")

def randomize_and_run():
    try:
        frames_count = int(entry_frames.get())
        if frames_count <= 0:
            raise ValueError("Number of frames must be greater than 0.")
    except ValueError:
        result_text.set("⚠️ Please input a valid number of frames.")
        return
    except Exception:
        result_text.set("⚠️ An unexpected error occurred while reading frames.")
        return

    ref = generate_reference_string()
    entry_ref_string.delete(0, tk.END)
    entry_ref_string.insert(0, " ".join(str(x) for x in ref))
    run_all(ref)


root = tk.Tk()
try:
    root.iconbitmap("5882873.ico")
except tk.TclError as e:
    print("⚠️ Could not load icon:", e)

root.title("📊 Page Replacement Visualizer")
root.geometry("1150x780")
root.configure(bg="#f5f7fa")

def center_window():
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

root.after(0, center_window)

header = tk.Frame(root, bg="#34495e", pady=12)
header.pack(fill="x")

tk.Label(
    header,
    text="Page Replacement Visualizer",
    font=("Segoe UI", 26, "bold"),
    fg="#ecf0f1",
    bg="#34495e"
).pack()

input_frame = tk.Frame(root, bg="#ecf0f1", pady=12)
input_frame.pack(fill="x", padx=15)

tk.Label(input_frame, text="Frames:", font=("Segoe UI", 13), bg="#ecf0f1", fg="#2c3e50").pack(side="left")
entry_frames = tk.Entry(input_frame, width=6, font=("Segoe UI", 13))
entry_frames.pack(side="left", padx=7)

tk.Label(input_frame, text="Reference String:", font=("Segoe UI", 13), bg="#ecf0f1", fg="#2c3e50").pack(side="left", padx=(20, 7))
entry_ref_string = tk.Entry(input_frame, width=42, font=("Segoe UI", 13))
entry_ref_string.pack(side="left", padx=5, fill="x", expand=True)

tk.Button(
    input_frame,
    text="Run",
    font=("Segoe UI", 12, "bold"),
    bg="#2980b9",
    fg="white",
    activebackground="#1c5980",
    activeforeground="#ecf0f1",
    relief="flat",
    padx=12,
    pady=6,
    command=run_all
).pack(side="left", padx=12)

tk.Button(
    input_frame,
    text="Randomize",
    font=("Segoe UI", 12, "bold"),
    bg="#27ae60",
    fg="white",
    activebackground="#1b7730",
    activeforeground="#ecf0f1",
    relief="flat",
    padx=12,
    pady=6,
    command=randomize_and_run
).pack(side="left")

page_text = tk.StringVar()
result_text = tk.StringVar()

tk.Label(
    root,
    textvariable=result_text,
    font=("Segoe UI", 14, "bold"),  # Slightly smaller, but still noticeable
    fg="#e67e22",
    bg="#f5f7fa",
    anchor="w",
    padx=20,
    pady=15
).pack(fill="x")

visual_container = tk.Frame(root, bg="#ffffff")
visual_container.pack(fill="both", expand=True, padx=(15,0), pady=(0, 10))

canvas = tk.Canvas(visual_container, bg="#ffffff", highlightthickness=0)
scrollbar = tk.Scrollbar(visual_container, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

scrollable_frame = tk.Frame(canvas, bg="#ffffff", padx=10, pady=10)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))  # Linux scroll down

visual_frame = scrollable_frame

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

root.mainloop()
