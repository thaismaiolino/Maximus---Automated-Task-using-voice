# import pyttsx
#
# import unicodedata
#
# engine = pyttsx.init()
# # engine.setProperty('voice', 'com.apple.speech.synthesis.voice.daniel')
# engine.setProperty('voice', 'com.apple.speech.synthesis.voice.luciana') ## TOP 10
# engine.say('Obrigada meu amorzinho')
# engine.runAndWait()

import requests
r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Niteroi,br=524901&APPID=14f212cb0456519d72374ff4c1f2ad31')
print r.json()