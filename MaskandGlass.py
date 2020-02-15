"""
在CSDN上看到“不脱发的程序猿"的文章《基于Python的人脸自动戴口罩系统》
https://blog.csdn.net/m0_38106923/article/details/104174562

里面介绍了怎么利用Dlib模块的landmark人脸68个关键点识别人脸五官数据，从而实现带口罩。
本文是在作者的基础上，增加了添加眼镜的部分。


"
"""

# _*_ coding:utf-8 _*_


from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import cv2
import tkinter as tk
import PIL
import dlib


class AddMask(object):
    
    # 设计对话框
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('基于Pyhon的人脸自动戴口罩系统')
        self.root.geometry('1200x500')

        self.path1_ = None
        self.path2_ = None
        self.seg_img_path = None
        self.mask = None
        self.glass=None
        self.label_Img_seg = None

        decoration = PIL.Image.open('C:/Achillesccj/Work/AI/MaskandGlass/pic/bg.png').resize((1200, 500))
        render = ImageTk.PhotoImage(decoration)
        img = tk.Label(image=render)
        img.image = render
        img.place(x=0, y=0)

        # 原图1的展示
        tk.Button(self.root, text="打开头像", command=self.show_original1_pic).place(x=50, y=120)
      #  tk.Button(self.root, text="退出软件", command=quit).place(x=900, y=40)

        tk.Label(self.root, text="头像", font=10).place(x=280, y=120)
        self.cv_orinial1 = tk.Canvas(self.root, bg='white', width=270, height=270)
        self.cv_orinial1.create_rectangle(8, 8, 260, 260, width=1, outline='red')
        self.cv_orinial1.place(x=180, y=150)
        self.label_Img_original1 = tk.Label(self.root)
        self.label_Img_original1.place(x=180, y=150)

        tk.Label(self.root,text="选择口罩",font=8).place(x=550,y=120)
        tk.Label(self.root,text="选择眼镜",font=8).place(x=650,y=120)

        first_pic = Image.open("C:/Achillesccj/Work/AI/MaskandGlass/pic/Mask.png")
        first_pic = first_pic.resize((60, 60), Image.ANTIALIAS)
        first_pic = ImageTk.PhotoImage(first_pic)
        self.first = tk.Label(self.root, image=first_pic)
        self.first.place(x=550,y=160, width=60, height=60)
        self.first.bind("<Button-1>", self.mask0)

        second_pic = Image.open("C:/Achillesccj/Work/AI/MaskandGlass/pic/Mask1.png")
        second_pic = second_pic.resize((60, 60), Image.ANTIALIAS)
        second_pic = ImageTk.PhotoImage(second_pic)
        self.second_pic = tk.Label(self.root, image=second_pic)
        self.second_pic.place(x=550, y=230, width=60, height=60)
        self.second_pic.bind("<Button-1>", self.mask1)

        third_pic = Image.open("C:/Achillesccj/Work/AI/MaskandGlass/pic/Mask3.png")
        third_pic = third_pic.resize((60, 60), Image.ANTIALIAS)
        third_pic = ImageTk.PhotoImage(third_pic)
        self.third_pic = tk.Label(self.root, image=third_pic)
        self.third_pic.place(x=550, y=300, width=60, height=60)
        self.third_pic.bind("<Button-1>", self.mask3)

        forth_pic = Image.open("C:/Achillesccj/Work/AI/MaskandGlass/pic/Mask4.png")
        forth_pic = forth_pic.resize((60, 60), Image.ANTIALIAS)
        forth_pic = ImageTk.PhotoImage(forth_pic)
        self.forth_pic = tk.Label(self.root, image=forth_pic)
        self.forth_pic.place(x=550, y=370, width=60, height=60)
        self.forth_pic.bind("<Button-1>", self.mask4)
        
        first_glass = Image.open("C:/Achillesccj/Work/AI/MaskandGlass/pic/Glass1.png")
        first_glass = first_glass.resize((60, 60), Image.ANTIALIAS)
        first_glass = ImageTk.PhotoImage(first_glass)
        self.first_glass = tk.Label(self.root, image=first_glass)
        self.first_glass.place(x=650,y=160, width=60, height=60)
        self.first_glass.bind("<Button-1>", self.glass1)

        second_glass = Image.open("C:/Achillesccj/Work/AI/MaskandGlass/pic/Glass2.png")
        second_glass = second_glass.resize((60, 60), Image.ANTIALIAS)
        second_glass = ImageTk.PhotoImage(second_glass)
        self.second_glass = tk.Label(self.root, image=second_glass)
        self.second_glass.place(x=650, y=230, width=60, height=60)
        self.second_glass.bind("<Button-1>", self.glass2)

        third_glass = Image.open("C:/Achillesccj/Work/AI/MaskandGlass/pic/Glass3.png")
        third_glass = third_glass.resize((60, 60), Image.ANTIALIAS)
        third_glass = ImageTk.PhotoImage(third_glass)
        self.third_pic = tk.Label(self.root, image=third_glass)
        self.third_pic.place(x=650, y=300, width=60, height=60)
        self.third_pic.bind("<Button-1>", self.glass3)

        forth_glass = Image.open("C:/Achillesccj/Work/AI/MaskandGlass/pic/Glass4.png")
        forth_glass = forth_glass.resize((60, 60), Image.ANTIALIAS)
        forth_glass = ImageTk.PhotoImage(forth_glass)
        self.forth_glass = tk.Label(self.root, image=forth_glass)
        self.forth_glass.place(x=650, y=370, width=60, height=60)
        self.forth_glass.bind("<Button-1>", self.glass4)
        
        
        
        
        
        tk.Label(self.root, text="佩戴效果", font=10).place(x=920, y=120)
        self.cv_seg = tk.Canvas(self.root, bg='white', width=270, height=270)
        self.cv_seg.create_rectangle(8, 8, 260, 260, width=1, outline='red')
        self.cv_seg.place(x=820, y=150)
        self.label_Img_seg = tk.Label(self.root)
        self.label_Img_seg.place(x=820, y=150)

        self.root.mainloop()

    # 原图1展示
    def show_original1_pic(self):
        self.path1_ = askopenfilename(title='选择文件')
        print(self.path1_)
        self.Img = PIL.Image.open(r'{}'.format(self.path1_))
        Img = self.Img.resize((270,270),PIL.Image.ANTIALIAS)   # 调整图片大小至256x256
        img_png_original = ImageTk.PhotoImage(Img)
        #这边是做什么的
        
        self.label_Img_original1.config(image=img_png_original)
        self.label_Img_original1.image = img_png_original  # keep a reference
        self.cv_orinial1.create_image(5, 5,anchor='nw', image=img_png_original)

    # 人脸戴口罩效果展示
    def show_morpher_pic(self):
        #调取原图
        img1 = cv2.imread(self.path1_)
        #调取mouth的边缘数据
        x_min, x_max, y_min, y_max, size = self.get_mouth(img1)
        #基于位置信息，调整口罩大小
        adding = self.mask.resize(size)
        im = Image.fromarray(img1[:, :, ::-1])  # 切换RGB格式
        # 两幅图融合到一起
        im.paste(adding, (int(x_min), int(y_min)), adding)
        # im.show()
        save_path = self.path1_.split('.')[0]+'_result.jpg'
        im.save(save_path)
        Img = im.resize((270, 270), PIL.Image.ANTIALIAS)  # 调整图片大小至270x270
        img_png_seg = ImageTk.PhotoImage(Img)
        self.label_Img_seg.config(image=img_png_seg)
        self.label_Img_seg.image = img_png_seg  # keep a reference
        
     #带眼镜的照片   
    def show_glass_pic(self):
        #调取原图
        img1 = cv2.imread(self.path1_)
        #调取mouth的边缘数据
        x_min, x_max, y_min, y_max, size = self.get_eye(img1)
        #基于位置信息，调整口罩大小
        adding = self.glass.resize(size)
        im = Image.fromarray(img1[:, :, ::-1])  # 切换RGB格式
        # 两幅图融合到一起
        im.paste(adding, (int(x_min), int(y_min)), adding)
        # im.show()
        save_path = self.path1_.split('.')[0]+'_result.jpg'
        im.save(save_path)
        Img = im.resize((270, 270), PIL.Image.ANTIALIAS)  # 调整图片大小至270x270
        img_png_seg = ImageTk.PhotoImage(Img)
        self.label_Img_seg.config(image=img_png_seg)
        self.label_Img_seg.image = img_png_seg  # keep a reference

    def mask0(self, event):
        self.mask = Image.open('pic/mask.png')
        self.show_morpher_pic()

    def mask1(self, event):
        self.mask = Image.open('pic/mask1.png')
        self.show_morpher_pic()

    def mask3(self, event):
        self.mask = Image.open('pic/mask3.png')
        self.show_morpher_pic()

    def mask4(self, event):
        self.mask = Image.open('pic/mask4.png')
        self.show_morpher_pic()
        
        
    def glass1(self, event):
        self.glass = Image.open('pic/Glass1.png')
        self.show_glass_pic()

    def glass2(self, event):
        self.glass = Image.open('pic/Glass2.png')
        self.show_glass_pic()

    def glass3(self, event):
        self.glass = Image.open('pic/Glass3.png')
        self.show_glass_pic()

    def glass4(self, event):
        self.glass = Image.open('pic/Glass4.png')
        self.show_glass_pic()

    def get_mouth(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')
        faces = detector(img_gray, 0)
        for k, d in enumerate(faces):
            x = []
            y = []
            # 人脸大小的高度
            height = d.bottom() - d.top()
            # 人脸大小的宽度
            width = d.right() - d.left()
            shape = predictor(img_gray, d)
            # 48-67 为嘴唇部分
            for i in range(48, 68):
                x.append(shape.part(i).x)
                y.append(shape.part(i).y)
            # 根据人脸的大小扩大嘴唇对应口罩的区域
            y_max = (int)(max(y) + height / 3)
            y_min = (int)(min(y) - height / 3)
            x_max = (int)(max(x) + width / 3)
            x_min = (int)(min(x) - width / 3)
            size = ((x_max - x_min), (y_max - y_min))
            return x_min, x_max, y_min, y_max, size

    def get_eye(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')
        faces = detector(img_gray, 0)
        for k, d in enumerate(faces):
            x = []
            y = []
            # 人脸大小的高度
            height = d.bottom() - d.top()
            # 人脸大小的宽度
            width = d.right() - d.left()
            shape = predictor(img_gray, d)
            # 36-45 为眼睛部分
            for i in range(36, 45):
                x.append(shape.part(i).x)
                y.append(shape.part(i).y)
            # 根据眼睛的位置，经过适当扩展，得到眼镜的区域
            y_max = (int)(max(y) + height / 3)
            y_min = (int)(min(y) - height / 3)
            x_max = (int)(max(x) + width / 3)
            x_min = (int)(min(x) - width / 3)
            size = ((x_max - x_min), (y_max - y_min))
            return x_min, x_max, y_min, y_max, size

    def quit(self):
        self.root.destroy()



if __name__ == '__main__':
    AddMask()
