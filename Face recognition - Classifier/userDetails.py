import platform
import requests
#import telegram


TELEGRAM_BOT_TOKEN = '5535933470:AAFWP__W6-1fAxqrCQbE2QTXFDygnZhFnN8'
TELEGRAM_CHAT_ID = '-696427975'


print("="*40, "System Information", "="*40)
uname = platform.uname()
print(f"System: {uname.system}")
print(f"Node Name: {uname.node}")
print(f"Release: {uname.release}")
print(f"Version: {uname.version}")
print(f"Machine: {uname.machine}")
print(f"Processor: {uname.processor}")

#-- Network information
print("="*40, "User Informations", "="*40)
response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=926c0917bf5e42fda8e40569e5c796fb")
print(response.status_code)
print(response.content)

#def alertMessage() :
#    print("="*40, "User", "="*40)
#    message =  "\n{\n" f"System: {uname.system}\nNode Name: {uname.node}\nRelease: {uname.release}\nVersion: {uname.version}\nMachine: {uname.machine}\nProcessor: {uname.processor}" + "\n}"
#    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

#message =  "{\n" + "="*3 + "User Informations" + "="*3 + f"\nSystem: {uname.system}\nNode Name: {uname.node}\nRelease: {uname.release}\nVersion: {uname.version}\nMachine: {uname.machine}\nProcessor: {uname.processor}" + f"{response.status_code}" + f"{response.content}" +"\n}"
#bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

#bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
