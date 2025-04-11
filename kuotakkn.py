import requests
from bs4 import BeautifulSoup
import time

TOKEN = '8014051915:AAHUjqv6HolPnXUlFdNwKLw299OLdmVOpGk'
CHAT_ID = '8014051915'
URL = 'https://kkn.unsoed.ac.id/?KuotaKknSearch%5Bkode_fak%5D=H&KuotaKknSearch%5Bjenis_kkn_id%5D=1&KuotaKknSearch%5Bnegara_id%5D=&KuotaKknSearch%5Bkecamatan_id%5D=&KuotaKknSearch%5Bkuota%5D=&KuotaKknSearch%5Bterisi%5D='

# Variabel global untuk menyimpan message_id terakhir
last_message_id = None

def send_telegram_message(message):
    """
    Mengirim pesan ke channel Telegram dan mengembalikan message_id.
    """
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
    response = requests.post(url, data=payload)
    response_json = response.json()
    
    if response.status_code == 200:
        return response_json.get('result', {}).get('message_id')
    else:
        error_code = response_json.get('error_code')
        description = response_json.get('description')
        print(f"Error {error_code}: {description}")
        return None

def delete_telegram_message(message_id):
    """
    Menghapus pesan dari channel Telegram berdasarkan message_id.
    """
    url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage"
    payload = {'chat_id': CHANNEL_ID, 'message_id': message_id}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        response_json = response.json()
        print(f"Failed to delete message {message_id}: {response_json.get('description')}")
        return False
    print(f"Deleted old message: {message_id}")
    return True

def check_kuota():
    """
    Memeriksa ketersediaan kuota KKN dan mengirimkan informasi ke channel jika ada slot tersedia.
    """
    global last_message_id
    
    try:
        res = requests.get(URL)
        soup = BeautifulSoup(res.text, 'html.parser')
        rows = soup.select('table tr')

        available_slots = []

        for row in rows[2:]:
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
            # Format pesan
            message = "🔔 <b>Kuota KKN Teknik TERSEDIA!</b>\n\n" + "\n\n".join(available_slots)
            
            # PENTING: Hapus pesan lama SEBELUM mengirim pesan baru
            if last_message_id:
                delete_success = delete_telegram_message(last_message_id)
                if not delete_success:
                    print(f"Warning: Couldn't delete previous message ID: {last_message_id}")
                # Reset last_message_id hanya jika penghapusan berhasil
                if delete_success:
                    last_message_id = None
            
            # Kirim pesan baru setelah pesan lama dihapus
            new_message_id = send_telegram_message(message)
            if new_message_id:
                last_message_id = new_message_id
                print(f"Ditemukan slot kosong dan pesan telah dikirim. Message ID: {new_message_id}")
        else:
            print("Tidak ada slot tersedia saat ini.")
    except Exception as e:
        print(f"Error dalam check_kuota: {e}")

def main():
    print("Bot KKN Monitoring dimulai...")
    while True:
        try:
            check_kuota()
            time.sleep(30)  
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()