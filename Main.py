from tkinter import *

import Scraping

class Main():

    def __init__(self):

        #Scrapingインスタンス生成
        self.s = Scraping.Scraping()
        
        self.label_x = 20
        self.label_y = 20
        self.entry_width = 30
        self.entry_x = 40
        self.entry_y = 20
        self.get_flag = False

        ####メイン画面の生成####
        self.root = Tk()
        self.root.title("スクレイピングツール")
        self.root.geometry("400x250")

        ###メニュー作成###
        self.menu_ROOT = Menu(self.root)
        self.root.configure(menu = self.menu_ROOT)
        
        self.menu_ROOT.add_command(label = "終了(X)", under = 3, command = None)
        
        ###キーワードを入力するbox###
        self.keyword_text = Label(text=u'キーワードを入力してください：', foreground='#000000')
        self.keyword_text.place(x = self.label_x, y = self.label_y)
        self.keyword_box = Entry(width = self.entry_width)
        self.keyword_box.pack(anchor = E, padx = self.entry_x, pady = self.entry_y)

        ###submitボタン###
        self.btn = Button(self.root, text='データ取得')

        # ウィジェットが左クリックされたときの関数を定義
        self.btn.bind("<1>", self.scraping)
        self.btn.place(x=170, y=170)
        
        #データ取得状況を監視
        self.checkGetFlag()

    def scraping(self, event):
        #データ取得中はボタンをクリックできない
        event.widget.bind("<1>", self.stop)
        self.get_flag = True
        event.widget.configure(text = 'データ取得中')

        #スクレイピング開始
        self.s.scraping(self.keyword_box.get())
        
        self.get_flag = False

    def checkGetFlag(self):
        if (self.btn.cget('text') == "データ取得中") and not self.get_flag :
            self.btn.bind("<1>", self.scraping)
            self.btn.configure(text = 'データ取得')
        self.root.after(10, self.checkGetFlag)

    def stop(self,event):
        pass
if __name__ == "__main__":
    main = Main()
    main.root.mainloop()