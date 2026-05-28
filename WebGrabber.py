import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO

# ===================== 版本 & 版权信息 =====================
VERSION = "v1.0.1 Beta版"
AUTHOR_ID = "©️JohnJHZhang"
CONTACT = "E-mail：johnjhzhang@outlook.com"

# ===================== 5国语言配置（默认简体中文） =====================
LANG = {
    "zh-CN": {
        "title": "网页内容抓取工具",
        "url": "输入网址：",
        "fetch": "抓取内容",
        "lang": "语言：",
        "theme": "切换深色模式",
        "save_dir": "选择保存文件夹",
        "download_text": "下载文字",
        "download_img": "下载选中图片",
        "text_preview": "文字预览",
        "img_preview": "图片预览",
        "select_all": "全选/取消全选",
        "no_dir": "请先选择保存文件夹！",
        "no_text": "未抓取到文字内容",
        "no_img": "未抓取到有效图片",
        "no_select": "未选择任何图片！",
        "success": "抓取完成！",
        "error": "抓取失败："
    },
    "zh-TW": {
        "title": "網頁內容擷取工具",
        "url": "輸入網址：",
        "fetch": "擷取內容",
        "lang": "語言：",
        "theme": "切換深色模式",
        "save_dir": "選擇儲存資料夾",
        "download_text": "下載文字",
        "download_img": "下載選取圖片",
        "text_preview": "文字預覽",
        "img_preview": "圖片預覽",
        "select_all": "全選/取消全選",
        "no_dir": "請先選擇儲存資料夾！",
        "no_text": "未擷取到文字內容",
        "no_img": "未擷取到有效圖片",
        "no_select": "未選擇任何圖片！",
        "success": "擷取完成！",
        "error": "擷取失敗："
    },
    "en": {
        "title": "Web Content Grabber",
        "url": "Enter URL:",
        "fetch": "Fetch Content",
        "lang": "Language:",
        "theme": "Dark Mode",
        "save_dir": "Select Save Folder",
        "download_text": "Download Text",
        "download_img": "Download Selected",
        "text_preview": "Text Preview",
        "img_preview": "Image Preview",
        "select_all": "Select All",
        "no_dir": "Please select a save folder first!",
        "no_text": "No text content found",
        "no_img": "No valid images found",
        "no_select": "No images selected!",
        "success": "Fetch Success!",
        "error": "Fetch failed: "
    },
    "ja": {
        "title": "Webコンテンツグラバー",
        "url": "URL入力：",
        "fetch": "コンテンツ取得",
        "lang": "言語：",
        "theme": "ダークモード",
        "save_dir": "保存フォルダ選択",
        "download_text": "テキスト保存",
        "download_img": "選択した画像を保存",
        "text_preview": "テキストプレビュー",
        "img_preview": "画像プレビュー",
        "select_all": "すべて選択",
        "no_dir": "最初に保存フォルダを選択してください！",
        "no_text": "テキストが見つかりません",
        "no_img": "有効な画像が見つかりません",
        "no_select": "画像が選択されていません！",
        "success": "取得完了！",
        "error": "取得に失敗しました："
    },
    "ko": {
        "title": "웹 콘텐츠 그래버",
        "url": "URL 입력:",
        "fetch": "콘텐츠 가져오기",
        "lang": "언어:",
        "theme": "다크 모드",
        "save_dir": "저장 폴더 선택",
        "download_text": "텍스트 다운로드",
        "download_img": "선택한 이미지 다운로드",
        "text_preview": "텍스트 미리보기",
        "img_preview": "이미지 미리보기",
        "select_all": "전체 선택",
        "no_dir": "먼저 저장 폴더를 선택하세요!",
        "no_text": "텍스트 내용이 없습니다",
        "no_img": "유효한 이미지가 없습니다",
        "no_select": "이미지를 선택하지 않았습니다!",
        "success": "가져오기 완료!",
        "error": "가져오기 실패："
    }
}

