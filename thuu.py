import re
import tkinter as tk
from tkinter import messagebox, simpledialog

# Dictionary to store scores
scores = {"Câu 1": None, "Câu 2": None, "Câu 3": None}

# Validate password
def validate_password(password):
    if not password.strip():
        return "⚠️ Mật khẩu không được để trống."
    if " " in password:
        return "⚠️ Mật khẩu không được chứa khoảng trắng."
    if not (8 <= len(password) <= 12):
        return "⚠️ Mật khẩu phải có độ dài từ 8 đến 12 ký tự."
    if not re.search("[a-z]", password):
        return "⚠️ Mật khẩu phải có ít nhất 1 chữ cái viết thường."
    if not re.search("[A-Z]", password):
        return "⚠️ Mật khẩu phải có ít nhất 1 chữ cái viết hoa."
    if not re.search("[0-9]", password):
        return "⚠️ Mật khẩu phải có ít nhất 1 số."
    if not re.search("[$#@]", password):
        return "⚠️ Mật khẩu phải có ít nhất 1 ký tự đặc biệt ($, #, @)."
    if not re.match(r'^[a-zA-Z0-9$#@]+$', password):
        return "⚠️ Mật khẩu chứa ký tự không hợp lệ."
    return None

# Question 1: Password validation
def check_password():
    while True:
        input_passwords = password_entry.get().strip()
        if not input_passwords:
            messagebox.showerror("Lỗi", "⚠️ Danh sách mật khẩu không được để trống.")
            return

        passwords = input_passwords.split(";")
        valid_passwords = []
        invalid_passwords = []

        for password in passwords:
            error = validate_password(password)
            if error:
                invalid_passwords.append(f"❌ '{password}': {error}")
            else:
                valid_passwords.append(f"✅ {password}")

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "📜 Danh sách mật khẩu hợp lệ:\n")
        result_text.insert(tk.END, "\n".join(valid_passwords) if valid_passwords else "Không có mật khẩu hợp lệ.")
        if invalid_passwords:
            result_text.insert(tk.END, "\n\n⚠️ Danh sách mật khẩu không hợp lệ:\n")
            result_text.insert(tk.END, "\n".join(invalid_passwords))
            messagebox.showwarning("Lỗi", "⚠️ Có mật khẩu không hợp lệ, vui lòng sửa lại danh sách.")
            return

        messagebox.showinfo("Thành công", "✅ Tất cả mật khẩu đều hợp lệ.")
        return True

# Question 2: Caesar Cipher Encryption
def caesar_cipher_encrypt(message, shift):
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            encrypted_message += chr((ord(char) - base + shift) % 26 + base)
        elif char.isdigit():
            base = ord('0')
            encrypted_message += chr((ord(char) - base + shift) % 10 + base)
        elif 32 <= ord(char) <= 126:
            base = 32
            encrypted_message += chr((ord(char) - base + shift) % (126 - 32 + 1) + base)
        else:
            encrypted_message += char
    return encrypted_message

def encrypt_message():
    while True:
        message = cipher_message_entry.get().strip()
        if not message:
            messagebox.showerror("Lỗi", "⚠️ Thông điệp không được để trống.")
            return

        try:
            shift = int(cipher_shift_entry.get())
        except ValueError:
            messagebox.showerror("Lỗi", "⚠️ Vui lòng nhập một số nguyên hợp lệ.")
            return

        encrypted_message = caesar_cipher_encrypt(message, shift)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"🔑 Thông điệp sau khi mã hóa: {encrypted_message}")
        messagebox.showinfo("Thành công", "✅ Thông điệp đã được mã hóa.")
        return True

