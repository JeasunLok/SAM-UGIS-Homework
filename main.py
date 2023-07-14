"""测试一个经典的GUI程序的写法,使用面向对象的方式"""
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename,asksaveasfilename
from PIL import Image,ImageTk
import os
from tkinter import ttk
import time
import threading
import numpy as np
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

from src.sam_segmentation import sam_segmentation
from src.econ_segmentation import econ_segmentation
from src.classification import main_classification

def thread_it(func, *args):
    # 创建线程
    t = threading.Thread(target=func, args=args) 
    # 守护线程
    t.setDaemon(True) 
    # 启动线程
    t.start()

class Application(Frame):
    """一个经典的GUI程序的类的写法"""
    def __init__(self, master=None):
        super().__init__(master)      #super()代表的是父类的定义，而不是父类对象
        self.master=master
        self.pack()
        self.image_path = StringVar()
        self.samples_path = StringVar()

        self.segmentation_path = StringVar()
        self.segmentation_method = StringVar()

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
        # 选中GPU
        def radioSelected4(e):
            GPU_btn['foreground']='#000000'
            CPU_btn['foreground']='#717171'
        # 选中CPU
        def radioSelected5(e):
            GPU_btn['foreground']='#717171'
            CPU_btn['foreground']='#000000'
        # 选中SAM分割
        def radioSelected6(e):
            SAM_btn['foreground']='#000000'
            ECON_btn['foreground']='#717171'
            self.Kernel_size_entry['state']='disabled'
            self.Max_dist_entry['state']='disabled'
            Kernel_size['foreground']='#717171'
            Max_dist['foreground']='#717171'
         # 选中ECON分割
        def radioSelected7(e):
            SAM_btn['foreground']='#717171'
            ECON_btn['foreground']='#000000'
            self.Kernel_size_entry['state']='normal'
            self.Max_dist_entry['state']='normal'
            Kernel_size['foreground']='#000000'
            Max_dist['foreground']='#000000'

   
        ## 分割算法选择 还有参数 选择多尺度分割需要有两个输入文本框输入两个参数1.核大小 2.最大距离
        self.segmentation_method_selection_label = Label(root, text='选择分割算法：',font=('楷体', 15),
                                                           padx=10,pady=10)
        self.segmentation_method_selection_label.pack()
        self.segmentation_method_selection_label.place(x=0, y=240)

        self.segmentation_method.set("SAM")
        SAM_btn=Radiobutton(root, text="SAM分割", variable=self.segmentation_method, value="SAM",
                           cursor='hand2',font=('黑体',12),foreground='#000000')
        SAM_btn.bind('<Button-1>',radioSelected6) # Button-1是鼠标左键点击事件
        SAM_btn.pack()
        SAM_btn.place(x=190,y=253)

        ECON_btn=Radiobutton(root, text="多尺度分割", variable=self.segmentation_method, value="ECON",
                            cursor='hand2',font=('黑体',12),foreground='#717171')
        ECON_btn.bind('<Button-1>',radioSelected7) 
        ECON_btn.pack()
        ECON_btn.place(x=290,y=253)

        # ECON算法的两个参数
        self.econ_seg_kernel_size = StringVar()
        self.econ_seg_max_dist = StringVar()

        ECON_para_frame=Frame(root,height=30,width=300,relief='groove',bd=2,padx=5,pady=5)
        ECON_para_frame.pack()
        ECON_para_frame.place(x=490,y=250)
        Kernel_size=Label(ECON_para_frame, text='核大小:', font=('黑体',11),foreground='#717171')
        Kernel_size.grid(row=0,column=0)
        self.Kernel_size_entry = Entry(ECON_para_frame, textvariable=self.econ_seg_kernel_size, font=('Times New Roman', 11), 
                                              relief='sunken',bd=1,width=6,state='disabled',justify='center')                            
        self.Kernel_size_entry.grid(row=0,column=1)

        Max_dist=Label(ECON_para_frame, text=' 最大距离:', font=('黑体',11),foreground='#717171')
        Max_dist.grid(row=0,column=2)
        self.Max_dist_entry = Entry(ECON_para_frame, textvariable=self.econ_seg_max_dist, font=('Times New Roman', 11),
                                              relief='sunken',bd=1,width=6,state='disabled',justify='center')
        self.Max_dist_entry.grid(row=0,column=3)
        
        
        # 选择分类算法
        self.classification_method_selection_label = Label(root, text='选择分类算法：',font=('楷体', 15),
                                                           padx=10,pady=10)
        self.classification_method_selection_label.place(x=0, y=300)
       
        self.gpu_selection_label = Label(root, text='选择运算设备：', font=('楷体', 15),
                                         padx=10,pady=10)
        self.gpu_selection_label.place(x=0, y=360)
        self.classification_method.set("DT")
        DT_btn=Radiobutton(root, text="决策树", variable=self.classification_method, value="DT",
                           cursor='hand2',font=('黑体',12),foreground='#000000')
        DT_btn.bind('<Button-1>',radioSelected1) # Button-1是鼠标左键点击事件
        DT_btn.pack()
        DT_btn.place(x=190,y=313)

        SVM_btn=Radiobutton(root, text="支持向量机", variable=self.classification_method, value="SVM",
                            cursor='hand2',font=('黑体',12),foreground='#717171')
        SVM_btn.bind('<Button-1>',radioSelected2) 
        SVM_btn.pack()
        SVM_btn.place(x=290,y=313)

        RF_btn=Radiobutton(root, text="随机森林", variable=self.classification_method, value="RF",
                           cursor='hand2',font=('黑体',12),foreground='#717171')
        RF_btn.bind('<Button-1>',radioSelected3) 
        RF_btn.pack()
        RF_btn.place(x=432,y=313)

        # 设置训练集比例
        self.train_ratio=StringVar()
        self.train_ratio.set('0.6')
        Train_ratio_frame=Frame(root,height=30,width=50,relief='groove',bd=2,padx=5,pady=5)
        Train_ratio_frame.pack()
        Train_ratio_frame.place(x=608,y=310)
        Train_ratio=Label(Train_ratio_frame, text='训练集比例:', font=('黑体',11))
        Train_ratio.grid(row=0,column=0)
        self.Train_ratio_entry=Entry(Train_ratio_frame,textvariable=self.train_ratio, font=('Times New Roman', 11), 
                                              relief='sunken',bd=1,width=6,justify='center')
        self.Train_ratio_entry.grid(row=0,column=1)
        

        # 选择运算设备
        self.gpu_selection.set("GPU")
        GPU_btn=Radiobutton(root, text="GPU", variable=self.gpu_selection, value="GPU",
                            cursor='hand2',font=('Times New Roman',13),foreground='#000000')
        GPU_btn.bind('<Button-1>',radioSelected4)
        GPU_btn.pack()
        GPU_btn.place(x=190,y=370)
        CPU_btn=Radiobutton(root, text="CPU", variable=self.gpu_selection, value="CPU",
                            cursor='hand2',font=('Times New Roman',13),foreground='#717171')
        CPU_btn.bind('<Button-1>',radioSelected5)
        CPU_btn.pack()
        CPU_btn.place(x=290,y=370)

        # 显示分类精度
        self.accuracy_OA = StringVar()
        self.accuracy_OA.set("0")
        self.accuracy_Kappa = StringVar()
        self.accuracy_Kappa.set("0")

        Accuracy_frame=Frame(root,height=10,width=100,relief='groove',bd=2,padx=5,pady=5)
        Accuracy_frame.pack()
        Accuracy_frame.place(x=558,y=370)
        OA=Label(Accuracy_frame, text='OA:', font=('Times New Roman',11))
        OA.grid(row=0,column=0)
        self.OA_entry=Entry(Accuracy_frame,textvariable=self.accuracy_OA, font=('Times New Roman', 11), 
                                              relief='sunken',bd=1,width=6,state='readonly',justify='center')
        self.OA_entry.grid(row=0,column=1)
        Kappa=Label(Accuracy_frame, text=' Kappa:', font=('Times New Roman',11))
        Kappa.grid(row=0,column=2)
        self.Kappa_entry=Entry(Accuracy_frame,textvariable=self.accuracy_Kappa, font=('Times New Roman', 11), 
                                              relief='sunken',bd=1,width=6,state='readonly',justify='center')
        self.Kappa_entry.grid(row=0,column=3)


        #--------- 软件运算执行的相关组件 ---------#  
        # self.segmentation_button = Button(root,text='分割',cursor='hand2',relief='raised',command=self.segmentation,
        #                                 width=8,bg='#ECECEC',font=('华文彩云',12),activebackground='#D9D9D9')
        self.segmentation_button = Button(root,text='分割',cursor='hand2',relief='raised',command=lambda:thread_it(self.segmentation),
                                width=8,bg='#ECECEC',font=('华文彩云',12),activebackground='#D9D9D9')
        self.segmentation_button.pack()
        self.segmentation_button.place(x=10,y=430)


        self.classification_button = Button(root,text='分类',cursor='hand2',relief='raised',command=lambda:thread_it(self.classification),
                                        width=8,bg='#ECECEC',font=('华文彩云',12),activebackground='#D9D9D9')
        self.classification_button.pack()
        self.classification_button.place(x=150,y=430)

        # 创建一个退出按钮
        self.quit_button= Button(root,text='退出',cursor='hand2',relief='raised',command=root.destroy,
                                        width=8,bg='#ECECEC',font=('华文彩云',12),activebackground='#D9D9D9')
        self.quit_button.pack()
        self.quit_button.place(x=430,y=430)

        # 图片显示按钮
        self.showImage_button= Button(root,text='图片',cursor='hand2',relief='raised',command=self.showImage,
                                        width=8,bg='#ECECEC',font=('华文彩云',12),activebackground='#D9D9D9')
        self.showImage_button.pack()
        self.showImage_button.place(x=290,y=430)

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
                return
            MyImage=Image.open(filename)       # 打开图片
            self.Image_btn1['relief']='sunken' # 改变按钮的样式（例如，展示初始图像时，该按钮为“下沉”样式）
            self.Image_btn2['relief']='raised'
            self.Image_btn4['relief']='raised'
        elif ImageType=='SegmentImage':
            filename=self.segmentation_path.get()
            if filename=='':
                messagebox.showinfo('错误','无分割结果')
                return
            MyImage=Image.open(filename)
            MyImage_array=np.array(MyImage)
            MyImage_array=np.floor(np.array(MyImage_array)/np.max(MyImage_array)*255)
            MyImage=Image.fromarray(MyImage_array)
            self.Image_btn1['relief']='raised'
            self.Image_btn2['relief']='sunken'
            self.Image_btn4['relief']='raised'
        elif ImageType=='ClassifyImage':
            filename=self.classification_path.get()
            if filename=='':
                messagebox.showinfo('错误','无分类结果')
                return
            MyImage=Image.open(filename)
            MyImage_array=np.array(MyImage)
            MyImage_array=np.floor(np.array(MyImage_array)/np.max(MyImage_array)*255)
            MyImage=Image.fromarray(MyImage_array)
            self.Image_btn1['relief']='raised'
            self.Image_btn2['relief']='raised'
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

        # self.Image_btn3=Button(Image_btn_frame, text='样本图像', command=lambda:self.selectImage(ImageType='SamplesImage'),
        #                        cursor='hand2',relief='raised',width=10,bg='#ECECEC',font=('宋体',12),
        #                        activebackground='#D9D9D9')
        # self.Image_btn3.grid(row=0,column=2)

        self.Image_btn4=Button(Image_btn_frame, text='分类结果', command=lambda:self.selectImage(ImageType='ClassifyImage'),
                               cursor='hand2',relief='raised',width=10,bg='#ECECEC',font=('宋体',12),
                               activebackground='#D9D9D9')
        self.Image_btn4.grid(row=0,column=2)

        # 用Label加载图片
        self.PhotoLabel=Label(ImageRoot)
        self.PhotoLabel.pack(pady=20)
        # self.PhotoLabel.place(y=50)
        ImageRoot.mainloop()
    
    # 进度条组件
    # 启动进度条
    def startProgressbar(self):
        # 创建一个新窗口用于显示进度条
        screenwidth = root.winfo_screenwidth()  # 获取显示屏宽度
        screenheight = root.winfo_screenheight()
        root_size = '%dx%d+%d+%d' % (350, 150, (screenwidth - 350) / 2, (screenheight - 150) / 2)  # 设置窗口居中参数
        self.BarRoot=Toplevel(root)
        self.BarRoot.geometry(root_size)
        self.BarRoot.title('程序运行中')
        self.Mybar=ttk.Progressbar(self.BarRoot,length=300,mode='indeterminate',orient='horizontal')
        self.Mybar.pack(padx=10,pady=50)
        self.Mybar.start()
    # 停止进度条并关闭该窗口
    def stopProgreebar(self):  
        self.Mybar.stop()
        self.BarRoot.destroy()
        
    # 非常简单地完善了以下“分类”和“分割”按钮的报错
    def segmentation(self):
        if self.image_path.get()=='':
            messagebox.showinfo('错误','未输入图像文件')
        elif self.segmentation_path.get()=='':
            messagebox.showinfo('错误','未指定输出分割文件')
        else:
            # 这里加了一个选择ECON算法时的分割参数输入的验证，此处只简单验证了是否为数字
            if self.segmentation_method.get()=='ECON':
                if self.Kernel_size_entry.get().isdigit()==False or self.Max_dist_entry.get().isdigit()==False:
                    messagebox.showerror('错误','分割参数输入错误')
                    self.Kernel_size_entry.delete(0,'end')
                    self.Max_dist_entry.delete(0,'end')
                    return
            messagebox.showinfo("分割","开始分割")            
            self.startProgressbar() # 启动进度条
            print(self.segmentation_method.get()+" segmentation")
            if self.segmentation_method.get() == "SAM":
                sam_segmentation(self.image_path.get(), self.segmentation_path.get(), self.gpu_selection.get())
            elif self.segmentation_method.get() == "ECON":
                econ_segmentation(self.image_path.get(), self.segmentation_path.get(), float(self.econ_seg_kernel_size.get()), float(self.econ_seg_max_dist.get()))
            self.stopProgreebar()   # 停止进度条
            messagebox.showinfo("分割","分割完成")

    def classification(self):
        if self.samples_path.get()=='':
            messagebox.showinfo('错误','未输入样本文件')
        elif self.classification_path.get()=='':
            messagebox.showinfo('错误','未指定输出分类文件')
        else:
            # 检查训练集比例是否符合0-1
            if float(self.Train_ratio_entry.get())<=0.0 or float(self.Train_ratio_entry.get())>=1.0:
                messagebox.showerror('错误','训练集比例输入错误')
                self.Train_ratio_entry.delete(0,'end')
                return
            messagebox.showinfo("分类","开始分类")
            self.startProgressbar() # 启动进度条
            print(self.classification_method.get()+" segmentation")
            accuracy = main_classification(self.image_path.get(), self.segmentation_path.get(), self.samples_path.get(), self.classification_path.get(), float(self.train_ratio.get()), self.classification_method.get())
            self.accuracy_OA.set(str(round(accuracy["OA"], 4)))
            self.accuracy_Kappa.set(str(round(accuracy["kappa"], 3)))
            self.stopProgreebar()   # 停止进度条
            messagebox.showinfo("分类","分类完成")
            
    def image_load(self):
        filename = askopenfilename(filetypes=[("tif图像文件", "*.tif")])
        self.image_path.set(filename)

    def segmentation_load(self):
        # 选择输出文件的路径并命名,filetypes参数后续可以根据具体情况更改
        filename = asksaveasfilename(defaultextension='.tif',filetypes=[('tif图像文件', '*.tif'), ('All Files', '*.*')]) 
        self.segmentation_path.set(filename)

    def samples_load(self):
        filename = askopenfilename(filetypes=[("shp矢量文件", "*.shp")])
        self.samples_path.set(filename)

    def classification_load(self):
        filename = asksaveasfilename(defaultextension='.tif') 
        self.classification_path.set(filename)

root=Tk()
screenwidth = root.winfo_screenwidth()  # 获取显示屏宽度
screenheight = root.winfo_screenheight()
root_size = '%dx%d+%d+%d' % (810, 500, (screenwidth - 810) / 2, (screenheight - 500) / 2)  # 设置窗口居中参数
root.geometry(root_size)  # 让窗口居中显示

root.title("SAM与多尺度分割卫星图像分割与分类开发版本")
root.resizable(False, False)
app = Application(master=root)
root.mainloop()