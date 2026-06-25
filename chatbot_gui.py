import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os

from chatbot_engine import get_bot_response
from faq_topics import FAQ_TOPICS

# =========================================================
# CONFIG
# =========================================================
CHAT_HISTORY_FILE = "chat_history.json"
EXPORT_FOLDER = "exported_chats"

if not os.path.exists(EXPORT_FOLDER):
    os.makedirs(EXPORT_FOLDER)

# Colors
BG_MAIN = "#edf4ff"
CARD_BG = "#ffffff"
SIDEBAR_BG = "#0f172a"
SIDEBAR_INNER = "#111827"
HEADER_GRADIENT = "#2563eb"
CHAT_BG = "#f8fbff"

BOT_BUBBLE = "#e0ecff"
USER_BUBBLE = "#d1fae5"

BOT_NAME = "#1d4ed8"
USER_NAME = "#059669"

TEXT_DARK = "#111827"
TEXT_MUTED = "#6b7280"
WHITE = "#ffffff"

TOPIC_BTN = "#1e293b"
TOPIC_BTN_HOVER = "#334155"
FAQ_BTN = "#eff6ff"
FAQ_BTN_TEXT = "#1d4ed8"

SEND_BTN = "#2563eb"
SEND_BTN_HOVER = "#1d4ed8"

CLEAR_BTN = "#ef4444"
EXPORT_BTN = "#0ea5e9"

# =========================================================
# ROOT WINDOW
# =========================================================
root = tk.Tk()
root.title("AI Internship & Student Helpdesk Assistant")
root.geometry("1260x790")
root.configure(bg=BG_MAIN)
root.minsize(1120, 700)

chat_history = []

# =========================================================
# DATA / FILE HELPERS
# =========================================================
def current_time():
    return datetime.now().strftime("%I:%M %p")

def save_chat_history():
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=4, ensure_ascii=False)

