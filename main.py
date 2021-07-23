import telebot
import pandas as pd
from cowin_api import CoWinAPI
from nsetools import Nse

API_KEY='1'

bot = telebot.TeleBot(API_KEY)

print("**Bot initiated**")
#Bot Start

@bot.message_handler(commands=['start'])
def greet(message):
  bot.send_message(message.chat.id, "Hi, Welcome to Dial Me Now, how can I help you? \n Enter /cowin for Vaccination Slots Availability \n Enter /happy for World Happiness Report \n Enter /stock for Stock Price")


#Cowin Slots
@bot.message_handler(commands=['cowin'])
def cowin(message):
  bot.send_message(message.chat.id,"Enter command as *district district name* for example *district Jaipur I*",parse_mode="Markdown")

def slot_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "district":
    return False
  else:
    return True
@bot.message_handler(func=slot_request)
def slot_name(message):
  try:
    request = message.text.split()
    if request[1]=='Jaipur' or request[1]=='jaipur':
      request="Jaipur "+request[2]
      response=''
      count=1
      coApi = CoWinAPI()
      dis_id=''
      if request=='Jaipur II':
        dis_id='506'
      else:
        dis_id = '505'
      available_centers = coApi.get_availability_by_district(dis_id)
      for j in available_centers['centers']:
        if j['block_name']==request+' Urban':
          response += str(count) + '. Center Name: ' + j['name'] + ', Address: ' + j['address'] + ', Block Name: ' + j[
            'block_name'] + '\n'
          count += 1
      print(response)
      bot.send_message(message.chat.id, response)
    else:
      response = ''
      count=1
      district= request[1].capitalize()
      coApi=CoWinAPI()
      all_districts_raj = coApi.get_districts(state_id='29')
      for i in all_districts_raj['districts']:
        if district in i['district_name']:
          dis_id = i['district_id']
      available_centers = coApi.get_availability_by_district(str(dis_id))
      for j in available_centers['centers']:
        response += str(count)+'. Center Name: ' + j['name'] + ', Address: '+j['address']+', Block Name: '+j['block_name']+'\n'
        count += 1
      print(response)
      bot.send_message(message.chat.id, response)
  except:
    bot.send_message(message.chat.id,'No Data Found')

# World Happiness Report
@bot.message_handler(commands=['happy'])
def happy(message):
  bot.send_message(message.chat.id,"Enter command as *country country name* for example *country India*",parse_mode="Markdown")

def happy_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "country":
    return False
  else:
    return True
@bot.message_handler(func=happy_request)
def happy_report(message):
  try:
    df= pd.read_csv('world-happiness-report-2021.csv')
    request = message.text.split()
    country=request[1]
    rank = list(df.loc[df['Country name'] == country].index)
    response= request[1]+' ranked '+str(rank[0] + 1)+' on World Happiness Report'
    print(response)
    bot.send_message(message.chat.id, response)
  except:
    bot.send_message(message.chat.id, 'No Data Found try new')

def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "stock":
    return False
  else:
    return True

@bot.message_handler(commands=['stock'])
def stock_message(message):
  bot.send_message(message.chat.id,"Enter command as *stock stock symbol* for example *stock INFY*",parse_mode="Markdown")
@bot.message_handler(func=stock_request)

def stock_price(message):
  try:
    request=message.text.split()
    nse = Nse()
    q = nse.get_quote(request[1])
    response='Last price of '+ q['companyName'] +' (' + q['symbol']+') '+ 'was '+str(q['lastPrice'])
    print(response)
    bot.send_message(message.chat.id, response)
  except:
    bot.send_message(message.chat.id, 'Something is wrong please try again')



bot.polling()
