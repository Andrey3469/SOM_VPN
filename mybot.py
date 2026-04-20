import telebot
from telebot import types
from telebot import apihelper
import time
import json
import os
import random
import string
from datetime import datetime, timedelta

# ============ НАСТРОЙКИ ============
apihelper.proxy = {}

TOKEN = '8794961428:AAHatXUGU00TgirKwebRgtxbpG12lVvfeTw'
ADMIN_ID = 5195664540
WALLET_NUMBER = '410119498554165'
CHANNEL_ID = '@SOM_VPN69'

# ССЫЛКИ ДЛЯ ПРОВЕРКИ
# ПЕРВЫЙ БОТ (ipcorp_bot)
BOT1_USERNAME = 'ipcorp_bot'
BOT1_START_CODE = 'r01923772967'
BOT1_LINK = f"https://t.me/{BOT1_USERNAME}?start={BOT1_START_CODE}"

# ВТОРОЙ БОТ (Excellentbot_bot)
BOT2_USERNAME = 'Excellentbot_bot'
BOT2_START_CODE = '01923772967'
BOT2_LINK = f"https://t.me/{BOT2_USERNAME}?start={BOT2_START_CODE}"
# VPN-ключи
VPN_KEYS = """vless://ea4b12cf-7b8b-4ec3-852d-39943450c7e3@109.120.191.246:555?encryption=none&flow=xtls-rprx-vision&security=reality&sni=max.ru&fp=qq&pbk=pF1OwseXc7K9qhmUt0uLv7kjM0Lp8X4WKIvZQemePXM&sid=def112&spiderX=%2FavoaKWnQIasasdrasdfUvi#Som%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4 
vless://ea4b12cf-7b8b-4ec3-852d-39943450c7e3@45.145.40.2:8443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=max.ru&fp=chrome&pbk=iITd4I5MlZT0vgdiZHMAO36rS7GG-useUAoG85hJrVg&sid=ab2729898c949868#%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%20Wifi
vless://ea4b12cf-7b8b-4ec3-852d-39943450c7e3@217.16.25.104:8444?encryption=none&flow=xtls-rprx-vision&security=reality&sni=yandex.ru&fp=chrome&pbk=GTH4GeyF9LRf97UiNpwgYIpDLYIFFgBFQeptYH7t0lg&sid=571d7da65a310fce#%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%202
vless://ea4b12cf-7b8b-4ec3-852d-39943450c7e3@109.120.191.246:5555?encryption=none&flow=xtls-rprx-vision&security=reality&sni=max.ru&fp=qq&pbk=pF1OwseXc7K9qhmUt0uLv7kjM0Lp8X4WKIvZQemePXM&sid=def112&spiderX=%2FavoaKWnQIasasdrasdUvi#%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%203 
vless://ea4b12cf-7b8b-4ec3-852d-39943450c7e3@109.120.181.195:8443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=yandex.ru&fp=qq&pbk=pF1OwseXc7K9qhmUt0uLv7kjM0Lp8X4WKIvZQemePXM&sid=901bcd&spiderX=%2FavoaKWnQIasasdrasdfUvi#%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%204
vless://ea4b12cf-7b8b-4ec3-852d-39943450c7e3@109.120.183.179:8443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=yandex.ru&fp=qq&pbk=GuFysx_LybQZUUKDfRlJFexg9EPJePX5aigQVQsEkRI&sid=0f08794fe3843da5#%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%205
vless://ea4b12cf-7b8b-4ec3-852d-39943450c7e3@51.250.84.229:8443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=yandex.ru&fp=chrome&pbk=GuFysx_LybQZUUKDfRlJFexg9EPJePX5aigQVQsEkRI&sid=0f08794fe3843da5#%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%206
vless://ea4b12cf-7b8b-4ec3-852d-39943450c7e3@ru51.kotvpn.net:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=max.ru&fp=qq&pbk=o7NN7G_0EYlNqfrTOoSTPUcJPnXEPo5AYct4Kb64aUY&sid=91da4ef59542fa99#%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%207
vless://ea4b12cf-7b8b-4ec3-852d-39943450c7e3@217.16.31.243:8443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=max.ru&fp=qq&pbk=2DN6m4Q0Oi-jbdSpfnNymoyZw1Yiim2HEh1H1ozcgU0&sid=4a3da5d94540bc1a#%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%208
vless://ea4b12cf-7b8b-4ec3-852d-39943450c7e3@ru84yandex.kotvpn.net:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=max.ru&fp=qq&pbk=vI68ANz2jG9BI1PD2TziWkblvMVHV82ltGL1ECCunkY&sid=7f9170f4b8efe0ca#%D0%BE%D0%B1%D1%85%D0%BE%D0%BE%D0%B4%209 
vless://ea4b12cf-7b8b-4ec3-852d-39943450c7e3@217.16.31.251:8443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=yandex.ru&fp=qq&pbk=AU1EqYuQyoJ5eBPPby3ph-20QtVBpyIeOUQ3kgOfAkA&sid=9371df93ea8bb310#%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%2010
vless://ea4b12cf-7b8b-4ec3-852d-39943450c7e3@217.16.25.104:8443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=yandex.ru&fp=qq&pbk=V6bdUQVTHkh6F1asP9mqiKMQcycOJdZjMVqEEM7IiVY&sid=b5d00e7e5328804#%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%2011 
vless://ea4b12cf-7b8b-4ec3-852d-39943450c7e3@217.16.25.104:8444?encryption=none&flow=xtls-rprx-vision&security=reality&sni=yandex.ru&fp=qq&pbk=GTH4GeyF9LRf97UiNpwgYIpDLYIFFgBFQeptYH7t0lg&sid=571d7da65a310fce#%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%2012"""

