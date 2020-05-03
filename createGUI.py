#-*- coding: utf-8 -*-
import json, os, datetime, random, string, glob, pprint, gmusicapi
import urllib.request as req
from time import sleep
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

# 処理するフォルダ
target_dir = "processing/"
# Google Music APIを処理するフォルダ
IMAGE_PROCESSING = '__processing/'
# データを保存するjsonファイル
json_path = "src/sample.json"
# 曲の保存ファイル
music_path = "music/mp3/"
# アートワークの保存ファイル
artw_path = "music/illust/"
# 証明書
CREDENTIAL_FILE = 'mobileclient.cred'


api = gmusicapi.Mobileclient()
if not os.path.exists(CREDENTIAL_FILE):
    api.perform_oauth(CREDENTIAL_FILE)
api.oauth_login(gmusicapi.Mobileclient.FROM_MAC_ADDRESS, CREDENTIAL_FILE)


def txt(_text):
    consolelog.insert('1.0', '\n'+str(_text))

def select_track(x, song_data):
    def c():
        
        entry_MN.delete(0, END)
        entry_feat.delete(0, END)
        entry_artist.delete(0, END)
        entry_genre.delete(0, END)
        entry_release.delete(0, END)

        entry_MN.insert(END, song_data[x]["title"])
        entry_artist.insert(END, song_data[x]["artist"])
        entry_release.insert(END, song_data[x]["year"])

        try:    os.rename(IMAGE_PROCESSING+str(x)+".jpg", target_dir+str(x)+".jpg")
        except: txt("file does not exist.")

    return c

def randomName():
    return ''.join(random.choices(string.ascii_uppercase, k=15))

def clear(_clear):
    if _clear == 1:
        entry_MN.delete(0, END)
    if _clear == 2:
        entry_feat.delete(0, END)
    if _clear == 3:
        entry_artist.delete(0, END)
    if _clear == 4:
        entry_genre.delete(0, END)
    if _clear == 5:
        entry_release.delete(0, END)

def search(self):
    with open(json_path, "r") as f:
        json_data = json.load(f)
    txt("load "+json_path)

    music_name = tk_search.get()

    if(music_name in [L["music_data"]["name"] for L in json_data if L["music_data"]["name"]==music_name]):
        txt("this misuc file has already been saved.")
    else:
        txt("Check Ok!")
        google_music_data = api.search(music_name, max_results=5)

        song_data = []
        s_btn     = []
        img       = []
        s_frame   = []

        count = 0
        for data in google_music_data["song_hits"]:

            data                 = data["track"]
            track_title          = data["title"]
            try:    track_artist = data["artist"]
            except: track_artist = ""
            try:    track_year   = data["year"]
            except: track_year   = ""

            track_json_data = {
                "title":  track_title,
                "artist": track_artist,
                "year":   track_year
            }
            song_data.append(track_json_data)

            req.urlretrieve(data["albumArtRef"][0]["url"], IMAGE_PROCESSING+str(count)+'.jpg')
            count  += 1
        

        s_root = Tk()
        s_root.geometry('800x800')
        s_root.title("Google Music API 検索")


        count = 0
        for data in google_music_data["song_hits"]:

            img.append(Image.open(IMAGE_PROCESSING+str(count)+'.jpg'))
            img[count].thumbnail((100, 100), Image.ANTIALIAS)
            #img[count] = ImageTk.PhotoImage(img[count])

            s_frame.append(ttk.Frame(s_root, width=800, padding=0, relief="groove"))
            s_frame[count].grid(row=count,column=0,sticky=W)

            canvas = Canvas(s_frame[count], width=100, height=100)
            img[count] = ImageTk.PhotoImage(img[count], master=canvas)
            canvas.grid(row=0, column=0, sticky=E)
            canvas.create_image(0, 0, image=img[count], anchor=NW)

            text = "タイトル: {}\nアーティスト: {}\nリリース年: {}\n".format(song_data[count]["title"], song_data[count]["artist"], song_data[count]["year"])
            ttk.Label(s_frame[count], text=text, padding=(5, 2)).grid(row=0, column=1, sticky=E)

            s_btn.append(ttk.Button(s_frame[count], text='選択', command=select_track(count, song_data)))
            s_btn[count].grid(row=0, column=2, sticky=E)

            count += 1

        s_root.mainloop()

