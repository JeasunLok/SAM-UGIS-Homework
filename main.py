"""测试一个经典的GUI程序的写法,使用面向对象的方式"""
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename,asksaveasfilename
from  PIL  import  Image,ImageTk

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
         
        #--------- 选择文件的相关组件 ---------#
        # 4个文本框显示文件路径
        self.image_path_label = Label(root, text='输入图像文件：', font=('楷体',15),padx=10,pady=10)
        self.image_path_label.place(x=0, y=0)
        self.image_path_label_entry = Entry(root, textvariable=self.image_path, font=('宋体', 11), width=50, 
                                            state='readonly',relief='sunken',bd=1)
        self.image_path_label_entry.place(x=195, y=6,height=37)
      

        self.segmentation_path_label = Label(root, text='输出分割文件：', font=('楷体', 15),padx=10,pady=10)
        self.segmentation_path_label.place(x=0, y=60)
        self.segmentation_path_label_entry = Entry(root, textvariable=self.segmentation_path, font=('宋体', 11), width=50,
                                                   state='readonly',relief='sunken',bd=1)
        self.segmentation_path_label_entry.place(x=195, y=66,height=37)

        self.samples_path_label = Label(root, text='输入样本文件：', font=('楷体', 15),padx=10,pady=10)
        self.samples_path_label.place(x=0, y=120)
        self.samples_path_label_entry = Entry(root, textvariable=self.samples_path, font=('宋体', 11), width=50, 
                                              state='readonly',relief='sunken',bd=1)
        self.samples_path_label_entry.place(x=195, y=126,height=37)

        self.classification_path_label = Label(root, text='输出分类文件：', font=('楷体', 15),padx=10,pady=10)
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
        self.image_file_button.bind('<Enter>',on_button1)   #绑定事件，Enter为鼠标进入按钮，Leave为鼠标离开按钮
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
                                                           padx=10,pady=10)
        self.classification_method_selection_label.place(x=0, y=240)
       
        self.gpu_selection_label = Label(root, text='选择运算设备：', font=('楷体', 15),
                                         padx=10,pady=10)
        self.gpu_selection_label.place(x=0, y=300)
      
    #   选择算法或设备（激活Radio）后改变字体颜色，以突出已选的Radio
        def radioSelected1(e):
            DT_btn['foreground']='#000000'
            SVM_btn['foreground']='#717171'
            RF_btn['foreground']='#717171'
        def radioSelected2(e):
            DT_btn['foreground']='#717171'
            SVM_btn['foreground']='#000000'
            RF_btn['foreground']='#717171'
        def radioSelected3(e):
            DT_btn['foreground']='#717171'
            SVM_btn['foreground']='#717171'
            RF_btn['foreground']='#000000'
        def radioSelected4(e):
            GPU_btn['foreground']='#000000'
            CPU_btn['foreground']='#717171'
        def radioSelected5(e):
            GPU_btn['foreground']='#717171'
            CPU_btn['foreground']='#000000'
        self.classification_method.set("DT")
        DT_btn=Radiobutton(root, text="决策树", variable=self.classification_method, value="DT",
                           cursor='hand2',font=('黑体',12),foreground='#000000')
        DT_btn.bind('<Button-1>',radioSelected1) # Button-1是鼠标左键点击事件
        DT_btn.pack()
        DT_btn.place(x=190,y=253)

        SVM_btn=Radiobutton(root, text="支持向量机", variable=self.classification_method, value="SVM",
                            cursor='hand2',font=('黑体',12),foreground='#717171')
        SVM_btn.bind('<Button-1>',radioSelected2) 
        SVM_btn.pack()
        SVM_btn.place(x=290,y=253)

        RF_btn=Radiobutton(root, text="随机森林", variable=self.classification_method, value="RF",
                           cursor='hand2',font=('黑体',12),foreground='#717171')
        RF_btn.bind('<Button-1>',radioSelected3) 
        RF_btn.pack()
        RF_btn.place(x=432,y=253)

        self.gpu_selection.set("GPU")
        GPU_btn=Radiobutton(root, text="GPU", variable=self.gpu_selection, value="GPU",
                            cursor='hand2',font=('Times New Roman',13),foreground='#000000')
        GPU_btn.bind('<Button-1>',radioSelected4)
        GPU_btn.pack()
        GPU_btn.place(x=190,y=310)
        CPU_btn=Radiobutton(root, text="CPU", variable=self.gpu_selection, value="CPU",
                            cursor='hand2',font=('Times New Roman',13),foreground='#717171')
        CPU_btn.bind('<Button-1>',radioSelected5)
        CPU_btn.pack()
        CPU_btn.place(x=290,y=310)

        #--------- 软件运算执行的相关组件 ---------#  
        self.segmentation_button = Button(root,text='分割',cursor='hand2',relief='raised',command=self.segmentation,
                                        width=8,bg='#ECECEC',font=('华文彩云',12),activebackground='#D9D9D9')
        self.segmentation_button.pack()
        self.segmentation_button.place(x=10,y=370)


        self.classification_button = Button(root,text='分类',cursor='hand2',relief='raised',command=self.classification,
                                        width=8,bg='#ECECEC',font=('华文彩云',12),activebackground='#D9D9D9')
        self.classification_button.pack()
        self.classification_button.place(x=150,y=370)

        # 创建一个退出按钮
        self.quit_button= Button(root,text='退出',cursor='hand2',relief='raised',command=root.destroy,
                                        width=8,bg='#ECECEC',font=('华文彩云',12),activebackground='#D9D9D9')
        self.quit_button.pack()
        self.quit_button.place(x=430,y=370)

        # 图片显示按钮
        self.showImage_button= Button(root,text='图片',cursor='hand2',relief='raised',command=self.showImage,
                                        width=8,bg='#ECECEC',font=('华文彩云',12),activebackground='#D9D9D9')
        self.showImage_button.pack()
        self.showImage_button.place(x=290,y=370)

        
    # 缩放图片的尺寸    
    def resizeImage(self,Image_original):
        (w,h)=Image_original.size
        f1 = 800/w
        f2 = 600/h  
        factor = min(f1,f2)
        width  = int(w*factor)  
        height = int(h*factor)
        return Image_original.resize((width, height), Image.ANTIALIAS)
    
    # 图片查看器中的菜单栏 用来切换不同的图片
    def selectImage(self,ImageType):
        if ImageType=='InputImage':
            filename=self.image_path.get()
            if filename=='':
                messagebox.showinfo('错误','未输入图像文件')
                self.ImageRoot.destroy
                return
            MyImage=Image.open(filename)       # 打开图片
            self.Image_btn1['relief']='sunken' # 改变按钮的样式（例如，展示初始图像时，该按钮为“下沉”样式）
            self.Image_btn2['relief']='raised'
            self.Image_btn3['relief']='raised'
            self.Image_btn4['relief']='raised'
        elif ImageType=='SegmentImage':
            filename=self.segmentation_path.get()
            if filename=='':
                messagebox.showinfo('错误','无分割结果')
                self.ImageRoot.destroy
                return
            MyImage=Image.open(filename)
            self.Image_btn1['relief']='raised'
            self.Image_btn2['relief']='sunken'
            self.Image_btn3['relief']='raised'
            self.Image_btn4['relief']='raised'
        elif ImageType=='SamplesImage':
            filename=self.samples_path.get()
            if filename=='':
                messagebox.showinfo('错误','未输入样本文件')
                self.ImageRoot.destroy
                return
            MyImage=Image.open(filename)
            self.Image_btn1['relief']='raised'
            self.Image_btn2['relief']='raised'
            self.Image_btn3['relief']='sunken'
            self.Image_btn4['relief']='raised'
        elif ImageType=='ClassifyImage':
            filename=self.classification_path.get()
            if filename=='':
                messagebox.showinfo('错误','无分类结果')
                self.ImageRoot.destroy
                return
            MyImage=Image.open(filename)
            self.Image_btn1['relief']='raised'
            self.Image_btn2['relief']='raised'
            self.Image_btn3['relief']='raised'
            self.Image_btn4['relief']='sunken'
        MyImage_resized=self.resizeImage(MyImage)        # 调整图片的尺寸
        self.MyPhoto=ImageTk.PhotoImage(MyImage_resized) # 图片转为PhotoImage
        self.PhotoLabel['image']=self.MyPhoto            # 为Label设置image属性

    # 新建一个toplevel的root当作图片查看器
    def showImage(self): 
        # 新建一个容器     
        ImageRoot = Toplevel(root)
        ImageRoot.geometry('800x620') # 图片可显示的最大尺寸实际为800*600，纵向预留了20给按钮组
        ImageRoot.title('图片查看器')

        # 用4个button组成按钮组来选择在图片查看器中加载的图片
        Image_btn_frame=Frame(ImageRoot,height=30)
        Image_btn_frame.pack()
        self.Image_btn1=Button(Image_btn_frame, text='初始图像', command=lambda:self.selectImage(ImageType='InputImage'),
                               cursor='hand2',relief='raised',width=10,bg='#ECECEC',font=('宋体',12),
                               activebackground='#D9D9D9')
        self.Image_btn1.grid(row=0,column=0)

        self.Image_btn2=Button(Image_btn_frame, text='分割结果', command=lambda:self.selectImage(ImageType='SegmentImage'),
                               cursor='hand2',relief='raised',width=10,bg='#ECECEC',font=('宋体',12),
                               activebackground='#D9D9D9')
        self.Image_btn2.grid(row=0,column=1)

        self.Image_btn3=Button(Image_btn_frame, text='样本图像', command=lambda:self.selectImage(ImageType='SamplesImage'),
                               cursor='hand2',relief='raised',width=10,bg='#ECECEC',font=('宋体',12),
                               activebackground='#D9D9D9')
        self.Image_btn3.grid(row=0,column=2)

        self.Image_btn4=Button(Image_btn_frame, text='分类结果', command=lambda:self.selectImage(ImageType='ClassifyImage'),
                               cursor='hand2',relief='raised',width=10,bg='#ECECEC',font=('宋体',12),
                               activebackground='#D9D9D9')
        self.Image_btn4.grid(row=0,column=3)

        # 用Label加载图片
        self.PhotoLabel=Label(ImageRoot)
        self.PhotoLabel.pack(pady=20)
        # self.PhotoLabel.place(y=50)
        ImageRoot.mainloop()

    # 非常简单地完善了以下“分类”和“分割”按钮的报错
    def segmentation(self):
        if self.image_path.get()=='':
            messagebox.showinfo('错误','未输入图像文件')
        elif self.segmentation_path.get()=='':
            messagebox.showinfo('错误','未指定输出分割文件')
        else:
            messagebox.showinfo("分割","开始分割")

    def classification(self):
        if self.samples_path.get()=='':
            messagebox.showinfo('错误','未输入样本文件')
        elif self.classification_path.get()=='':
            messagebox.showinfo('错误','未指定输出分类文件')
        else:
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
root.geometry("810x450")
root.title("一个经典的GUI程序类的测试")
root.resizable(False, False)
app = Application(master=root)


# 进度条
# bar = Progressbar(root, length=200, maximum=100, value=30)
# bar.pack(padx=10, pady=10)

root.mainloop()
print(app.image_path.get())