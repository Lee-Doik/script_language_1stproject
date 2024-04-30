import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s(%(lineno)d): %(asctime)s - %(levelname)s - %(message)s'
)
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from logging import info as info
from PIL import Image, ImageTk, ImageEnhance
import os


class ImageViewer:
    def __init__(self, master):
        self.master = master
        self.bottom_frame = Frame(master=master)
        self.bottom_frame.pack(fill=BOTH, expand=True, padx=0, pady=0)
        self.folder = "Images"
        self.files = os.listdir("Images")
        self.index = 0
        self.angle = 0
        self.rotation_center = (0, 0)  # 회전 중심점 초기값
        self.favorite_folder = None  # 즐겨찾기 폴더 경로를 저장할 변수 추가
        self.btn_favorite_folder = Button(master=self.bottom_frame, text='즐겨찾기 폴더 지정', command=self.set_favorite_folder)
        self.btn_favorite_folder.pack(side=LEFT, padx=5, pady=5)
        # 현재 이미지를 즐겨찾기 폴더에 저장하는 버튼
        self.btn_save_to_favorite = Button(master=self.bottom_frame, text='즐겨찾기 폴더에 저장',
                                           command=self.save_to_favorite_folder)
        self.btn_save_to_favorite.pack(side=LEFT, padx=5, pady=5)
        self.drag_data = {'x': 0, 'y': 0, 'item': None}

        self.canvas = Canvas(master, width=800, height=600, highlightthickness=0)
        self.canvas.pack()

        self.show_image()

        self.master.bind('<Left>', self.prev_image)
        self.master.bind('<Right>', self.next_image)
        self.master.bind('<MouseWheel>', self.zoom)
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)

    def load_folder(self, folder):
        self.folder = folder
        self.files = os.listdir(folder)
        self.index = 0
        self.show_image()

    # 이미지 보여주기
    def show_image(self):
        self.image = Image.open(os.path.join(self.folder, self.files[self.index]))
        self.image = self.image.resize((800, 600), Image.Resampling.LANCZOS)
        self.rotation_center = (self.image.width // 2, self.image.height // 2)  # 회전 중심점 업데이트
        self.update_display()

    def update_display(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.delete("all")
        self.canvas.create_image(self.rotation_center[0], self.rotation_center[1], image=self.tk_image, anchor='center')

    # 다음 이미지 불러오기
    def next_image(self, event=None):
        info("다음 이미지")
        self.index = (self.index + 1) % len(self.files)
        self.show_image()

    # 이전 이미지 불러오기
    def prev_image(self, event=None):
        info("이전 이미지")
        self.index = (self.index - 1) % len(self.files)
        self.show_image()

    # 이미지 확대/축소

    def zoom(self, event):
        x = self.image.width
        y = self.image.height
        if event.delta > 0:
            info('줌 인')
            self.image = self.image.resize((int(x * 1.1), int(y * 1.1)), Image.Resampling.LANCZOS)
        else:
            info('줌 아웃')
            self.image = self.image.resize((int(x * 0.9), int(y * 0.9)), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_image, anchor='nw')

    def on_click(self, event):
        # 이미지 클릭 이벤트 핸들러
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            self.drag_data['item'] = item[0]
            self.drag_data['x'] = event.x
            self.drag_data['y'] = event.y

    def on_drag(self, event):
        # 이미지 드래그 이벤트 핸들러
        if self.drag_data['item']:
            x, y = event.x, event.y
            self.canvas.move(self.drag_data['item'], x - self.drag_data['x'], y - self.drag_data['y'])
            self.drag_data['x'] = x
            self.drag_data['y'] = y

    def brighten_image(self):
        info('이미지 밝기 높이기')
        self.image = self.image.point(lambda p: p * 1.1)
        self.update_display()

    def darken_image(self):
        info('이미지 밝기 낮추기')
        self.image = self.image.point(lambda p: p * 0.9)
        self.update_display()

    def adjust_contrast(self, factor):
        info('이미지 대비 조절')
        self.image = ImageEnhance.Contrast(self.image).enhance(factor)
        self.update_display()

    def increase_contrast(self):
        self.adjust_contrast(1.2)

    def decrease_contrast(self):
        self.adjust_contrast(0.8)

    def rotate_image(self, angle):
        info('이미지 회전')
        self.angle += angle
        rotated_image = self.image.rotate(self.angle, expand=True)  # 회전된 이미지 생성
        self.image = rotated_image
        self.update_display()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            self.folder = os.path.dirname(file_path)
            self.files = [os.path.basename(file_path)]
            self.index = 0
            self.show_image()

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.load_folder(folder_path)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("저장 완료", f"사진이 {file_path} 에 저장되었습니다.")

    def save_image_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("저장 완료", f"사진이 {file_path} 에 저장되었습니다.")

    def set_favorite_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.favorite_folder = folder_path
            messagebox.showinfo("즐겨찾기 폴더 설정", f"즐겨찾기 폴더가 {folder_path}로 설정되었습니다.")

    def save_to_favorite_folder(self):
        if self.favorite_folder:
            file_name = os.path.basename(self.files[self.index])
            target_path = os.path.join(self.favorite_folder, file_name)
            self.image.save(target_path)
            messagebox.showinfo("저장 완료", f"{file_name}이(가) 즐겨찾기 폴더에 저장되었습니다.")
        else:
            messagebox.showwarning("즐겨찾기 폴더 미지정", "즐겨찾기 폴더가 지정되지 않았습니다. 먼저 폴더를 지정해주세요.")