# ===================== 主程序 =====================
class WebGrabberApp:
    def __init__(self, root):
        self.root = root
        self.root.title(LANG["zh-CN"]["title"])
        self.root.geometry("900x750")
        # 支持窗口拖动放大/缩小
        self.root.resizable(True, True)

        # 全局变量
        self.current_lang = "zh-CN"
        self.is_dark = False
        self.save_path = None
        self.web_text = ""
        self.web_images = []
        self.image_checkboxes = []
        self.image_vars = []
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

        # 版权&版本控件
        self.version_label = None
        self.author_label = None
        self.contact_label = None

        self.init_ui()
        self.set_light_theme()

    # ===================== 主题设置（适配版本、版权、邮箱文字颜色） =====================
    def set_light_theme(self):
        self.root.configure(bg="white")
        ctk.set_appearance_mode("light")
        text_color = "#666666"
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color="black", bg_color="white")
            elif isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color="white", border_color="#cccccc")
            elif isinstance(widget, ctk.CTkTextbox):
                widget.configure(fg_color="white", text_color="black")
            elif isinstance(widget, ctk.CTkScrollableFrame):
                widget.configure(fg_color="white")
        # 底部版权文字 - 浅色模式灰色
        if self.version_label:
            self.version_label.configure(text_color=text_color, bg_color="white")
        if self.author_label:
            self.author_label.configure(text_color=text_color, bg_color="white")
        if self.contact_label:
            self.contact_label.configure(text_color=text_color, bg_color="white")
        self.is_dark = False

    def set_dark_theme(self):
        self.root.configure(bg="black")
        ctk.set_appearance_mode("dark")
        text_color = "#00ff00"
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color="#00ff00", bg_color="black")
            elif isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color="black", border_color="#333333")
            elif isinstance(widget, ctk.CTkTextbox):
                widget.configure(fg_color="black", text_color="#00ff00")
            elif isinstance(widget, ctk.CTkScrollableFrame):
                widget.configure(fg_color="black")
        # 底部版权文字 - 深色模式绿色
        if self.version_label:
            self.version_label.configure(text_color=text_color, bg_color="black")
        if self.author_label:
            self.author_label.configure(text_color=text_color, bg_color="black")
        if self.contact_label:
            self.contact_label.configure(text_color=text_color, bg_color="black")
        self.is_dark = True

    def toggle_theme(self):
        self.set_dark_theme() if not self.is_dark else self.set_light_theme()

    # ===================== 语言切换 =====================
    def change_language(self, choice):
        self.current_lang = choice
        self.root.title(LANG[choice]["title"])
        self.url_label.configure(text=LANG[choice]["url"])
        self.fetch_btn.configure(text=LANG[choice]["fetch"])
        self.lang_label.configure(text=LANG[choice]["lang"])
        self.theme_switch.configure(text=LANG[choice]["theme"])
        self.dir_btn.configure(text=LANG[choice]["save_dir"])
        self.select_all_check.configure(text=LANG[choice]["select_all"])
        self.download_text_btn.configure(text=LANG[choice]["download_text"])
        self.download_img_btn.configure(text=LANG[choice]["download_img"])

    # ===================== 全选/取消全选 =====================
    def toggle_select_all(self):
        is_select = self.select_all_var.get()
        for var in self.image_vars:
            var.set(is_select)

    # ===================== 抓取内容 =====================
    def fetch_content(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("提示", "请输入网址")
            return

        try:
            response = requests.get(url, headers=self.headers, verify=True, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # 提取文字
            self.web_text = soup.get_text(strip=True, separator="\n")
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, self.web_text)

            # 提取图片
            self.web_images = []
            for img in soup.find_all("img"):
                src = img.get("src", "").strip()
                if src.startswith("data:image/"):
                    continue
                full_url = urljoin(url, src)
                self.web_images.append(full_url)

            self.load_image_preview()
            messagebox.showinfo("成功", LANG[self.current_lang]["success"])

        except Exception as e:
            messagebox.showerror("错误", LANG[self.current_lang]["error"] + str(e))

    # ===================== 图片预览（统一布局，无遮挡） =====================
    def load_image_preview(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.image_checkboxes.clear()
        self.image_vars.clear()

        row, col = 0, 0
        max_col = 4

        for img_url in self.web_images:
            try:
                img_response = requests.get(img_url, headers=self.headers, verify=True, timeout=3)
                image_data = BytesIO(img_response.content)
                img = Image.open(image_data)
                img.thumbnail((120, 120))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 120))

                # 统一容器，无遮挡布局
                item_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
                item_frame.grid(row=row, column=col, padx=8, pady=8)

                img_label = ctk.CTkLabel(item_frame, image=ctk_img, text="")
                img_label.image = ctk_img
                img_label.pack(pady=2)

                var = tk.IntVar(value=1)
                self.image_vars.append(var)
                check = ctk.CTkCheckBox(item_frame, variable=var, text="")
                check.pack(pady=2)
                self.image_checkboxes.append(check)

                col += 1
                if col >= max_col:
                    col = 0
                    row += 1
            except Exception:
                continue

    # ===================== 下载文字 =====================
    def download_text(self):
        if not self.save_path:
            messagebox.showwarning("提示", LANG[self.current_lang]["no_dir"])
            return
        if not self.web_text:
            messagebox.showwarning("提示", LANG[self.current_lang]["no_text"])
            return

        file_path = os.path.join(self.save_path, "网页文字.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.web_text)
        messagebox.showinfo("成功", "文字已保存为 网页文字.txt")

    # ===================== 下载选中图片 =====================
    def download_selected_images(self):
        if not self.save_path:
            messagebox.showwarning("提示", LANG[self.current_lang]["no_dir"])
            return
        if not self.web_images:
            messagebox.showwarning("提示", LANG[self.current_lang]["no_img"])
            return

        selected_indices = [i for i, var in enumerate(self.image_vars) if var.get() == 1]
        if not selected_indices:
            messagebox.showwarning("提示", LANG[self.current_lang]["no_select"])
            return

        for idx in selected_indices:
            try:
                img_url = self.web_images[idx]
                ext = os.path.splitext(img_url)[-1] or ".jpg"
                img_name = f"图片_{idx+1}{ext}"
                img_path = os.path.join(self.save_path, img_name)

                img_data = requests.get(img_url, headers=self.headers, verify=True, timeout=5).content
                with open(img_path, "wb") as f:
                    f.write(img_data)
            except Exception:
                continue

        messagebox.showinfo("成功", f"已下载 {len(selected_indices)} 张选中图片！")

    # ===================== 选择文件夹 =====================
    def select_folder(self):
        self.save_path = filedialog.askdirectory()
        if self.save_path:
            self.dir_label.configure(text=self.save_path)

    # ===================== UI布局（新版局：版本/版权/邮箱在按钮下方右下角） =====================
    def init_ui(self):
        # 顶部框架
        top_frame = ctk.CTkFrame(self.root)
        top_frame.pack(fill=tk.X, padx=20, pady=10)

        self.url_label = ctk.CTkLabel(top_frame, text=LANG[self.current_lang]["url"])
        self.url_label.grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.url_entry = ctk.CTkEntry(top_frame)
        self.url_entry.grid(row=0, column=1, padx=5, pady=8, sticky="ew")
        top_frame.columnconfigure(1, weight=1)

        self.fetch_btn = ctk.CTkButton(top_frame, text=LANG[self.current_lang]["fetch"],
                                       fg_color="#007aff", text_color="white", command=self.fetch_content)
        self.fetch_btn.grid(row=0, column=2, padx=10, pady=8)

        self.lang_label = ctk.CTkLabel(top_frame, text=LANG[self.current_lang]["lang"])
        self.lang_label.grid(row=1, column=0, padx=5, pady=8, sticky="w")
        lang_options = ["zh-CN", "zh-TW", "en", "ja", "ko"]
        self.lang_menu = ctk.CTkOptionMenu(top_frame, values=lang_options, command=self.change_language)
        self.lang_menu.set("zh-CN")
        self.lang_menu.grid(row=1, column=1, padx=5, pady=8, sticky="w")

        self.theme_switch = ctk.CTkSwitch(top_frame, text=LANG[self.current_lang]["theme"], command=self.toggle_theme)
        self.theme_switch.grid(row=1, column=2, padx=10, pady=8)

        # 标签页（自适应缩放，文字/图片布局完全一致）
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        tab_text = self.tabview.add(LANG[self.current_lang]["text_preview"])
        tab_img = self.tabview.add(LANG[self.current_lang]["img_preview"])

        # 文字预览页
        self.text_box = ctk.CTkTextbox(tab_text, wrap=tk.WORD)
        self.text_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.download_text_btn = ctk.CTkButton(tab_text, text=LANG[self.current_lang]["download_text"],
                                              fg_color="#007aff", text_color="white", command=self.download_text)
        self.download_text_btn.pack(pady=8)

        # 图片预览页
        self.select_all_var = tk.IntVar(value=1)
        self.select_all_check = ctk.CTkCheckBox(tab_img, text=LANG[self.current_lang]["select_all"],
                                                variable=self.select_all_var, command=self.toggle_select_all)
        self.select_all_check.pack(anchor="w", padx=10, pady=5)

        self.scroll_frame = ctk.CTkScrollableFrame(tab_img)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.download_img_btn = ctk.CTkButton(tab_img, text=LANG[self.current_lang]["download_img"],
                                             fg_color="#007aff", text_color="white", command=self.download_selected_images)
        self.download_img_btn.pack(pady=8)

        # ===================== 底部主框架（分两行布局） =====================
        bottom_frame = ctk.CTkFrame(self.root)
        bottom_frame.pack(fill=tk.X, padx=20, pady=5)
        bottom_frame.columnconfigure(0, weight=1)

        # 第一行：选择文件夹按钮 + 路径标签
        self.dir_btn = ctk.CTkButton(bottom_frame, text=LANG[self.current_lang]["save_dir"],
                                     fg_color="#007aff", text_color="white", command=self.select_folder)
        self.dir_btn.grid(row=0, column=0, sticky="w", padx=10, pady=8)

        self.dir_label = ctk.CTkLabel(bottom_frame, text="未选择保存文件夹")
        self.dir_label.grid(row=0, column=0, sticky="w", padx=200, pady=8)

        # 第二行：版本号 + 版权ID + 联系方式（右下角，按钮正下方）
        self.version_label = ctk.CTkLabel(bottom_frame, text=VERSION, font=("Arial", 9))
        self.version_label.grid(row=1, column=0, sticky="e", padx=10, pady=2)

        self.author_label = ctk.CTkLabel(bottom_frame, text=AUTHOR_ID, font=("Arial", 9))
        self.author_label.grid(row=2, column=0, sticky="e", padx=10, pady=2)

        self.contact_label = ctk.CTkLabel(bottom_frame, text=CONTACT, font=("Arial", 9))
        self.contact_label.grid(row=3, column=0, sticky="e", padx=10, pady=2)

if __name__ == "__main__":
    root = ctk.CTk()
    app = WebGrabberApp(root)
    root.mainloop()
