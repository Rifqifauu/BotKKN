import requests
from bs4 import BeautifulSoup
import time

TOKEN = '7580988527:AAGgK5S3iF4gISAhqtNQLOMnXoJl0gDYPcw'
CHAT_ID = '7456474633'

URL = 'https://kkn.unsoed.ac.id/site/index?KuotaKknSearch%5Bkode_fak%5D=H&KuotaKknSearch%5Bjenis_kkn_id%5D=1&KuotaKknSearch%5Bnegara_id%5D=&KuotaKknSearch%5Bkecamatan_id%5D=&KuotaKknSearch%5Bkuota%5D=&KuotaKknSearch%5Bterisi%5D='

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=payload)

def check_kuota():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    rows = soup.select('table tr')

    for row in rows[2:]:  # skip header
        cols = row.find_all('td')
        if len(cols) < 9:
            continue
        kuota = cols[9].text.strip()
        terisi = cols[10].text.strip()
        status = cols[11].text.strip()

        if status.lower() != 'penuh':
            lokasi = cols[8].text.strip()
            message = f"🔔 Kuota KKN Teknik TERSEDIA!\n📍 Lokasi: {lokasi}\nKuota: {kuota} | Terisi: {terisi}"
            send_telegram_message(message)
            print("Ditemukan slot kosong!")

while True:
    try:
        check_kuota()
        time.sleep(60)  # cek setiap 60 detik
    except Exception as e:
        print("Error:", e)
        time.sleep(60)