bot = telebot.TeleBot(TOKEN)
user_payments = {}
promocodes = {}

# Файлы для хранения данных
DATA_FILE = 'payments.json'
PROMO_FILE = 'promocodes.json'

def load_data():
    global user_payments
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                user_payments = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Файл payments.json повреждён. Создаю новый...")
            user_payments = {}
            save_data()
    else:
        user_payments = {}

def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(user_payments, f, ensure_ascii=False, indent=2)

def load_promos():
    global promocodes
    if os.path.exists(PROMO_FILE):
        try:
            with open(PROMO_FILE, 'r', encoding='utf-8') as f:
                promocodes = json.load(f)
                for code, data in promocodes.items():
                    if 'max_uses' not in data:
                        data['max_uses'] = 1
                    if 'used_count' not in data:
                        data['used_count'] = len(data.get('used_by', []))
                    if 'used_by' not in data:
                        data['used_by'] = []
            save_promos()
        except json.JSONDecodeError:
            print("⚠️ Файл promocodes.json повреждён. Создаю новый...")
            promocodes = {}
            save_promos()
    else:
        promocodes = {}

def save_promos():
    with open(PROMO_FILE, 'w', encoding='utf-8') as f:
        json.dump(promocodes, f, ensure_ascii=False, indent=2)

load_data()
load_promos()

# ============ ПРОВЕРКА ДОСТУПА ============
def has_access(user_id):
    user_data = user_payments.get(str(user_id), {})
    return user_data.get('has_access', False)

def grant_access(user_id):
    user_data = user_payments.get(str(user_id), {})
    user_data['has_access'] = True
    user_payments[str(user_id)] = user_data
    save_data()

def block_user(user_id):
    """Отзывает доступ у пользователя"""
    user_id_str = str(user_id)
    if user_id_str in user_payments:
        user_payments[user_id_str]['has_access'] = False
        save_data()
        return True
    return False

def unblock_user(user_id):
    """Восстанавливает доступ пользователя"""
    user_id_str = str(user_id)
    if user_id_str in user_payments:
        user_payments[user_id_str]['has_access'] = True
        save_data()
        return True
    return False

