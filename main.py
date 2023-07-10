"""测试一个经典的GUI程序的写法,使用面向对象的方式"""
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename,asksaveasfilename

from GUI.GUI_Layout import *

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

        # 菜单栏（感觉没什么用
        # self.menubar = Menu(root)
        # root.config(menu=self.menubar)
        # self.menubar.add_command(label="Click", command=lambda:print("Hello"))   

        #--------- 选择文件的相关组件 ---------#
        # 4个文本框显示文件路径
        self.image_path_label = Label(root, text='输入图像文件：', font=('楷体',15),relief='ridge',padx=10,pady=10)
        self.image_path_label.place(x=0, y=0)
        self.image_path_label_entry = Entry(root, textvariable=self.image_path, font=('宋体', 11), width=50, 
                                            state='readonly',relief='sunken',bd=1)
        self.image_path_label_entry.place(x=195, y=6,height=37)
      

        self.segmentation_path_label = Label(root, text='输出分割文件：', font=('楷体', 15),relief='ridge',padx=10,pady=10)
        self.segmentation_path_label.place(x=0, y=60)
        self.segmentation_path_label_entry = Entry(root, textvariable=self.segmentation_path, font=('宋体', 11), width=50,
                                                   state='readonly',relief='sunken',bd=1)
        self.segmentation_path_label_entry.place(x=195, y=66,height=37)

        self.samples_path_label = Label(root, text='输入样本文件：', font=('楷体', 15),relief='ridge',padx=10,pady=10)
        self.samples_path_label.place(x=0, y=120)
        self.samples_path_label_entry = Entry(root, textvariable=self.samples_path, font=('宋体', 11), width=50, 
                                              state='readonly',relief='sunken',bd=1)
        self.samples_path_label_entry.place(x=195, y=126,height=37)

        self.classification_path_label = Label(root, text='输出分类文件：', font=('楷体', 15),relief='ridge',padx=10,pady=10)
        self.classification_path_label.place(x=0, y=180)
        self.classification_path_label_entry = Entry(root, textvariable=self.classification_path, font=('宋体', 11), width=50, 
                                                     state='readonly',relief='sunken',bd=1)
        self.classification_path_label_entry.place(x=195, y=186,height=37)

        # 4个Button选择文件路径
        # 鼠标悬停button时改变颜色（代码很丑，试了半天没办法把button对象当参数传进来
        def on_button1(e):
            self.image_file_button['bg']='#F3F3F3'
        def leave_button1(e):
            self.image_file_button['bg']='#ECECEC'     
        def on_button2(e):
            self.segmentation_file_button['bg']='#F3F3F3'
        def leave_button2(e):
            self.segmentation_file_button['bg']='#ECECEC'
        def on_button3(e):
            self.samples_file_button['bg']='#F3F3F3'
        def leave_button3(e):
            self.samples_file_button['bg']='#ECECEC'
        def on_button4(e):
            self.classification_file_button['bg']='#F3F3F3'
        def leave_button4(e):
            self.classification_file_button['bg']='#ECECEC'

        self.image_file_button = Button(root, text='选择路径', command=self.image_load,cursor='hand2',relief='raised',
                                        width=10,bg='#ECECEC',font=('华文彩云',12),activebackground='#D9D9D9')
        self.image_file_button.bind('<Enter>',on_button1)
        self.image_file_button.bind('<Leave>',leave_button1)
        self.image_file_button.pack()
        self.image_file_button.place(x=665,y=5)

        self.segmentation_file_button = Button(root, text='选择路径', command=self.segmentation_load,cursor='hand2',relief='raised',
                                        width=10,bg='#ECECEC',font=('华文彩云',12),activebackground='#D9D9D9')
        self.segmentation_file_button.bind('<Enter>',on_button2)
        self.segmentation_file_button.bind('<Leave>',leave_button2)
        self.segmentation_file_button.pack()
        self.segmentation_file_button.place(x=665,y=65)

        self.samples_file_button = Button(root, text='选择路径', command=self.samples_load,cursor='hand2',relief='raised',
                                        width=10,bg='#ECECEC',font=('华文彩云',12),activebackground='#D9D9D9')
        self.samples_file_button.bind('<Enter>',on_button3)
        self.samples_file_button.bind('<Leave>',leave_button3)
        self.samples_file_button.pack()
        self.samples_file_button.place(x=665,y=125)

        self.classification_file_button = Button(root, text='选择路径', command=self.classification_load,cursor='hand2',relief='raised',
                                        width=10,bg='#ECECEC',font=('华文彩云',12),activebackground='#D9D9D9')
        self.classification_file_button.bind('<Enter>',on_button4)
        self.classification_file_button.bind('<Leave>',leave_button4)
        self.classification_file_button.pack()
        self.classification_file_button.place(x=665,y=185)

        #--------- 模型运算设置的相关组件 ---------#
        self.classification_method_selection_label = Label(root, text='选择分类算法：',font=('楷体', 15),
                                                           relief='ridge',padx=10,pady=10)
        self.classification_method_selection_label.place(x=0, y=240)
       

        self.gpu_selection_label = Label(root, text='选择运算设备：', font=('楷体', 15),
                                         relief='ridge',padx=10,pady=10)
        self.gpu_selection_label.place(x=0, y=300)
      
    #   TODO
        def radioSelected1():
            DT_btn['font']=('黑体',12)

        self.classification_method.set("DT")
        DT_btn=Radiobutton(root, text="决策树", variable=self.classification_method, value="DT",
                           cursor='hand2',font=('宋体',12))
        # DT_btn.bind(<Click>,)
        DT_btn.pack()
        DT_btn.place(x=190,y=253)

        SVM_btn=Radiobutton(root, text="支持向量机", variable=self.classification_method, value="SVM",
                            cursor='hand2',font=('宋体',12))
        SVM_btn.pack()
        SVM_btn.place(x=290,y=253)

        RF_btn=Radiobutton(root, text="随机森林", variable=self.classification_method, value="RF",
                           cursor='hand2',font=('宋体',12))
        RF_btn.pack()
        RF_btn.place(x=432,y=253)

        self.gpu_selection.set("GPU")
        Radiobutton(root, text="GPU", variable=self.gpu_selection, value="GPU",cursor='hand2').pack()
        Radiobutton(root, text="CPU", variable=self.gpu_selection, value="CPU",cursor='hand2').pack()
        self.segmentation_button = Button(self,cursor='hand2')
        self.segmentation_button["text"] = "分割"
        self.segmentation_button.pack()
        self.segmentation_button["command"] =self.segmentation

        self.classification_button = Button(self)
        self.classification_button["text"] = "分类"
        self.classification_button.pack()
        self.classification_button["command"] =self.classification
        self.classification_button["cursor"] ='hand2'

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
        # 选择输出文件的路径并命名,filetypes参数后续可以根据具体情况更改
        filename = asksaveasfilename(defaultextension='.tif',filetypes=[('tif图像文件', '*.txt'), ('All Files', '*.*')]) 
        self.segmentation_path.set(filename)

    def samples_load(self):
        filename = askopenfilename(filetypes=[("tif图像文件", "*.tif")])
        self.samples_path.set(filename)

    def classification_load(self):
        filename = asksaveasfilename(defaultextension='.tif') 
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