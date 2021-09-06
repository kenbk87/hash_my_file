from tkinter import *
from tkinter import filedialog, Menu
import cv2
import os
import hashlib
import audioread

cuasochinh = Tk()
cuasochinh.title("Get MD5 2.0 - Updated on 17/7/2021 - coded by Ken")
cuasochinh.wm_iconbitmap('')


def donothing():
    pass


#Hàm tính mã MD5 của file:
def generate_file_md5(rootdir, filename, blocksize=2**20):
    m = hashlib.md5()
    with open(os.path.join(rootdir, filename), "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def thoat():
    cuasochinh.quit()


def dungluong(duong_dan_file):
    dungluong_byte = os.path.getsize(duong_dan_file)
    if dungluong_byte >= 1048576:
        dungluong_megabyte = dungluong_byte/1048576
        return str(round(dungluong_megabyte, 1)).replace('.', ',') + 'MB'
    elif round(dungluong_byte/1024) == 0:
        return str(round(dungluong_byte/1024, 1)).replace('.', ',') + 'KB'
    else:
        return str(round(dungluong_byte/1024)).replace('.', ',') + 'KB'


def thoiluong_audio(tep_tim_audio):
    with audioread.audio_open(tep_tim_audio) as f:
        # totalsec contains the length in float
        length = f.duration
        hours = round(length // 3600)  # calculate in hours
        length %= 3600
        mins = round(length // 60)  # calculate in minutes
        length %= 60
        seconds = round(length)  # calculate in seconds
        if hours == 0:
            return (str( mins ) + ' phút ' + str( seconds ) + ' giây')
        else:
            return (str(hours) + ' giờ ' + str(mins) + ' phút ' + str(seconds) + ' giây')


def thoiluong_video(tep_tin_video):
    cap = cv2.VideoCapture(tep_tin_video)
    fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    hours = round(duration//3600)
    minutes = int(duration / 60)
    if minutes < 10:
        minutes = '0' + str(minutes)
    seconds = round(duration % 60, 3)
    if seconds < 10:
        seconds = '0' + str(seconds)
    if hours == 0:
        return ('00:'+ str(minutes) + ':' + str(seconds))
    else:
        return (str(hours) + ':' + str( minutes ) + ':' + str(seconds))


def is_video_file(filename):
    video_file_extensions = (
'.264', '.3g2', '.3gp', '.3gp2', '.3gpp', '.3gpp2', '.3mm', '.3p2', '.60d', '.787', '.89', '.aaf', '.aec', '.aep', '.aepx',
'.aet', '.aetx', '.ajp', '.ale', '.am', '.amc', '.amv', '.amx', '.anim', '.aqt', '.arcut', '.arf', '.asf', '.asx', '.avb',
'.avc', '.avd', '.avi', '.avp', '.avs', '.avs', '.avv', '.axm', '.bdm', '.bdmv', '.bdt2', '.bdt3', '.bik', '.bin', '.bix',
'.bmk', '.bnp', '.box', '.bs4', '.bsf', '.bvr', '.byu', '.camproj', '.camrec', '.camv', '.ced', '.cel', '.cine', '.cip',
'.clpi', '.cmmp', '.cmmtpl', '.cmproj', '.cmrec', '.cpi', '.cst', '.cvc', '.cx3', '.d2v', '.d3v', '.dat', '.dav', '.dce',
'.dck', '.dcr', '.dcr', '.ddat', '.dif', '.dir', '.divx', '.dlx', '.dmb', '.dmsd', '.dmsd3d', '.dmsm', '.dmsm3d', '.dmss',
'.dmx', '.dnc', '.dpa', '.dpg', '.dream', '.dsy', '.dv', '.dv-avi', '.dv4', '.dvdmedia', '.dvr', '.dvr-ms', '.dvx', '.dxr',
'.dzm', '.dzp', '.dzt', '.edl', '.evo', '.eye', '.ezt', '.f4p', '.f4v', '.fbr', '.fbr', '.fbz', '.fcp', '.fcproject',
'.ffd', '.flc', '.flh', '.fli', '.flv', '.flx', '.gfp', '.gl', '.gom', '.grasp', '.gts', '.gvi', '.gvp', '.h264', '.hdmov',
'.hkm', '.ifo', '.imovieproj', '.imovieproject', '.ircp', '.irf', '.ism', '.ismc', '.ismv', '.iva', '.ivf', '.ivr', '.ivs',
'.izz', '.izzy', '.jss', '.jts', '.jtv', '.k3g', '.kmv', '.ktn', '.lrec', '.lsf', '.lsx', '.m15', '.m1pg', '.m1v', '.m21',
'.m21', '.m2a', '.m2p', '.m2t', '.m2ts', '.m2v', '.m4e', '.m4u', '.m4v', '.m75', '.mani', '.meta', '.mgv', '.mj2', '.mjp',
'.mjpg', '.mk3d', '.mkv', '.mmv', '.mnv', '.mob', '.mod', '.modd', '.moff', '.moi', '.moov', '.mov', '.movie', '.mp21',
'.mp21', '.mp2v', '.mp4', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg4', '.mpf', '.mpg', '.mpg2', '.mpgindex', '.mpl',
'.mpl', '.mpls', '.mpsub', '.mpv', '.mpv2', '.mqv', '.msdvd', '.mse', '.msh', '.mswmm', '.mts', '.mtv', '.mvb', '.mvc',
'.mvd', '.mve', '.mvex', '.mvp', '.mvp', '.mvy', '.mxf', '.mxv', '.mys', '.ncor', '.nsv', '.nut', '.nuv', '.nvc', '.ogm',
'.ogv', '.ogx', '.osp', '.otrkey', '.pac', '.par', '.pds', '.pgi', '.photoshow', '.piv', '.pjs', '.playlist', '.plproj',
'.pmf', '.pmv', '.pns', '.ppj', '.prel', '.pro', '.prproj', '.prtl', '.psb', '.psh', '.pssd', '.pva', '.pvr', '.pxv',
'.qt', '.qtch', '.qtindex', '.qtl', '.qtm', '.qtz', '.r3d', '.rcd', '.rcproject', '.rdb', '.rec', '.rm', '.rmd', '.rmd',
'.rmp', '.rms', '.rmv', '.rmvb', '.roq', '.rp', '.rsx', '.rts', '.rts', '.rum', '.rv', '.rvid', '.rvl', '.sbk', '.sbt',
'.scc', '.scm', '.scm', '.scn', '.screenflow', '.sec', '.sedprj', '.seq', '.sfd', '.sfvidcap', '.siv', '.smi', '.smi',
'.smil', '.smk', '.sml', '.smv', '.spl', '.sqz', '.srt', '.ssf', '.ssm', '.stl', '.str', '.stx', '.svi', '.swf', '.swi',
'.swt', '.tda3mt', '.tdx', '.thp', '.tivo', '.tix', '.tod', '.tp', '.tp0', '.tpd', '.tpr', '.trp', '.ts', '.tsp', '.ttxt',
'.tvs', '.usf', '.usm', '.vc1', '.vcpf', '.vcr', '.vcv', '.vdo', '.vdr', '.vdx', '.veg','.vem', '.vep', '.vf', '.vft',
'.vfw', '.vfz', '.vgz', '.vid', '.video', '.viewlet', '.viv', '.vivo', '.vlab', '.vob', '.vp3', '.vp6', '.vp7', '.vpj',
'.vro', '.vs4', '.vse', '.vsp', '.w32', '.wcp', '.webm', '.wlmp', '.wm', '.wmd', '.wmmp', '.wmv', '.wmx', '.wot', '.wp3',
'.wpl', '.wtv', '.wve', '.wvx', '.xej', '.xel', '.xesc', '.xfl', '.xlmv', '.xmv', '.xvid', '.y4m', '.yog', '.yuv', '.zeg',
'.zm1', '.zm2', '.zm3', '.zmv')
    if filename.endswith(video_file_extensions):
        return True


def is_audio_file(filename):
    audio_file_extensions = ('.mp3', '.wav', '.m4a', '.wma', '.aac')
    if filename.endswith(audio_file_extensions):
        return True


#Liệt kê các file trong thư mục được chọn, hiển thị nội dung lên của sổ Text:
def hienthi():
    dd = filedialog.askdirectory()
    ds = os.listdir(dd)
    dem = 1
    for i in ds:
        #Sử dụng đường dẫn tuyệt đối
        dd_tuyet_doi = os.path.join(dd, i)

        #Kiểm tra có phải là tập tin hay không:
        if os.path.isfile(dd_tuyet_doi):
            noidung.insert(INSERT, '- Tệp tin ' + str(dem) +': ' + str(i) + ', dung lượng: ' + dungluong(dd_tuyet_doi) + ';')
            ma_md5 = generate_file_md5(dd, str(i), blocksize=2**20)
            noidung.insert(INSERT, "    Mã MD5: " + ma_md5 + '.' + '\n')
            if is_video_file(i):
                noidung.insert(INSERT, '    Thời lượng: ' + thoiluong_video(dd_tuyet_doi) + '\n')
            elif is_audio_file(i):
                noidung.insert(INSERT, '    Thời lượng: ' + thoiluong_audio(dd_tuyet_doi) + '\n')

            dem = dem + 1


def thong_bao(noi_dung_thong_bao):
    root = Tk()
    root.title('')
    root.geometry("150x30")
    msg = Message(root, text=noi_dung_thong_bao, width=100)
    msg.pack()
    root.after(500, root.destroy)


def sao_chep():
    cuasochinh.clipboard_clear()
    cuasochinh.clipboard_append(noidung.get('1.0', END))
    cuasochinh.update()
    thong_bao('Copied')


#Hàm để xóa nội dung trong ô text:
def xoa():
    noidung.delete('1.0', END)


frame1 = Frame()
lb1 = Label(frame1, text="Choose a folder which contain files:")
lb1.pack(side=LEFT)

chon = Button(frame1, text="Choose", command=hienthi, width=10, padx=5, pady=5)
chon.pack(side=LEFT)

xoa = Button(frame1, text="Clear", command=xoa, width=10, padx=5, pady=5)
xoa.pack(side=LEFT)

saochep = Button(frame1, text="Copy all", command=sao_chep, width=10, padx=5, pady=5)
saochep.pack(side=LEFT)

frame1.grid(row=0,  columnspan=2,  padx=5, pady=5)

lb2 = Label(cuasochinh, text="Danh sách các tập tin có trong thư mục: ")
lb2.grid(row=1, column=0)

noidung = Text(cuasochinh, width=100, height=25)
noidung.config(font=('Times New Roman', 14))
noidung.grid(columnspan=2, row=1)

cuasochinh.resizable(width='FALSE', height='FALSE')
#Khai báo 1 Menu của của sổ chính:
menu1 = Menu(cuasochinh)
cuasochinh.config(menu=menu1)

#Khai báo các sub Menu:
subMenu1 = Menu(menu1)
subMenu2 = Menu(menu1)
subMenu3 = Menu(menu1)

#Đặt tên cho các subMenu:
menu1.add_cascade(label="File", menu=subMenu1)
menu1.add_cascade(label="Edit", menu=subMenu2)
menu1.add_cascade(label="About", menu=subMenu3)

#Thêm các mục trong mỗi subMenu:
subMenu1.add_command(label="Open", command=donothing())
subMenu1.add_command(label="Save", command=donothing())
subMenu1.add_separator()
subMenu1.add_command(label="Exit", command=thoat())

cuasochinh.mainloop()