def create(self):
    try:
        txt("/**********************************************/")
        mp3_file_path = glob.glob(target_dir+"*.mp3")
        if not mp3_file_path:
            txt("file does not exist.")
            txt("press any key to exit.")
        else:
            mp3_file_path = mp3_file_path[0].replace("\\","/")
            txt("GET "+mp3_file_path)
            

        illust_file_path = glob.glob(target_dir+"*.png")
        if not illust_file_path:
            illust_file_path = glob.glob(target_dir+"*.jpg")
            if not illust_file_path:
                txt("file does not exist.")
                txt("press any key to exit.")
            else:
                illust_file_path = illust_file_path[0].replace("\\","/")
                txt("GET "+illust_file_path)
        else:
            illust_file_path = illust_file_path[0].replace("\\","/")
            txt("GET "+illust_file_path)

        if mp3_file_path and illust_file_path:
            txt("start create")

            with open(json_path, "r") as f:
                json_data = json.load(f)
            txt("load "+json_path)

            input_music_name = tk_MN.get()
            if(input_music_name):
                music_name = input_music_name
            else:
                music_name = mp3_file_path.replace(".mp3","")
                
            if(music_name in [L["music_data"]["name"] for L in json_data if L["music_data"]["name"]==music_name]):
                txt("this misuc file has already been saved.")
            else:
                mp3_path = randomName()+".mp3"
                txt("mp3 name create "+mp3_path)

                os.rename(mp3_file_path, music_path+mp3_path)
                txt("mp3 path "+music_path+mp3_path)

                illust_path = randomName()
                txt("illust name create "+illust_path)

                os.rename(illust_file_path, artw_path+illust_path+illust_file_path[-4:])
                txt("illust path "+artw_path+illust_path+illust_file_path[-4:])

                create_date  = str(datetime.date.today()).replace("-","/")
                featuring    = tk_feat.get().split(",")
                artist_name  = tk_artist.get().split(",")
                genre        = tk_genre.get().split(",")
                release_date = tk_release.get()

                if featuring and artist_name and genre and release_date:
                    music_json = {
                        "file_data": {
                            "mp3_path": mp3_path,
                            "create_date": create_date,
                            "illust_path": illust_path+illust_file_path[-4:]
                        },
                        "music_data": {
                            "name": music_name,
                            "featuring": featuring,
                            "artist_name": artist_name,
                            "release_date": release_date,
                            "genre": genre
                        }
                    }
                    txt("------------------------------------------------\n"+json.dumps(music_json, indent=2)+"\n------------------------------------------------")

                    json_data.append(music_json)

                    with open(json_path, "w") as f:
                        json.dump(json_data, f, indent=4)
                    del json_data

                    txt("complete "+mp3_path)
                    txt("complete illust "+illust_path+illust_file_path[-4:])

                else:
                    txt("text box unfilled.")
        else:
            txt("file does not exist.")
    except Exception as e:
        txt("Error "+str(e))


if __name__ in "__main__":
    root = Tk()
    root.title("Animedley Create")
    root.resizable(False, False)
    frame = ttk.Frame(root, padding=20)
    frame.grid(row=0,column=0,sticky=W)

    ttk.Label(frame, text='曲名',        padding=(5, 2)).grid(row=0, column=0, sticky=E)
    ttk.Label(frame, text='feat',        padding=(5, 2)).grid(row=1, column=0, sticky=E)
    ttk.Label(frame, text='アーティスト', padding=(5, 2)).grid(row=2, column=0, sticky=E)
    ttk.Label(frame, text='ジャンル',     padding=(5, 2)).grid(row=3, column=0, sticky=E)
    ttk.Label(frame, text='リリース年',   padding=(5, 2)).grid(row=4, column=0, sticky=E)
    ttk.Label(frame, text='サーチ',       padding=(5, 2)).grid(row=5, column=0, sticky=E)

    tk_MN         = StringVar()
    tk_feat       = StringVar()
    tk_artist     = StringVar()
    tk_genre      = StringVar()
    tk_release    = StringVar()
    tk_search     = StringVar()

    entry_MN      = ttk.Entry(frame, textvariable=tk_MN, width=30)
    entry_feat    = ttk.Entry(frame, textvariable=tk_feat, width=30)
    entry_artist  = ttk.Entry(frame, textvariable=tk_artist, width=30)
    entry_genre   = ttk.Entry(frame, textvariable=tk_genre, width=30)
    entry_release = ttk.Entry(frame, textvariable=tk_release, width=30)
    entry_search  = ttk.Entry(frame, textvariable=tk_search, width=30)

    entry_MN.grid(row=0, column=1)
    entry_feat.grid(row=1, column=1)
    entry_artist.grid(row=2, column=1)
    entry_genre.grid(row=3, column=1)
    entry_release.grid(row=4, column=1)
    entry_search.grid(row=5, column=1)

    btn_MN         = ttk.Button(frame, text='clear', command= lambda : clear(1)).grid(row=0, column=2)
    btn_feat       = ttk.Button(frame, text='clear', command= lambda : clear(2)).grid(row=1, column=2)
    btn_artist     = ttk.Button(frame, text='clear', command= lambda : clear(3)).grid(row=2, column=2)
    btn_genre      = ttk.Button(frame, text='clear', command= lambda : clear(4)).grid(row=3, column=2)
    btn_release    = ttk.Button(frame, text='clear', command= lambda : clear(5)).grid(row=4, column=2)
    btn_search     = ttk.Button(frame, text='検索'  , command= lambda : search(btn_search)).grid(row=5, column=2)

    btn = ttk.Frame(frame, padding=20)
    btn.grid(row=6,column=1,sticky=W)

    ok         = ttk.Button(btn, text='create', command= lambda : create(ok)).pack(side=LEFT)
    cancel     = ttk.Button(btn, text='exit',command=quit).pack(side=LEFT)

    frame2 = ttk.Frame(root, padding=20)
    frame2.grid(row=1,column=0,sticky=W)

    consolelog = Text(frame2, width=48, foreground='#32cd32', background='#000000')
    consolelog.grid(row=0, column=0, sticky=(N, S, E, W))
    frame2.columnconfigure(0, weight=1)
    frame2.rowconfigure(0, weight=1)

    with open(json_path, "r") as f:
        json_data = json.load(f)
    txt("楽曲総数: {}".format(len(json_data)))
    txt("曲とｱｰﾄﾜｰｸを{}ﾌｫﾙﾀﾞに入れて下さい。".format(target_dir))

    root.mainloop()