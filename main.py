"""测试一个经典的GUI程序的写法，使用面向对象的方式"""
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

class Application(Frame):
    """一个经典的GUI程序的类的写法"""
    def __init__(self, master=None):
        super().__init__(master)      #super()代表的是父类的定义，而不是父类对象
        self.master=master
        self.pack()
        self.image_path = StringVar()
        self.samples_path = StringVar()
        self.segmentation_path = StringVar()
        self.classification_path = StringVar()
        self.classification_method = StringVar()
        self.gpu_selection = StringVar()
        self.createWidget()
        
    def createWidget(self):
        """创建组件"""

        self.menubar = Menu(root)
        root.config(menu=self.menubar)
        self.menubar.add_command(label="Click", command=lambda:print("Hello"))   

        self.classification_method.set("DT")
        Radiobutton(root, text="决策树算法", variable=self.classification_method, value="DT").pack()
        Radiobutton(root, text="支持向量机算法", variable=self.classification_method, value="SVM").pack()
        Radiobutton(root, text="随机森林算法", variable=self.classification_method, value="RF").pack()

        self.gpu_selection.set("GPU")
        Radiobutton(root, text="GPU", variable=self.gpu_selection, value="GPU").pack()
        Radiobutton(root, text="CPU", variable=self.gpu_selection, value="CPU").pack()

        self.image_path_label = Label(root, text='选择图像文件：', font=('华文彩云', 15))
        self.image_path_label.place(x=50, y=80)
        self.image_path_label_entry = Entry(root, textvariable=self.image_path, font=('FangSong', 10), width=30, state='readonly')
        self.image_path_label_entry.place(x=190, y=85)

        self.segmentation_path_label = Label(root, text='选择分割文件：', font=('华文彩云', 15))
        self.segmentation_path_label.place(x=50, y=155)
        self.segmentation_path_label_entry = Entry(root, textvariable=self.segmentation_path, font=('FangSong', 10), width=30, state='readonly')
        self.segmentation_path_label_entry.place(x=190, y=160)

        self.samples_path_label = Label(root, text='选择样本文件：', font=('华文彩云', 15))
        self.samples_path_label.place(x=50, y=230)
        self.samples_path_label_entry = Entry(root, textvariable=self.samples_path, font=('FangSong', 10), width=30, state='readonly')
        self.samples_path_label_entry.place(x=190, y=235)

        self.classification_path_label = Label(root, text='选择分类文件：', font=('华文彩云', 15))
        self.classification_path_label.place(x=50, y=305)
        self.classification_path_label_entry = Entry(root, textvariable=self.classification_path, font=('FangSong', 10), width=30, state='readonly')
        self.classification_path_label_entry.place(x=190, y=310)

        self.classification_method_selection_label = Label(root, text='选择分类算法：', font=('华文彩云', 15))
        self.classification_method_selection_label.place(x=50, y=380)
        # self.classification_method_selection_label_entry = Entry(root, textvariable=self.image_path, font=('FangSong', 10), width=30, state='readonly')
        # self.classification_method_selection_label_entry.place(x=190, y=385)

        self.gpu_selection_label = Label(root, text='选择运算设备：', font=('华文彩云', 15))
        self.gpu_selection_label.place(x=50, y=455)
        # self.gpu_selection_label_entry = Entry(root, textvariable=self.image_path, font=('FangSong', 10), width=30, state='readonly')
        # self.gpu_selection_label_entry.place(x=190, y=460)

        self.segmentation_button = Button(self)
        self.segmentation_button["text"] = "分割"
        self.segmentation_button.pack()
        self.segmentation_button["command"] =self.segmentation

        self.classification_button = Button(self)
        self.classification_button["text"] = "分类"
        self.classification_button.pack()
        self.classification_button["command"] =self.classification

        self.image_file_button = Button(self, text='选择路径', command=self.image_load)
        self.image_file_button.pack()

        self.segmentation_file_button = Button(self, text='选择路径', command=self.segmentation_load)
        self.segmentation_file_button.pack()

        self.samples_file_button = Button(self, text='选择路径', command=self.samples_load)
        self.samples_file_button.pack()

        self.classification_file_button = Button(self, text='选择路径', command=self.classification_load)
        self.classification_file_button.pack()

        ## 这里是图片显示 这里估计要弄很久 你看着办
        # self.image_cv = Canvas(root, bg="white", highlightthickness=0)
        # self.image_cv.pack()
        # # image = PhotoImage(file=self.image_path)
        # # self.image_cv.create_image(500, 500, image=image)

        # self.segmentation_cv = Canvas(root, bg="white", highlightthickness=0)
        # self.segmentation_cv.pack()

        # self.classification_cv = Canvas(root, bg="white", highlightthickness=0)
        # self.classification_cv.pack()

        # 创建一个退出按钮
        self.quit_button= Button(self, text="退出", command=root.destroy)
        self.quit_button.pack()

    def segmentation(self):
        messagebox.showinfo("分割","开始分割")

    def classification(self):
        messagebox.showinfo("分类","开始分类")
    
    def image_load(self):
        filename = askopenfilename(filetypes=[("tif图像文件", "*.tif")])
        self.image_path.set(filename)

    def segmentation_load(self):
        filename = askopenfilename(filetypes=[("tif图像文件", "*.tif")])
        self.segmentation_path.set(filename)

    def samples_load(self):
        filename = askopenfilename(filetypes=[("tif图像文件", "*.tif")])
        self.samples_path.set(filename)

    def classification_load(self):
        filename = askopenfilename(filetypes=[("tif图像文件", "*.tif")])
        self.classification_path.set(filename)

root=Tk()
root.geometry("960x540")
root.title("一个经典的GUI程序类的测试")
root.resizable(False, False)
app = Application(master=root)

# 进度条
# bar = Progressbar(root, length=200, maximum=100, value=30)
# bar.pack(padx=10, pady=10)

root.mainloop()
print(app.image_path.get())