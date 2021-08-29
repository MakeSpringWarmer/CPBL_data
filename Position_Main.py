from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sqlite3

#此程式用於爬取各守備位置球員於一軍之打擊基礎、進階數據並存放於SQLite資料庫中

conn = sqlite3.connect("D:/CPBL_Data/batter.db")
cur = conn.cursor()
try:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    chrome = webdriver.Chrome(options=options, executable_path="D:/CPBL_Data/chromedriver.exe")

    chrome.set_page_load_timeout(10)
    chrome.get('https://www.cpbl.com.tw/stats/recordall')



    for j in range(2,11):

        chrome.find_element_by_xpath('//*[@id="DefenceType"]/option'+"["+str(j)+"]").click()
        Position = chrome.find_element_by_xpath('//*[@id="DefenceType"]/option'+"["+str(j)+"]").text
        time.sleep(2)
        chrome.find_element_by_xpath('//*[@id="bindVue"]/div/div[6]/input').click()
        time.sleep(2)
        chrome.find_element_by_xpath('//*[@id="PageListContainer"]/div[1]/div/table/tbody/tr[1]/th[3]').click()
        time.sleep(2)
        chrome.find_element_by_xpath('//*[@id="PageSize"]/option[4]').click()
        time.sleep(2)
        chrome.find_element_by_xpath('//*[@id="SendTextPaging"]').click()
        time.sleep(2)

        soup = BeautifulSoup(chrome.page_source, 'html5lib')

        trs = soup.find('table').find_all('tr')
        Year = chrome.find_element_by_xpath('//*[@id="bindVue"]/div/div[2]/select/option[2]').text
        for i in range(1, len(trs)):
            tr = trs[i]
            tds = [td for td in tr.children]
            # print(tds)
            Player = tds[1].find('span','name').text
            Game = tds[5].text
            if int(Game) < 15 :  #設定出賽數達指定條件之球員才進行儲存
                continue
            AVG = tds[3].text
            PA = tds[7].text
            AB = tds[9].text
            R = tds[11].text
            RBI = tds[13].text
            H = tds[15].text
            H1 = tds[17].text
            H2 = tds[19].text
            H3 = tds[21].text
            HR = tds[23].text
            TB = tds[25].text
            BB = tds[29].text
            HBP = tds[33].text
            K = tds[35].text
            DP = tds[37].text
            SH = tds[39].text
            SF = tds[41].text
            SB = tds[43].text
            CS = tds[45].text
            OBP = tds[47].text
            SLG = tds[49].text
            OPS = tds[51].text
            GF = tds[53].text
            IsoP = float(SLG) - float(AVG)
            IsoD = float(OBP) - float(AVG)
            SOpercent = round(float(K) / float(PA), 3)
            BBpercent = round(float(BB) / float(PA), 3)
            BIPpercnt = round(
                (float(AB) - float(K) - float(HR) + float(SF)) / (float(AB) + float(BB) + float(HBP) + float(SF)), 3)
            BABIP = round((float(H) - float(HR)) / (float(AB) - float(K) - float(HR) + float(SF)), 3)
            XBH = round((float(H2) + float(H3) + float(HR)) / float(H), 3)
            SecA = round((float(BB) + float(TB) - float(H) + float(SB) - float(CS)) / float(AB), 3)
            KBB = round(float(BB)/float(K),3)
            Name = Player+Position
            print("球員名:%s 出賽數:%s 打擊率:%s" % (Player,Game,AVG))
            cur.execute('insert into Position_Batter(PBatter_Position,PBatter_name , PBatter_YearTeam , PBatter_Game, PBatter_PA, PBatter_AB, PBatter_R,'
                        'PBatter_RBI,PBatter_K, '
                        'PBatter_BB,PBatter_HBP,PBatter_SF,PBatter_SH,PBatter_H,PBatter_H1,PBatter_H2,PBatter_H3,PBatter_HR,'
                        'PBatter_TB,PBatter_AVG,PBatter_OBP, '
                        'PBatter_SLG,PBatter_OPS,PBatter_SB,PBatter_CS,PBatter_GF,PBatter_Isop,PBatter_IsoD,PBatter_SOpercent,'
                        'PBatter_BBpercent,PBatter_BIPpercent, '
                        'PBatter_BABIP,PBatter_XBH,PBatter_SecA,PBatter_KBB) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'
                        '?,?,?,?,?,?,?,?)',
                        (
                        Position,Name, Year, Game, PA, AB, R, RBI, K, BB, HBP, SF, SH, H, H1, H2, H3, HR, TB, AVG, OBP, SLG, OPS,
                        SB, CS, GF, IsoP, IsoD, SOpercent, BBpercent, BIPpercnt, BABIP, XBH, SecA, KBB))
            conn.commit()


finally:
    chrome.quit()
    conn.close()