# ============ ОТПРАВКА УВЕДОМЛЕНИЯ АДМИНУ ============
def send_access_request_to_admin(user_id, username):
    admin_text = f"""🔔 **НОВЫЙ ЗАПРОС НА ДОСТУП!**

👤 Пользователь: @{username or 'нет username'}
🆔 ID: `{user_id}`

📌 **Действия:**
1. Проверьте, перешёл ли пользователь по ссылкам:
   • {BOT1_LINK}
   • {BOT2_LINK}
2. Если да — выдайте доступ командой:
   `/grant {user_id}`

❌ Если нет — попросите перейти по ссылкам и нажать «ПОЛУЧИТЬ ДОСТУП» снова."""
    
    try:
        bot.send_message(ADMIN_ID, admin_text, parse_mode='Markdown')
    except Exception as e:
        print(f"Ошибка отправки уведомления админу: {e}")

# ============ КОМАНДЫ АДМИНИСТРАТОРА ============
@bot.message_handler(commands=['grant'])
def grant_access_command(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❌ Использование: /grant USER_ID\n\nПример: /grant 5195664540")
        return
    
    user_id = parts[1]
    
    try:
        grant_access(user_id)
        bot.reply_to(message, f"✅ Доступ выдан пользователю {user_id}")
        
        try:
            bot.send_message(
                int(user_id),
                f"🎉 Администратор выдал вам доступ к боту!\n\n"
                f"🏆 Теперь вы можете пользоваться VPN-ботом.\n"
                f"Нажмите /start, чтобы начать."
            )
        except:
            pass
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['block'])
def block_command(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❌ Использование: /block USER_ID\n\nПример: /block 5195664540")
        return
    
    user_id = parts[1]
    
    if block_user(user_id):
        bot.reply_to(message, f"✅ Доступ пользователя {user_id} отозван")
        try:
            bot.send_message(int(user_id), "🚫 Ваш доступ к боту отозван администратором.")
        except:
            pass
    else:
        bot.reply_to(message, f"❌ Пользователь {user_id} не найден в базе")

@bot.message_handler(commands=['unblock'])
def unblock_command(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❌ Использование: /unblock USER_ID\n\nПример: /unblock 5195664540")
        return
    
    user_id = parts[1]
    
    if unblock_user(user_id):
        bot.reply_to(message, f"✅ Доступ пользователя {user_id} восстановлен")
        try:
            bot.send_message(int(user_id), "✅ Ваш доступ к боту восстановлен! Нажмите /start")
        except:
            pass
    else:
        bot.reply_to(message, f"❌ Пользователь {user_id} не найден в базе")

@bot.message_handler(commands=['createpromo'])
def create_promo(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 5:
            bot.reply_to(message, "❌ /createpromo forever discount 100 10")
            return
        
        tariff = parts[1].lower()
        promo_type = parts[2].lower()
        value = int(parts[3]) if parts[3].isdigit() else 0
        max_uses = int(parts[4]) if parts[4].isdigit() else 1
        
        promo_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        promocodes[promo_code] = {
            'tariff': tariff,
            'type': promo_type,
            'value': value,
            'max_uses': max_uses,
            'used_count': 0,
            'used_by': []
        }
        save_promos()
        bot.reply_to(message, f"✅ Промокод: {promo_code}")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['listpromos'])
def list_promos(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    if not promocodes:
        bot.reply_to(message, "📭 Нет промокодов")
        return
    
    text = "🎫 ПРОМОКОДЫ:\n\n"
    for code, data in promocodes.items():
        remaining = data['max_uses'] - data['used_count']
        text += f"📌 {code}\n   Осталось: {remaining}/{data['max_uses']}\n\n"
    bot.reply_to(message, text)

@bot.message_handler(commands=['deletepromo'])
def delete_promo(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❌ /deletepromo КОД")
        return
    
    promo_code = parts[1].upper()
    if promo_code in promocodes:
        del promocodes[promo_code]
        save_promos()
        bot.reply_to(message, f"✅ Удалён")
    else:
        bot.reply_to(message, "❌ Не найден")

@bot.message_handler(commands=['users'])
def list_users(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    active = []
    for user_id, data in user_payments.items():
        if data.get('paid', False):
            active.append(f"👤 {user_id} - {data.get('type', '?')}")
    
    if active:
        bot.reply_to(message, "👥 АКТИВНЫЕ:\n" + "\n".join(active))
    else:
        bot.reply_to(message, "📭 Нет активных")

@bot.message_handler(commands=['userinfo'])
def user_info(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❌ /userinfo USER_ID")
        return
    
    user_id = parts[1]
    
    if user_id not in user_payments:
        bot.reply_to(message, f"❌ Пользователь {user_id} не найден")
        return
    
    data = user_payments[user_id]
    text = f"📊 ПОЛЬЗОВАТЕЛЬ {user_id}:\n"
    text += f"Тариф: {data.get('type', '?')}\n"
    text += f"Статус подписки: {'Активна' if data.get('paid') else 'Не активна'}\n"
    text += f"Доступ к боту: {'✅ Да' if data.get('has_access') else '❌ Нет'}\n"
    if data.get('expires_at'):
        expires_str = datetime.fromtimestamp(data['expires_at']).strftime('%d.%m.%Y %H:%M')
        text += f"Подписка до: {expires_str}"
    bot.reply_to(message, text)

@bot.message_handler(commands=['give'])
def give_subscription(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    parts = message.text.split()
    if len(parts) < 4:
        bot.reply_to(message, "❌ /give USER_ID ТАРИФ ДНЕЙ")
        return
    
    user_id = parts[1]
    tariff = parts[2].lower()
    days = int(parts[3])
    
    expires_at = None
    if days > 0:
        expires_at = time.time() + (days * 86400)
    
    grant_access(user_id)
    
    user_payments[user_id] = {
        'type': tariff,
        'paid': True,
        'expires_at': expires_at,
        'admin_given': True,
        'has_access': True
    }
    save_data()
    
    expires_str = datetime.fromtimestamp(expires_at).strftime('%d.%m.%Y %H:%M') if expires_at else "бессрочно"
    bot.reply_to(message, f"✅ Выдана подписка {user_id} до {expires_str}")
    
    try:
        bot.send_message(int(user_id), f"🎉 Администратор выдал вам подписку!\n📅 До: {expires_str}\n\nНажмите /start, чтобы начать пользоваться ботом.")
    except:
        pass

@bot.message_handler(commands=['end'])
def end_subscription(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❌ /end USER_ID")
        return
    
    user_id = parts[1]
    
    if user_id not in user_payments:
        bot.reply_to(message, f"❌ Пользователь {user_id} не найден")
        return
    
    user_payments[user_id]['paid'] = False
    save_data()
    bot.reply_to(message, f"✅ Подписка {user_id} завершена")

@bot.message_handler(commands=['extend'])
def extend_subscription(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    parts = message.text.split()
    if len(parts) < 3:
        bot.reply_to(message, "❌ /extend USER_ID ДНЕЙ")
        return
    
    user_id = parts[1]
    days = int(parts[2])
    
    if user_id not in user_payments:
        bot.reply_to(message, f"❌ Пользователь {user_id} не найден")
        return
    
    current_expires = user_payments[user_id].get('expires_at', time.time())
    new_expires = max(current_expires, time.time()) + (days * 86400)
    user_payments[user_id]['expires_at'] = new_expires
    user_payments[user_id]['paid'] = True
    save_data()
    
    expires_str = datetime.fromtimestamp(new_expires).strftime('%d.%m.%Y %H:%M')
    bot.reply_to(message, f"✅ Продлено до {expires_str}")

@bot.message_handler(commands=['pending'])
def show_pending(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    pending = []
    for user_id, data in user_payments.items():
        if not data.get('paid', False) and data.get('amount', 0) > 0:
            pending.append(f"👤 {user_id} - {data['amount']}₽")
    
    if pending:
        bot.reply_to(message, "⏳ ОЖИДАЮТ:\n" + "\n".join(pending))
    else:
        bot.reply_to(message, "✅ Нет ожидающих")

@bot.message_handler(commands=['approve'])
def approve_payment(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ /approve USER_ID [дни]")
            return
        
        user_id = parts[1]
        days = int(parts[2]) if len(parts) > 2 else 30
        
        if user_id not in user_payments:
            bot.reply_to(message, f"❌ Платёж для {user_id} не найден")
            return
        
        if user_payments[user_id].get('paid', False):
            bot.reply_to(message, f"✅ Платёж для {user_id} уже подтверждён")
            return
        
        expires_at = time.time() + (days * 86400)
        
        user_payments[user_id]['paid'] = True
        user_payments[user_id]['expires_at'] = expires_at
        user_payments[user_id]['approved_at'] = time.time()
        save_data()
        
        expires_str = datetime.fromtimestamp(expires_at).strftime('%d.%m.%Y %H:%M')
        
        markup = types.InlineKeyboardMarkup()
        btn_menu = types.InlineKeyboardButton('🔙 В главное меню', callback_data='main_menu')
        markup.add(btn_menu)
        
        try:
            bot.send_message(
                int(user_id),
                f"✅ Ваш платеж подтверждён!\n\n"
                f"📦 Тариф: {user_payments[user_id]['type']}\n"
                f"📅 Действует до: {expires_str}\n\n"
                f"🔑 ВАШИ VPN-КЛЮЧИ (скопируйте любой):\n\n"
                f"{VPN_KEYS}\n\n"
                f"📖 Инструкция: скачайте Happ → + → Импорт из буфера",
                reply_markup=markup
            )
            bot.reply_to(message, f"✅ Все ключи отправлены пользователю {user_id}")
        except Exception as e:
            bot.reply_to(message, f"❌ Ошибка отправки: {e}")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['reject'])
def reject_payment(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ /reject USER_ID [причина]")
            return
        
        user_id = parts[1]
        reason = " ".join(parts[2:]) if len(parts) > 2 else "Не указана"
        
        if user_id not in user_payments:
            bot.reply_to(message, f"❌ Платёж не найден")
            return
        
        user_payments[user_id]['rejected'] = True
        save_data()
        
        try:
            bot.send_message(int(user_id), f"❌ Ваш платёж отклонён!\nПричина: {reason}")
            bot.reply_to(message, f"✅ Отклонён")
        except:
            bot.reply_to(message, f"✅ Отклонён")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    total_users = len(user_payments)
    active_users = 0
    has_access_count = 0
    
    for user_id, data in user_payments.items():
        if data.get('paid', False):
            expires = data.get('expires_at')
            if not expires or expires > time.time():
                active_users += 1
        if data.get('has_access', False):
            has_access_count += 1
    
    text = f"📊 СТАТИСТИКА:\n\n"
    text += f"👥 Всего: {total_users}\n"
    text += f"✅ Активных подписок: {active_users}\n"
    text += f"🔓 Имеют доступ: {has_access_count}\n"
    text += f"🎫 Промокодов: {len(promocodes)}\n"
    text += f"💳 Кошелек: {WALLET_NUMBER}"
    bot.reply_to(message, text)

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "❌ /broadcast ТЕКСТ")
        return
    
    broadcast_text = parts[1]
    
    sent = 0
    failed = 0
    
    for user_id in user_payments.keys():
        try:
            bot.send_message(int(user_id), f"📢 РАССЫЛКА:\n\n{broadcast_text}")
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    
    bot.reply_to(message, f"✅ Отправлено: {sent}\n❌ Ошибок: {failed}")

@bot.message_handler(commands=['checkexpiring'])
def check_expiring(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    now = time.time()
    expiring = []
    
    for user_id, data in user_payments.items():
        if data.get('paid', False) and data.get('expires_at'):
            days_left = (data['expires_at'] - now) / 86400
            if 0 < days_left <= 3:
                expiring.append(f"👤 {user_id} - {days_left:.1f} дней")
    
    if expiring:
        bot.reply_to(message, "⚠️ ИСТЕКАЮТ:\n" + "\n".join(expiring))
    else:
        bot.reply_to(message, "✅ Нет истекающих")

@bot.message_handler(commands=['adminhelp'])
def admin_help(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    text = """🔐 КОМАНДЫ АДМИНА

📌 Доступ:
/grant USER_ID - выдать доступ к боту
/block USER_ID - отозвать доступ
/unblock USER_ID - восстановить доступ

📌 Промокоды:
/createpromo - создать
/listpromos - список
/deletepromo - удалить

📌 Пользователи:
/users - список
/userinfo - инфо
/give - выдать подписку
/end - завершить подписку
/extend - продлить подписку

📌 Платежи:
/pending - ожидают
/approve - подтвердить
/reject - отклонить

📌 Другое:
/stats - статистика
/broadcast - рассылка
/checkexpiring - истекающие
/getid - свой ID"""
    
    bot.reply_to(message, text)

@bot.message_handler(commands=['promo'])
def activate_promo(message):
    if not has_access(message.chat.id):
        send_main_menu(message.chat.id)
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❌ /promo КОД")
        return
    
    promo_code = parts[1].upper()
    user_id = str(message.chat.id)
    
    if promo_code not in promocodes:
        bot.reply_to(message, "❌ Неверный код")
        return
    
    promo = promocodes[promo_code]
    
    if promo['used_count'] >= promo['max_uses']:
        bot.reply_to(message, "❌ Промокод использован")
        return
    
    if user_id in promo['used_by']:
        bot.reply_to(message, "❌ Вы уже использовали")
        return
    
    if promo['type'] == 'discount':
        promo['used_count'] += 1
        promo['used_by'].append(user_id)
        save_promos()
        
        if user_id not in user_payments:
            user_payments[user_id] = {}
        user_payments[user_id][f'discount_{promo["tariff"]}'] = promo['value']
        save_data()
        
        original_price = 499 if promo['tariff'] == 'forever' else 99
        final_price = original_price - promo['value']
        bot.reply_to(message, f"✅ Скидка {promo['value']}₽ на {promo['tariff']}\n💰 Цена: {final_price}₽")
    else:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['getid'])
def get_id(message):
    bot.reply_to(message, f"Ваш ID: {message.chat.id}")

# ============ ПРОВЕРКА ПОДПИСКИ НА КАНАЛ ============
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Ошибка проверки подписки на канал: {e}")
        return False

def send_subscription_required(chat_id):
    markup = types.InlineKeyboardMarkup()
    btn_channel = types.InlineKeyboardButton('📢 ПОДПИСАТЬСЯ НА КАНАЛ', url='https://t.me/SOM_VPN69')
    btn_check = types.InlineKeyboardButton('✅ ПРОВЕРИТЬ ПОДПИСКУ', callback_data='check_sub')
    markup.add(btn_channel)
    markup.add(btn_check)
    
    bot.send_message(
        chat_id,
        f"🔒 ДЛЯ ИСПОЛЬЗОВАНИЯ БОТА НЕОБХОДИМА ПОДПИСКА НА КАНАЛ!\n\n"
        f"👉 Канал: https://t.me/SOM_VPN69\n\n"
        f"📌 Инструкция:\n"
        f"1️⃣ Нажмите на кнопку ниже\n"
        f"2️⃣ Подпишитесь на канал\n"
        f"3️⃣ Вернитесь и нажмите «ПРОВЕРИТЬ ПОДПИСКУ»\n\n"
        f"⭐ После подписки вам откроется доступ к боту!",
        reply_markup=markup
    )

# ============ ГЛАВНОЕ МЕНЮ ============
def send_main_menu(chat_id):
    if not has_access(chat_id):
        # Создаём кнопки со ссылками (здесь ссылки точно правильные)
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_bot1 = types.InlineKeyboardButton('🤖 ПЕРЕЙТИ В ipcorp_bot', url=BOT1_LINK)
        btn_bot2 = types.InlineKeyboardButton('🤖 ПЕРЕЙТИ В Excellentbot_bot', url=BOT2_LINK)
        btn_get_access = types.InlineKeyboardButton('🔓 ПОЛУЧИТЬ ДОСТУП', callback_data='request_access')
        markup.add(btn_bot1, btn_bot2, btn_get_access)
        
        bot.send_message(
            chat_id,
            f"🔒 **У ВАС НЕТ ДОСТУПА К БОТУ!**\n\n"
            f"📌 **Для получения доступа:**\n"
            f"1️⃣ Нажмите на кнопки ниже\n"
            f"2️⃣ В каждом боте нажмите «Запустить»\n"
            f"3️⃣ Нажмите «ПОЛУЧИТЬ ДОСТУП»\n\n"
            f"После этого администратор проверит ваш запрос и выдаст доступ.",
            parse_mode='Markdown',
            reply_markup=markup
        )
        return
    
    if not check_subscription(chat_id):
        send_subscription_required(chat_id)
        return
    
    
    
    
    # Если доступ есть — показываем главное меню
    if not check_subscription(chat_id):
        send_subscription_required(chat_id)
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('💰 Купить подписку', callback_data='buy')
    btn2 = types.InlineKeyboardButton('📋 Моя подписка', callback_data='my_sub')
    btn3 = types.InlineKeyboardButton('🆘 Тех.Поддержка', callback_data='support')
    btn4 = types.InlineKeyboardButton('📖 Инструкция', callback_data='manual')
    btn5 = types.InlineKeyboardButton('🎫 Промокод', callback_data='promo')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(chat_id, "🏆 Добро пожаловать в VPN-бот!\nВыберите действие:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    send_main_menu(message.chat.id)

# ============ ОБРАБОТЧИК КНОПКИ "ПОЛУЧИТЬ ДОСТУП" ============
@bot.callback_query_handler(func=lambda call: call.data == 'request_access')
def request_access_callback(call):
    user_id = call.from_user.id
    username = call.from_user.username
    
    # Отправляем уведомление администратору
    send_access_request_to_admin(user_id, username)
    
    # Отвечаем пользователю
    bot.answer_callback_query(call.id, "✅ Запрос отправлен администратору! Ожидайте.")
    bot.send_message(
        user_id,
        "📩 Ваш запрос на доступ отправлен администратору.\n"
        "Ожидайте подтверждения. Обычно это занимает до 10 минут.\n\n"
        "После получения доступа нажмите /start снова."
    )

# ============ ОБРАБОТЧИК ПРОВЕРКИ ПОДПИСКИ НА КАНАЛ ============
@bot.callback_query_handler(func=lambda call: call.data == 'check_sub')
def check_subscription_callback(call):
    user_id = call.from_user.id
    
    if not has_access(user_id):
        bot.answer_callback_query(call.id, "❌ Сначала получите доступ к боту!", show_alert=True)
        send_main_menu(user_id)
        return

    if check_subscription(user_id):
        bot.edit_message_text(
            "✅ Подписка на канал подтверждена!\n\n🏆 Добро пожаловать в VPN-бот!",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        send_main_menu(user_id)
        bot.answer_callback_query(call.id, "✅ Подписка подтверждена!")
    else:
        bot.answer_callback_query(
            call.id, 
            "❌ Вы ещё не подписались на канал!\nПодпишитесь и нажмите кнопку снова.",
            show_alert=True
        )

# ============ ОБРАБОТЧИКИ КНОПОК ПОКУПКИ ============
@bot.callback_query_handler(func=lambda call: call.data == 'buy')
def handle_buy(call):
    if not has_access(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Сначала получите доступ к боту!", show_alert=True)
        send_main_menu(call.message.chat.id)
        return
    
    if not check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Подпишитесь на канал!", show_alert=True)
        send_subscription_required(call.message.chat.id)
        return

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('🔥 Навсегда', callback_data='forever')
    btn2 = types.InlineKeyboardButton('📆 На месяц', callback_data='month')
    markup.add(btn1, btn2)
    
    try:
        bot.edit_message_text("💰 Выберите тип подписки:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'forever')
def handle_forever(call):
    if not has_access(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Сначала получите доступ!", show_alert=True)
        return
    if not check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Подпишитесь на канал!", show_alert=True)
        return
    
    user_id = str(call.from_user.id)
    label = f"forever_{user_id}_{int(time.time())}"
    
    base_price = 499
    discount = user_payments.get(user_id, {}).get('discount_forever', 0)
    final_price = max(0, base_price - discount)
    
    user_payments[user_id] = {
        'label': label,
        'amount': final_price,
        'type': 'forever',
        'paid': False
    }
    save_data()
    
    markup = types.InlineKeyboardMarkup()
    btn_check = types.InlineKeyboardButton('✅ Я оплатил', callback_data=f'check_{label}')
    btn_menu = types.InlineKeyboardButton('🔙 В главное меню', callback_data='main_menu')
    markup.add(btn_check, btn_menu)
    
    text = f"""🔥 Подписка «Навсегда»

💎 Стоимость: {final_price} ₽

💳 Реквизиты: {WALLET_NUMBER}

📌 В комментарии напишите ID: {user_id}

❗️ После оплаты нажмите «Я оплатил»"""
    
    try:
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'month')
def handle_month(call):
    if not has_access(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Сначала получите доступ!", show_alert=True)
        return
    if not check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Подпишитесь на канал!", show_alert=True)
        return
    
    user_id = str(call.from_user.id)
    label = f"month_{user_id}_{int(time.time())}"
    
    base_price = 99
    discount = user_payments.get(user_id, {}).get('discount_month', 0)
    final_price = max(0, base_price - discount)
    
    user_payments[user_id] = {
        'label': label,
        'amount': final_price,
        'type': 'month',
        'paid': False
    }
    save_data()
    
    markup = types.InlineKeyboardMarkup()
    btn_check = types.InlineKeyboardButton('✅ Я оплатил', callback_data=f'check_{label}')
    btn_menu = types.InlineKeyboardButton('🔙 В главное меню', callback_data='main_menu')
    markup.add(btn_check, btn_menu)
    
    text = f"""📆 Подписка «На месяц»

💎 Стоимость: {final_price} ₽

💳 Реквизиты: {WALLET_NUMBER}

📌 В комментарии напишите ID: {user_id}

❗️ После оплаты нажмите «Я оплатил»"""
    
    try:
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data.startswith('check_'))
def handle_check(call):
    if not has_access(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Сначала получите доступ!", show_alert=True)
        return
    if not check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Подпишитесь на канал!", show_alert=True)
        return
    
    label = call.data.replace('check_', '')
    user_id = call.from_user.id
    
    if str(user_id) not in user_payments:
        bot.answer_callback_query(call.id, "❌ Ошибка. Попробуйте выбрать подписку заново.")
        return
    
    if user_payments[str(user_id)].get('paid', False):
        bot.answer_callback_query(call.id, "✅ Оплата уже подтверждена!")
        return
    
    payment_data = user_payments[str(user_id)]
    bot.send_message(ADMIN_ID, f"🔔 ПЛАТЁЖ!\n👤 {user_id}\n💰 {payment_data['amount']}₽\n✅ /approve {user_id} 30\n❌ /reject {user_id}")
    bot.answer_callback_query(call.id, "✅ Заявка отправлена администратору!")
    bot.send_message(user_id, "📩 Заявка отправлена администратору. Ожидайте подтверждения.")

@bot.callback_query_handler(func=lambda call: call.data == 'promo')
def handle_promo_button(call):
    if not has_access(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Сначала получите доступ!", show_alert=True)
        send_main_menu(call.message.chat.id)
        return
    if not check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Подпишитесь на канал!", show_alert=True)
        send_subscription_required(call.message.chat.id)
        return
    
    bot.send_message(call.message.chat.id, "🎫 Введите промокод: /promo КОД")
    try:
        bot.answer_callback_query(call.callback_query_id)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def handle_main_menu(call):
    send_main_menu(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data in ['my_sub', 'support', 'manual'])
def handle_other(call):
    if not has_access(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Сначала получите доступ!", show_alert=True)
        send_main_menu(call.message.chat.id)
        return
    if not check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Подпишитесь на канал!", show_alert=True)
        send_subscription_required(call.message.chat.id)
        return
    
    if call.data == 'my_sub':
        user_id = str(call.from_user.id)
        if user_id in user_payments and user_payments[user_id].get('paid', False):
            text = f"✅ Активна: {user_payments[user_id]['type']}"
            if user_payments[user_id].get('expires_at'):
                expires_str = datetime.fromtimestamp(user_payments[user_id]['expires_at']).strftime('%d.%m.%Y %H:%M')
                text += f"\n📅 До: {expires_str}"
        else:
            text = "❌ Нет активной подписки"
    elif call.data == 'support':
        text = "🆘 Поддержка: @SOM_VPN69"
    else:
        text = "📖 Happ → + → Импорт"
    
    bot.send_message(call.message.chat.id, text)

# ============ ЗАПУСК ============
def run_bot():
    while True:
        try:
            print("✅ VPN-бот с ручной выдачей доступа запущен!")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("🔄 Перезапуск через 5 секунд...")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()