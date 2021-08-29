from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sqlite3

#此程式用於爬取指定野手各年度於一軍之打擊基礎、進階數據並存放於SQLite資料庫中

conn = sqlite3.connect("D:/CPBL_Data/batter.db")
cur = conn.cursor()
try:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    chrome = webdriver.Chrome(options=options, executable_path="D:/CPBL_Data/chromedriver.exe")

    chrome.set_page_load_timeout(10)
    chrome.get('https://www.cpbl.com.tw/team/person?Acnt=0000004634')

    # print(chrome.find_element_by_xpath('//*[@id="Content"]/div[3]/div/div/dl/dt/div[2]').text)

    player = chrome.find_element_by_xpath('//*[@id="Content"]/div[3]/div/div/dl/dt/div[2]').text
    chrome.find_element_by_xpath('//*[@id="bindVue"]/div[1]/div/div[1]/select/option[6]').click()
    time.sleep(2)
    chrome.find_element_by_xpath('//*[@id="bindVue"]/div[1]/div/div[2]/input').click()

    time.sleep(2)
    soup = BeautifulSoup(chrome.page_source, 'html5lib')
    trs = soup.find("div","RecordTable").find('table').find_all("tr")
    print("球員:%s" % player)
    for i in range(1, len(trs)):
        tr = trs[i]
        tds = [td for td in tr.children]
        YearTeam = tds[0].text
        Game = tds[2].text
        R = tds[10].text
        RBI = tds[8].text
        AB = tds[6].text
        PA = tds[4].text
        H = tds[12].text
        AVG = tds[32].text
        SLG = tds[30].text
        OBP = tds[28].text
        K = tds[24].text
        OPS = tds[56].text
        BB = tds[40].text
        HBP = tds[44].text
        SF = tds[38].text
        SH = tds[36].text
        H1 = tds[14].text
        H2 = tds[16].text
        H3 = tds[18].text
        HR = tds[20].text
        GF = tds[52].text
        TB = tds[22].text
        SB = tds[26].text
        CS = tds[46].text
        IsoP = float(SLG)-float(AVG)
        IsoD = float(OBP)-float(AVG)
        SOpercent = round(float(K)/float(PA),3)
        BBpercent = round(float(BB)/float(PA),3)
        BIPpercnt = round((float(AB)-float(K)-float(HR)+float(SF))/(float(AB)+float(BB)+float(HBP)+float(SF)),3)
        BABIP = round((float(H)-float(HR))/(float(AB)-float(K)-float(HR)+float(SF)),3)
        XBH = round((float(H2)+float(H3)+float(HR))/float(H),3)
        SecA = round((float(BB)+float(TB)-float(H)+float(SB)-float(CS))/float(AB),3)
        KBB = round(float(BB)/float(K),3)
        Name = player+"_"+YearTeam
        cur.execute('insert into Second_Batter(SBatter_name , SBatter_YearTeam , SBatter_Game,SBatter_PA,SBatter_AB,SBatter_R,'
                    'SBatter_RBI,SBatter_K, '
                    'SBatter_BB,SBatter_HBP,SBatter_SF,SBatter_SH,SBatter_H,SBatter_H1,SBatter_H2,SBatter_H3,SBatter_HR,'
                    'SBatter_TB,SBatter_AVG,SBatter_OBP, '
                    'SBatter_SLG,SBatter_OPS,SBatter_SB,SBatter_CS,SBatter_GF,SBatter_Isop,SBatter_IsoD,SBatter_SOpercent,'
                    'SBatter_BBpercent,SBatter_BIPpercent, '
                    'SBatter_BABIP,SBatter_XBH,SBatter_SecA,SBatter_KBB) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'
                    '?,?,?,?,?,?,?,?)',
                    (Name,YearTeam,Game,PA,AB,R,RBI,K,BB,HBP,SF,SH,H,H1,H2,H3,HR,TB,AVG,OBP,SLG,OPS,SB,CS,GF,IsoP,IsoD,SOpercent,BBpercent,BIPpercnt,BABIP,XBH,SecA,KBB))
        conn.commit()

        print(YearTeam)
        print("  打席:%s 打數:%s 安打:%s 打擊率:%s 上壘率:%s 長打率:%s 純長打率:%f 純上壘率:%f 被三振率:%f 得四壞率:%f 擊入場內率:%f 場內打擊率:%f 長打比率:%f 第二打擊率:%f 保送三振比:%f"
              % ( PA, AB, H , AVG ,OBP ,SLG,IsoP,IsoD,SOpercent,BBpercent,BIPpercnt,BABIP,XBH,SecA,KBB))

finally:
    chrome.quit()
    conn.close()
