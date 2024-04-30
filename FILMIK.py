import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s(%(lineno)d): %(asctime)s - %(levelname)s - %(message)s'
)
import tkinter
from tkinter import *
from tkinter import filedialog
from ImageViewer import ImageViewer


window = Tk()
window.title('FILMIK')
window.iconphoto(True, tkinter.PhotoImage(file="Icon/SLRicon.png"))
window.geometry("900x675")
window.configure(bg='black')


def load_folder():
    folder_path = filedialog.askdirectory()
    return folder_path

# 이미지 뷰어
viewer = ImageViewer(window)

# 하단 프레임
bottom_frame = Frame(master=window)
bottom_frame.pack(fill=BOTH, expand=True, padx=0, pady=0)

# pack Buttons
Button(master=bottom_frame, text='이전', command=viewer.prev_image).pack(side=LEFT, padx=0, pady=0)
Button(master=bottom_frame, text='다음', command=viewer.next_image).pack(side=LEFT, padx=0, pady=0)

# 밝기 조절 버튼
Button(master=bottom_frame, text='밝기 높이기', command=viewer.brighten_image).pack(side=RIGHT, padx=0, pady=0)
Button(master=bottom_frame, text='밝기 낯추기', command=viewer.darken_image).pack(side=RIGHT, padx=0, pady=0)

# 대비 조절 버튼
Button(master=bottom_frame, text='대비 높이기', command=viewer.increase_contrast).pack(side=RIGHT, padx=0, pady=0)
Button(master=bottom_frame, text='대비 낮추기', command=viewer.decrease_contrast).pack(side=RIGHT, padx=0, pady=0)

# 회전 버튼
Button(master=bottom_frame, text='시계 방향으로 회전', command=lambda: viewer.rotate_image(90)).pack(side=RIGHT, padx=0, pady=0)
Button(master=bottom_frame, text='반시계 방향으로 회전', command=lambda: viewer.rotate_image(-90)).pack(side=RIGHT, padx=0, pady=0)


top_menu = Menu()

menu_File = Menu(master=top_menu, tearoff=False)
menu_File.add_command(label='Open', accelerator='Ctrl+O', command=viewer.open_file)
menu_File.add_command(label='Open Folder', accelerator='Ctrl+Shift+F', command=viewer.open_folder)
menu_File.add_separator()
menu_File.add_command(label='Save', accelerator='Ctrl+S', command=viewer.save_image)
menu_File.add_command(label='Save as ...', accelerator='Ctrl+Shift+S', command=viewer.save_image_as)
menu_File.add_separator()
menu_File.add_command(label='Quit', accelerator='Ctrl+Q', command=window.quit)


menu_View = Menu(master=top_menu, tearoff=False)


top_menu.add_cascade(label='File', underline=True, menu=menu_File)

window.config(menu=top_menu)


# Press ESC key to QUIT.
window.bind('<Escape>', lambda e: window.quit())
window.mainloop()