def export_chat():
    if not chat_history:
        messagebox.showinfo("Export Chat", "No chat available to export.")
        return

    filename = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(EXPORT_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("AI Internship & Student Helpdesk Assistant - Chat Export\n")
        f.write("=" * 70 + "\n\n")
        for entry in chat_history:
            f.write(f"[{entry['time']}] {entry['sender']}: {entry['message']}\n\n")

    messagebox.showinfo("Export Chat", f"Chat exported successfully.\nSaved at:\n{filepath}")

def clear_chat():
    global chat_history
    chat_history = []
    save_chat_history()

    for widget in messages_frame.winfo_children():
        widget.destroy()

    add_bot_message(
        "Hello 👋 I’m your AI Internship & Student Helpdesk Assistant.\n\n"
        "I can help with:\n"
        "• internship domains\n"
        "• certificate\n"
        "• project submission\n"
        "• internship fee\n"
        "• company/services\n"
        "• support and working hours\n\n"
        "Use the topic panel on the left to browse FAQs or type your question below."
    )

def load_chat_history():
    if not os.path.exists(CHAT_HISTORY_FILE):
        return []

    try:
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# =========================================================
# CHAT BUBBLE HELPERS
# =========================================================
def scroll_to_bottom():
    root.update_idletasks()
    canvas.yview_moveto(1.0)

def add_message_to_history(sender, message):
    entry = {
        "sender": sender,
        "message": message,
        "time": current_time()
    }
    chat_history.append(entry)
    save_chat_history()
    return entry["time"]

def create_message_bubble(sender, message, timestamp):
    outer = tk.Frame(messages_frame, bg=CHAT_BG)
    outer.pack(fill="x", padx=14, pady=8, anchor="w")

    is_user = sender == "You"

    row = tk.Frame(outer, bg=CHAT_BG)
    row.pack(fill="x", anchor="e" if is_user else "w")

    if is_user:
        row.columnconfigure(0, weight=1)
        bubble_wrap = tk.Frame(row, bg=CHAT_BG)
        bubble_wrap.grid(row=0, column=1, sticky="e")
    else:
        row.columnconfigure(1, weight=1)
        bubble_wrap = tk.Frame(row, bg=CHAT_BG)
        bubble_wrap.grid(row=0, column=0, sticky="w")

    name_color = USER_NAME if is_user else BOT_NAME
    bubble_color = USER_BUBBLE if is_user else BOT_BUBBLE
    align = "e" if is_user else "w"

    name_label = tk.Label(
        bubble_wrap,
        text=f"{sender} • {timestamp}",
        bg=CHAT_BG,
        fg=name_color,
        font=("Arial", 9, "bold")
    )
    name_label.pack(anchor=align, padx=2, pady=(0, 3))

    bubble = tk.Frame(
        bubble_wrap,
        bg=bubble_color,
        bd=0,
        highlightthickness=0
    )
    bubble.pack(anchor=align)

    msg = tk.Label(
        bubble,
        text=message,
        bg=bubble_color,
        fg=TEXT_DARK,
        font=("Arial", 11),
        justify="left",
        wraplength=620,
        padx=16,
        pady=12
    )
    msg.pack(anchor="w")

    scroll_to_bottom()

def add_user_message(message):
    timestamp = add_message_to_history("You", message)
    create_message_bubble("You", message, timestamp)

def add_bot_message(message):
    timestamp = add_message_to_history("Assistant", message)
    create_message_bubble("Assistant", message, timestamp)

# =========================================================
# CHAT ACTIONS
# =========================================================
def ask_question(text):
    user_input.delete(0, tk.END)
    add_user_message(text)

    result = get_bot_response(text)
    bot_reply = result["response"]
    add_bot_message(bot_reply)

def send_message(event=None):
    text = user_input.get().strip()
    if not text:
        return
    ask_question(text)

# =========================================================
# FAQ / ACCORDION UI
# =========================================================
topic_containers = {}

def toggle_topic(topic_name):
    container = topic_containers[topic_name]
    faq_frame = container["faq_frame"]
    arrow_label = container["arrow"]

    if container["expanded"]:
        faq_frame.pack_forget()
        arrow_label.config(text="▸")
        container["expanded"] = False
    else:
        faq_frame.pack(fill="x", padx=10, pady=(0, 8))
        arrow_label.config(text="▾")
        container["expanded"] = True

def create_topic_block(parent, topic_name, faq_list):
    block = tk.Frame(parent, bg=SIDEBAR_BG)
    block.pack(fill="x", pady=(0, 10))

    topic_btn = tk.Frame(block, bg=TOPIC_BTN, cursor="hand2")
    topic_btn.pack(fill="x", padx=8)

    arrow = tk.Label(
        topic_btn,
        text="▸",
        bg=TOPIC_BTN,
        fg=WHITE,
        font=("Arial", 12, "bold")
    )
    arrow.pack(side="left", padx=(12, 6), pady=12)

    title = tk.Label(
        topic_btn,
        text=topic_name,
        bg=TOPIC_BTN,
        fg=WHITE,
        font=("Arial", 11, "bold")
    )
    title.pack(side="left", pady=12)

    faq_frame = tk.Frame(block, bg=SIDEBAR_BG)

    topic_containers[topic_name] = {
        "faq_frame": faq_frame,
        "arrow": arrow,
        "expanded": False
    }

    def on_enter(e):
        topic_btn.config(bg=TOPIC_BTN_HOVER)
        arrow.config(bg=TOPIC_BTN_HOVER)
        title.config(bg=TOPIC_BTN_HOVER)

    def on_leave(e):
        topic_btn.config(bg=TOPIC_BTN)
        arrow.config(bg=TOPIC_BTN)
        title.config(bg=TOPIC_BTN)

    def on_click(e=None):
        toggle_topic(topic_name)

    topic_btn.bind("<Enter>", on_enter)
    topic_btn.bind("<Leave>", on_leave)
    topic_btn.bind("<Button-1>", on_click)
    arrow.bind("<Button-1>", on_click)
    title.bind("<Button-1>", on_click)

    for question in faq_list:
        faq_btn = tk.Button(
            faq_frame,
            text="• " + question,
            font=("Arial", 10),
            bg=FAQ_BTN,
            fg=FAQ_BTN_TEXT,
            activebackground="#dbeafe",
            activeforeground=FAQ_BTN_TEXT,
            relief="flat",
            bd=0,
            justify="left",
            wraplength=250,
            anchor="w",
            padx=12,
            pady=10,
            cursor="hand2",
            command=lambda q=question: ask_question(q)
        )
        faq_btn.pack(fill="x", padx=18, pady=4)

# =========================================================
# MAIN LAYOUT
# =========================================================
outer = tk.Frame(root, bg=BG_MAIN)
outer.pack(fill="both", expand=True, padx=14, pady=14)

# ---------------- LEFT SIDEBAR ----------------
left_panel = tk.Frame(outer, bg=SIDEBAR_BG, width=320)
left_panel.pack(side="left", fill="y", padx=(0, 14))
left_panel.pack_propagate(False)

left_header = tk.Frame(left_panel, bg=SIDEBAR_BG)
left_header.pack(fill="x", padx=14, pady=(16, 8))

left_title = tk.Label(
    left_header,
    text="Topics & FAQs",
    bg=SIDEBAR_BG,
    fg=WHITE,
    font=("Arial", 18, "bold")
)
left_title.pack(anchor="w")

left_subtitle = tk.Label(
    left_header,
    text="Click a topic to view the FAQs under it.",
    bg=SIDEBAR_BG,
    fg="#cbd5e1",
    font=("Arial", 10),
    justify="left",
    wraplength=260
)
left_subtitle.pack(anchor="w", pady=(4, 0))

faq_area = tk.Frame(left_panel, bg=SIDEBAR_BG)
faq_area.pack(fill="both", expand=True, padx=8, pady=10)

for topic, faq_list in FAQ_TOPICS.items():
    create_topic_block(faq_area, topic, faq_list)

left_bottom = tk.Frame(left_panel, bg=SIDEBAR_INNER, bd=0)
left_bottom.pack(fill="x", padx=14, pady=(8, 16))

tips_title = tk.Label(
    left_bottom,
    text="Tips",
    bg=SIDEBAR_INNER,
    fg=WHITE,
    font=("Arial", 11, "bold")
)
tips_title.pack(anchor="w", padx=12, pady=(12, 6))

tips_text = tk.Label(
    left_bottom,
    text=(
        "• Use the FAQ topics if you don’t know what to ask.\n"
        "• This bot is best for internship/helpdesk questions.\n"
        "• If it is unsure, it gives a safer fallback reply."
    ),
    bg=SIDEBAR_INNER,
    fg="#cbd5e1",
    font=("Arial", 9),
    justify="left",
    wraplength=255
)
tips_text.pack(anchor="w", padx=12, pady=(0, 12))

# ---------------- RIGHT SIDE ----------------
right_panel = tk.Frame(outer, bg=BG_MAIN)
right_panel.pack(side="right", fill="both", expand=True)

# Header Card
header_card = tk.Frame(right_panel, bg=CARD_BG, bd=0)
header_card.pack(fill="x", pady=(0, 12))

header_top = tk.Frame(header_card, bg=HEADER_GRADIENT, height=96)
header_top.pack(fill="x")
header_top.pack_propagate(False)

header_title = tk.Label(
    header_top,
    text="AI Internship & Student Helpdesk Assistant",
    bg=HEADER_GRADIENT,
    fg=WHITE,
    font=("Arial", 22, "bold")
)
header_title.pack(anchor="w", padx=20, pady=(18, 2))

header_sub = tk.Label(
    header_top,
    text="Ask about internship domains, certificates, submission, support, fees, company details and services.",
    bg=HEADER_GRADIENT,
    fg="#dbeafe",
    font=("Arial", 10)
)
header_sub.pack(anchor="w", padx=20)

action_bar = tk.Frame(header_card, bg=CARD_BG)
action_bar.pack(fill="x", padx=16, pady=12)

clear_btn = tk.Button(
    action_bar,
    text="Clear Chat",
    bg=CLEAR_BTN,
    fg=WHITE,
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=14,
    pady=8,
    cursor="hand2",
    command=clear_chat
)
clear_btn.pack(side="left", padx=(0, 10))

export_btn = tk.Button(
    action_bar,
    text="Export Chat",
    bg=EXPORT_BTN,
    fg=WHITE,
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=14,
    pady=8,
    cursor="hand2",
    command=export_chat
)
export_btn.pack(side="left")

# Chat Card
chat_card = tk.Frame(right_panel, bg=CARD_BG)
chat_card.pack(fill="both", expand=True, pady=(0, 12))

chat_title = tk.Label(
    chat_card,
    text="Conversation",
    bg=CARD_BG,
    fg=TEXT_DARK,
    font=("Arial", 13, "bold")
)
chat_title.pack(anchor="w", padx=16, pady=(14, 8))

chat_container = tk.Frame(chat_card, bg=CHAT_BG)
chat_container.pack(fill="both", expand=True, padx=14, pady=(0, 14))

# Scrollable canvas for bubbles
canvas = tk.Canvas(chat_container, bg=CHAT_BG, highlightthickness=0)
scrollbar = tk.Scrollbar(chat_container, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

messages_frame = tk.Frame(canvas, bg=CHAT_BG)
canvas_window = canvas.create_window((0, 0), window=messages_frame, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_canvas_configure(event):
    canvas.itemconfig(canvas_window, width=event.width)

messages_frame.bind("<Configure>", on_frame_configure)
canvas.bind("<Configure>", on_canvas_configure)

# Input Card
input_card = tk.Frame(right_panel, bg=CARD_BG)
input_card.pack(fill="x")

input_label = tk.Label(
    input_card,
    text="Type your question",
    bg=CARD_BG,
    fg=TEXT_MUTED,
    font=("Arial", 10, "bold")
)
input_label.pack(anchor="w", padx=16, pady=(12, 4))

input_row = tk.Frame(input_card, bg=CARD_BG)
input_row.pack(fill="x", padx=14, pady=(0, 14))

user_input = tk.Entry(
    input_row,
    font=("Arial", 12),
    bd=0,
    relief="flat",
    bg="#f3f4f6",
    fg=TEXT_DARK,
    insertbackground=TEXT_DARK
)
user_input.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 10))

send_btn = tk.Button(
    input_row,
    text="Send",
    bg=SEND_BTN,
    fg=WHITE,
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=22,
    pady=11,
    cursor="hand2",
    command=send_message
)
send_btn.pack(side="right")

user_input.bind("<Return>", send_message)

# =========================================================
# LOAD OLD HISTORY / WELCOME
# =========================================================
loaded = load_chat_history()

if loaded:
    chat_history = loaded
    for item in chat_history:
        create_message_bubble(item["sender"], item["message"], item["time"])
else:
    add_bot_message(
        "Hello 👋 I’m your AI Internship & Student Helpdesk Assistant.\n\n"
        "I can help with:\n"
        "• internship domains\n"
        "• certificate\n"
        "• project submission\n"
        "• internship fee\n"
        "• company/services\n"
        "• support and working hours\n\n"
        "Use the topic panel on the left to browse FAQs or type your question below."
    )

root.mainloop()