# Question 3: Calculate an expression
def calculate_expression():
    while True:
        expression = expression_entry.get().strip()
        if not expression:
            messagebox.showerror("Lỗi", "⚠️ Biểu thức không được để trống.")
            return

        if not re.match(r'^[\d\s+\-*/().]+$', expression):
            messagebox.showerror("Lỗi", "⚠️ Biểu thức chứa ký tự không hợp lệ.")
            return

        try:
            result = eval(expression)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"🧮 Kết quả của biểu thức: {result}")
            messagebox.showinfo("Thành công", "✅ Biểu thức đã được tính toán.")
            return True
        except ZeroDivisionError:
            messagebox.showerror("Lỗi", "⚠️ Lỗi: Không thể chia cho 0.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"⚠️ Lỗi: {e}")

# View the final report
def view_report():
    report = "\n📋 KẾT QUẢ CHẤM ĐIỂM:\n"
    print(f"Mã số sinh viên: 14227371980980")
    print(f"Họ và tên: Tran Loi")
    for question, score in scores.items():
        report += f"- {question}: {score if score is not None else 'Chưa chấm'}\n"
    total_score = sum(score for score in scores.values() if score is not None)
    report += f"\n🎯 Tổng điểm: {total_score}\n"
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, report)

# Grading a specific question
def grade_question(question):
    valid = None
    if question == "Câu 1":
        valid = check_password()
    elif question == "Câu 2":
        valid = encrypt_message()
    elif question == "Câu 3":
        valid = calculate_expression()

    if valid:
        while True:
            try:
                score = simpledialog.askfloat("Nhập điểm", f"Nhập điểm cho {question} (0-10):", minvalue=0, maxvalue=10)
                if score is None:
                    messagebox.showerror("Lỗi", "⚠️ Bạn phải nhập điểm để tiếp tục.")
                else:
                    scores[question] = score
                    messagebox.showinfo("Điểm", f"✅ Bạn đã chấm điểm {question}: {score}")
                    break
            except ValueError:
                messagebox.showerror("Lỗi", "⚠️ Điểm nhập không hợp lệ. Vui lòng nhập lại.")

# Tkinter GUI setup
root = tk.Tk()
root.title("Ứng dụng chấm điểm")

# Password check section
password_frame = tk.LabelFrame(root, text="Câu 1: Kiểm tra mật khẩu", padx=10, pady=10)
password_frame.pack(fill="both", expand="yes", padx=10, pady=10)
tk.Label(password_frame, text="Nhập danh sách mật khẩu (ngăn cách bằng dấu chấm phẩy):").pack()
password_entry = tk.Entry(password_frame, width=50)
password_entry.pack(pady=5)
tk.Button(password_frame, text="Kiểm tra mật khẩu", command=lambda: grade_question("Câu 1")).pack()

# Caesar cipher section
cipher_frame = tk.LabelFrame(root, text="Câu 2: Mã hóa thông điệp", padx=10, pady=10)
cipher_frame.pack(fill="both", expand="yes", padx=10, pady=10)
tk.Label(cipher_frame, text="Nhập thông điệp cần mã hóa:").pack()
cipher_message_entry = tk.Entry(cipher_frame, width=50)
cipher_message_entry.pack(pady=5)
tk.Label(cipher_frame, text="Nhập độ dịch chuyển:").pack()
cipher_shift_entry = tk.Entry(cipher_frame, width=20)
cipher_shift_entry.pack(pady=5)
tk.Button(cipher_frame, text="Mã hóa thông điệp", command=lambda: grade_question("Câu 2")).pack()

# Expression calculator section
expression_frame = tk.LabelFrame(root, text="Câu 3: Tính toán biểu thức", padx=10, pady=10)
expression_frame.pack(fill="both", expand="yes", padx=10, pady=10)
tk.Label(expression_frame, text="Nhập biểu thức cần tính:").pack()
expression_entry = tk.Entry(expression_frame, width=50)
expression_entry.pack(pady=5)
tk.Button(expression_frame, text="Tính toán biểu thức", command=lambda: grade_question("Câu 3")).pack()

# Result section
result_frame = tk.LabelFrame(root, text="Kết quả", padx=10, pady=10)
result_frame.pack(fill="both", expand="yes", padx=10, pady=10)
result_text = tk.Text(result_frame, height=10, width=70)
result_text.pack()

# Report Button
tk.Button(root, text="Xem báo cáo", command=view_report).pack(pady=10)

# Run the GUI
root.mainloop()

