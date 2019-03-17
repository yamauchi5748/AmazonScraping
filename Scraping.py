from selenium import webdriver
import pandas as pd
import os

class Scraping():

    def scraping(self, keyword):
        
        if not os.path.isdir("C:/Scraping"):
            #CSVファイルを保存するフォルダをCドライブ直下に作成
            os.mkdir('C:/Scraping')

        #CSVファイルを作成
        f = open('C:/Scraping/result.csv', 'w')
        f.close()

        #データを格納するDataFrameを作成
        df = pd.DataFrame(columns=['商品名', '価格'])

        #chromedriverのオプション設定
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')     #AmazonCAPTHA対策でとりあえずheadlessにしない

        #driverオブジェクト生成
        driver = webdriver.Chrome(executable_path = 'C:\opt\win32\chromedriver.exe', options = options)
        
        #amzonのURL
        amazon_url = 'https://www.amazon.co.jp/'


        #キーワードをURLに追加
        amazon_url += 's?k=' + keyword + '&page='
        url = amazon_url + str(1)

        #ページを取得
        driver.get(url)

        #検索結果リストとページ数を取得
        results = driver.find_elements_by_xpath('//*[@id="s-results-list-atf"]/li')

        page = driver.find_elements_by_xpath('//*[@id="pagn"]/span')
        page_num_xpath = '//*[@id="pagn"]/span[' + str(len(page)-1) + ']'
        page_num = driver.find_elements_by_xpath(page_num_xpath)

        if len(page_num) == 0:
            page_num = 1
        else:
            page_num = int(page_num[0].text)

        #要素取得時に用いるid
        id = '//*[@id="result_'

        #商品検索番号
        product_num = -1

        #一般の表記と異なる商品名のxpath　※表記できない商品名のxpathはここに追記
        name_xpath_list =[
            '"]/div/div[3]/div[1]/a/h2',
            '"]/div/div[4]/div[1]/a/h2',
            '"]/div/div/div/div[4]/a/h2'
        ]

        #一般の表記と異なる商品価格のxpath　※表記できない商品価格のxpathはここに追記
        price_xpath_list = [
            '"]/div/div[6]/div[1]/a/span[2]',
            '"]/div/div[5]/div[1]/a/span[2]',
            '"]/div/div/div/div[5]/a/span[2]',
            '"]/div/div[6]/a/span[2]',
            '"]/div/div[7]/a/span[2]',
            '"]/div/div[9]/a/span[2]',
            '"]/div/div[6]/a/span'
        ]

        for num in range(1, page_num):
            if len(results) >= 24 :
                length = 24
            else :
                length = len(results)

            for i in range(len(results)):
                product_num += 1
                result_id = i + (length*(num-1))

                #商品名取得
                name_result = []
                cnt = 0
                while (len(name_result) == 0) and (cnt < len(name_xpath_list)):
                    name_xpath = id + str(result_id) + name_xpath_list[cnt]
                    name_result = driver.find_elements_by_xpath(name_xpath)
                    cnt += 1

                #商品価格取得
                price_result = []
                cnt = 0
                while (len(price_result) == 0) and (cnt < len(price_xpath_list)):
                    price_xpath = id + str(result_id) + price_xpath_list[cnt]
                    price_result = driver.find_elements_by_xpath(price_xpath)
                    cnt += 1

                if len(name_result) == 0:
                    print(product_num,"no name")
                    continue
                if len(price_result) == 0:
                    print(product_num, 'no price')
                    continue
                
                #データをシリーズ化し、DataFrameに格納
                s = pd.Series([name_result[0].text, price_result[0].text], index=df.columns, name=len(df))
                df = df.append(s)
                #print(product_num,result_id,len(results),name_result[0].text,price_result[0].text)
            
            #200件を超えたら終了
            if product_num > 200:
                return

            #次ページへ遷移
            url = amazon_url + str(num + 1)
            driver.get(url)

            #検索結果を再取得
            results = driver.find_elements_by_xpath('//*[@id="s-results-list-atf"]/li')
        
        # CSVファイルとして出力
        df.to_csv("C:/Scraping/result.csv", index=False, encoding="utf_8_sig")
        
        print(df)
        driver.quit()
