import requests
from bs4 import BeautifulSoup
import time

# Token dan ID Channel
TOKEN = '7580988527:AAGgK5S3iF4gISAhqtNQLOMnXoJl0gDYPcw'  # Ganti dengan token bot Anda
CHANNEL_ID = '-1002393238668'  # Ganti dengan username atau ID channel Anda

# URL untuk memeriksa kuota KKN
URL = 'https://kkn.unsoed.ac.id/?KuotaKknSearch%5Bkode_fak%5D=H&KuotaKknSearch%5Bjenis_kkn_id%5D=1&KuotaKknSearch%5Bnegara_id%5D=&KuotaKknSearch%5Bkecamatan_id%5D=&KuotaKknSearch%5Bkuota%5D=&KuotaKknSearch%5Bterisi%5D='

def send_telegram_message(message):
    """
    Mengirim pesan ke channel Telegram.
    """
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHANNEL_ID, 'text': message, 'parse_mode': 'HTML'}
    response = requests.post(url, data=payload)
    return response

def check_kuota():
    """
    Memeriksa ketersediaan kuota KKN dan mengirimkan informasi ke channel jika ada slot tersedia.
    """
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    rows = soup.select('table tr')

    available_slots = []

    for row in rows[2:]:  # Melewati header
        cols = row.find_all('td')
        if len(cols) < 12:
            continue
        kuota = cols[9].text.strip()
        terisi = cols[10].text.strip()
        status = cols[11].text.strip()

        if status.lower() != 'penuh':
            lokasi = cols[8].text.strip()
            available_slots.append(f"📍 <b>Lokasi:</b> {lokasi}\n     Kuota: {kuota} | Terisi: {terisi}")

    if available_slots:
        message = "🔔 <b>Kuota KKN Teknik TERSEDIA!</b>\n\n" + "\n\n".join(available_slots)
        send_telegram_message(message)
        print("Ditemukan slot kosong dan pesan telah dikirim.")
    else:
        print("Tidak ada slot tersedia saat ini.")

while True:
    try:
        check_kuota()
        time.sleep(180)
    except Exception as e:
        print("Error:", e)
        time.sleep(180)
