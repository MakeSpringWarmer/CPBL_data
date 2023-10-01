import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_df(url,target_team):

  #url = 'http://cpbl.com.tw/team/dailyrecord?ClubNo=AEO'

  # 發送GET請求
  response = requests.get(url)

  # 檢查請求是否成功
  if response.status_code == 200:
      # 使用BeautifulSoup解析HTML
      soup = BeautifulSoup(response.text, 'html.parser')

      # 找到目標div元素
      div = soup.find('div', {'class': 'RecordTable'})

      # 檢查是否找到div元素
      if div:
          # 使用Pandas的read_html函式直接將表格轉換為DataFrame
          table = div.find('table')
          df = pd.read_html(str(table))[0]

          # 將比賽時間轉換為分鐘表示
          time_pattern = r'(\d+)H(\d+)M'
          df['比賽時間（分鐘）'] = df['比賽時間'].apply(lambda x: int(re.search(time_pattern, x).group(1)) * 60 +int(re.search(time_pattern, x).group(2)))

          df['比賽結果'] = df.apply(lambda row: '勝' if row['勝隊'] == target_team
                                  else '和' if pd.isnull(row['勝隊'])
                                  else '負', axis=1)



          #target_team = '富邦悍將'  # 要判斷的特定隊伍名稱
          df['得分結果'] = df.apply(lambda row: row['得分'] if row['客隊'] == target_team
                                          else row['得分.1'] if row['主隊'] == target_team
                                          else None, axis=1)

          df['失分結果'] = df.apply(lambda row: row['得分'] if row['主隊'] == target_team
                                          else row['得分.1'] if row['客隊'] == target_team
                                          else None, axis=1)

          df['主客場'] = df.apply(lambda row: '主場' if row['主隊'] == target_team
                                  else '客場', axis=1)

          # 將日期欄位轉換為datetime格式
          df['日期'] = pd.to_datetime(df['日期'], format='%Y/%m/%d')

          df['得失分差'] = df['得分結果'] - df['失分結果']

          df['主客場'] = df.apply(lambda row: '主場' if row['主隊'] == target_team
                                  else '客場', axis=1)


          return df


      else:
          print('未找到目標div元素')
          return 0
  else:
      print('請求失敗')
      return 0