import tkinter as tk
from tkinter import scrolledtext, messagebox
from pycorrector import MacBertCorrector
import argparse
import csv
import os

class MacBertCorrectorApp:
    def __init__(self, root, output_dir):
        self.root = root
        self.root.title("Text Corrector")
        self.root.configure(bg="#F0F0F0")  # 设置背景颜色

        self.output_dir = output_dir
        self.corrector = MacBertCorrector(self.output_dir)

        self.create_widgets()

    def create_widgets(self):
        # 输入文本框
        self.input_label = tk.Label(self.root, text="输入文本:", font=("Arial", 12), bg="#F0F0F0")
        self.input_label.pack(pady=15)

        self.input_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=10, font=("Arial", 12))
        self.input_text.pack(pady=15)

        # 纠正按钮
        self.correct_button = tk.Button(self.root, text="纠正", command=self.correct_text, font=("Arial", 12), bg="#FFC107", fg="white")
        self.correct_button.pack(side=tk.LEFT, padx=15, pady=15)

        # 反馈按钮
        self.feedback_button = tk.Button(self.root, text="反馈", command=self.save_feedback, font=("Arial", 12), bg="#28a745", fg="white")
        self.feedback_button.pack(side=tk.RIGHT, padx=15, pady=15)

        # 输出文本框
        self.output_label = tk.Label(self.root, text="纠正后的文本:", font=("Arial", 12), bg="#F0F0F0")
        self.output_label.pack(pady=15)

        self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=10, font=("Arial", 12))
        self.output_text.pack(pady=15)

        # 详细错误信息框
        self.details_label = tk.Label(self.root, text="详细纠正信息:", font=("Arial", 12), bg="#F0F0F0")
        self.details_label.pack(pady=15)

        self.details_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=10, font=("Arial", 12))
        self.details_text.pack(pady=15)

    def correct_text(self):
        input_text = self.input_text.get("1.0", tk.END).strip()
        if input_text:
            result = self.corrector.correct(input_text, threshold=0.1)
            print(result)  # 打印返回值以调试
            corrected_text = result['target']
            details = result['errors']
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, corrected_text)
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert(tk.END, str(details))
            self.current_result = result

    def save_feedback(self):
        if hasattr(self, 'current_result'):
            feedback_dir = os.path.join(os.path.dirname(__file__), 'feedback')
            os.makedirs(feedback_dir, exist_ok=True)
            log_path = os.path.join(feedback_dir, 'log.csv')
            with open(log_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([self.current_result['source'], self.current_result['target'], self.current_result['errors']])
            print(f"Feedback saved to {log_path}")
            messagebox.showinfo("提示", "反馈已保存")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", default='E:\\pycorrector\\model\\macbert4csc-base-chinese', type=str, help="Dir for model.")
    args = parser.parse_args()

    root = tk.Tk()
    app = MacBertCorrectorApp(root, args.model_dir)
    root.mainloop()
