import tkinter as tk
from PIL import Image, ImageTk
import os

# Đường dẫn hình ảnh
bot_avt_path = os.path.join("media", "bot.png")
user_avt_path = os.path.join("media", "doremon.png")
send_icon_path = os.path.join("media", "sending.png")

# Hàm tạo tin nhắn dạng card
def create_message(frame, msg, side="left", avatar_path=bot_avt_path):
    card = tk.Frame(frame, bg="#f0f0f0", bd=1, relief="solid", padx=5, pady=5)
    
    try:
        avatar_img = Image.open(avatar_path).resize((32, 32))
    except Exception as e:
        print(f"Lỗi khi tải hình ảnh {avatar_path}: {e}")
        return
    
    avatar = ImageTk.PhotoImage(avatar_img)
    avatar_label = tk.Label(card, image=avatar, bg="#f0f0f0")
    avatar_label.image = avatar

    msg_label = tk.Label(card, text=msg, wraplength=200, justify="left", bg="#ffffff", anchor="w", padx=5, pady=5)
    
    if side == "left":
        card.pack(anchor="w", padx=10, pady=5, fill="x")
        avatar_label.pack(side="left")
        msg_label.pack(side="left", padx=5)
    else:
        card.pack(anchor="e", padx=(10, 0), pady=5, fill="x")  # Loại bỏ padding bên phải
        avatar_label.pack(side="right", padx=(5, 0))  # Loại bỏ padding bên phải của avatar
        msg_label.pack(side="right", padx=5, fill="x", expand=True)
    
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# Phản hồi bot
def get_response(user_input):
    responses = {
        "chào": "Chào bạn! Mình là chatbot đây.",
        "bạn tên gì": "Mình là chatbot viết bằng Tkinter.",
        "tạm biệt": "Hẹn gặp lại nhé!",
    }
    return responses.get(user_input.lower(), "Xin lỗi, mình chưa hiểu ý bạn.")

# Gửi tin nhắn
def send_message():
    user_input = entry.get()
    if user_input.strip() == "":
        return
    create_message(chat_frame, user_input, side="right", avatar_path=user_avt_path)
    response = get_response(user_input)
    create_message(chat_frame, response, side="left", avatar_path=bot_avt_path)
    entry.delete(0, tk.END)
    canvas.yview_moveto(1.0)

# Cửa sổ chính
root = tk.Tk()
root.title("Chatbot Card UI")
root.geometry("500x550")

# Frame chính để chứa canvas và bottom_frame
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Canvas có scrollbar
canvas = tk.Canvas(main_frame, bg="#ffffff")
scrollbar = tk.Scrollbar(main_frame, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

chat_frame = tk.Frame(canvas, bg="#ffffff")
canvas.create_window((0, 0), window=chat_frame, anchor="nw")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

chat_frame.bind("<Configure>", on_configure)

# Tin nhắn chào mặc định
create_message(chat_frame, "Chào bạn! Mình là chatbot đây.", side="left", avatar_path=bot_avt_path)

# Frame nhập tin nhắn + nút gửi
bottom_frame = tk.Frame(root, bg="#ffffff")
bottom_frame.pack(side="bottom", fill="x", padx=5, pady=5)

entry = tk.Entry(bottom_frame, font=("Arial", 12))
entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

# Nút gửi (sử dụng sending.png)
try:
    send_icon = Image.open(send_icon_path).resize((24, 24))
except Exception as e:
    print(f"Lỗi khi tải hình ảnh nút gửi: {e}")
    send_icon = None

if send_icon:
    send_icon_tk = ImageTk.PhotoImage(send_icon)
    send_button = tk.Button(bottom_frame, image=send_icon_tk, command=send_message)
    send_button.image = send_icon_tk
else:
    send_button = tk.Button(bottom_frame, text="Gửi", command=send_message)
send_button.pack(side="right")

# Bắt Enter
root.bind('<Return>', lambda event: send_message())

root.mainloop()