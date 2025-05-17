import random

def generate_reference_string(length=20): 
    return [random.randint(0, 9) for _ in range(length)]

def parse_reference_string(string):
    if string.strip().isdigit(): 
        return [int(x) for x in string.split()]
    return [int(x) for x in string.split()] if all(x.isdigit() for x in string.split()) else None

def fifo_visual(pages, frames_count):
    frames, faults = [], 0
    history = []
    for page in pages:
        fault = page not in frames
        if fault: 
            faults += 1
            if len(frames) >= frames_count: frames.pop(0)
            frames.append(page)
        history.append((list(frames), page, fault))
    return faults, history

def lru_visual(pages, frames_count):
    frames, recent, faults = [], [], 0
    history = []
    for page in pages:
        fault = page not in frames
        if fault: 
            faults += 1
            if len(frames) >= frames_count:
                removed = recent.pop(0)
                if removed in frames: frames.remove(removed)
            frames.append(page)
        else: 
            if page in recent: recent.remove(page)
        recent.append(page)
        history.append((list(frames), page, fault))
    return faults, history

def opt_visual(pages, frames_count):
    frames, faults = [], 0
    history = []
    for i, page in enumerate(pages):
        fault = page not in frames
        if fault:
            faults += 1
            if len(frames) < frames_count:
                frames.append(page)
            else:
                future = [pages[i+1:].index(f) if f in pages[i+1:] else float('inf') for f in frames]
                frames[future.index(max(future))] = page
        history.append((list(frames), page, fault))
    return faults, history
