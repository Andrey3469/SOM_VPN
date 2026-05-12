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
WALLET_NUMBER = 'https://tbank.ru/cf/5XblKroB2vj'

# ССЫЛКИ ДЛЯ ПРОВЕРКИ (переход по ним даёт доступ)
BOT1_LINK = "https://t.me/ipcorp_bot?start=r01923772967"
BOT2_LINK = "https://t.me/Excellentbot_bot?start=01923772967"

# VPN-ключи
VPN_KEYS = """https://185.39.19.122:2096/sub/7gnura420xqlt0ua"""

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
        except:
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
        except:
            promocodes = {}
            save_promos()
    else:
        promocodes = {}

def save_promos():
    with open(PROMO_FILE, 'w', encoding='utf-8') as f:
        json.dump(promocodes, f, ensure_ascii=False, indent=2)

load_data()
load_promos()

# ============ ФУНКЦИИ ДОСТУПА ============
def has_access(user_id):
    user_data = user_payments.get(str(user_id), {})
    print(f"🔍 Проверка доступа для {user_id}: {user_data.get('has_access', False)}")  # Отладочная строка
    return user_data.get('has_access', False)

def grant_access(user_id):
    user_id_str = str(user_id)
    if user_id_str not in user_payments:
        user_payments[user_id_str] = {}
    user_payments[user_id_str]['has_access'] = True
    user_payments[user_id_str]['verification_passed'] = True
    save_data()
    print(f"✅ Доступ выдан пользователю {user_id}, данные сохранены: {user_payments[user_id_str]}")

def block_user(user_id):
    user_id_str = str(user_id)
    if user_id_str in user_payments:
        user_payments[user_id_str]['has_access'] = False
        save_data()
        return True
    return False

def unblock_user(user_id):
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

✅ Для выдачи доступа: `/grant {user_id}`"""
    
    try:
        bot.send_message(ADMIN_ID, admin_text, parse_mode='Markdown')
    except Exception as e:
        print(f"Ошибка: {e}")

# ============ КОМАНДЫ АДМИНИСТРАТОРА ============
@bot.message_handler(commands=['grant'])
def grant_access_command(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❌ Использование: /grant USER_ID")
        return
    
    user_id = parts[1]
    grant_access(user_id)
    bot.reply_to(message, f"✅ Доступ выдан пользователю {user_id}")
    
    try:
        bot.send_message(int(user_id), "🎉 Вам выдан доступ к боту! Нажмите /start")
    except:
        pass

@bot.message_handler(commands=['block'])
def block_command(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❌ Использование: /block USER_ID")
        return
    
    user_id = parts[1]
    if block_user(user_id):
        bot.reply_to(message, f"✅ Доступ пользователя {user_id} отозван")
    else:
        bot.reply_to(message, f"❌ Пользователь {user_id} не найден")

@bot.message_handler(commands=['unblock'])
def unblock_command(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❌ Использование: /unblock USER_ID")
        return
    
    user_id = parts[1]
    if unblock_user(user_id):
        bot.reply_to(message, f"✅ Доступ пользователя {user_id} восстановлен")
    else:
        bot.reply_to(message, f"❌ Пользователь {user_id} не найден")

@bot.message_handler(commands=['createpromo', 'mypromo'])
def create_promo(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    try:
        parts = message.text.split()
        
        # Определяем, какая команда была использована
        command = parts[0].lower()
        
        if command == '/mypromo':
            # Формат: /mypromo НАЗВАНИЕ тариф тип значение активации
            if len(parts) < 6:
                bot.reply_to(message, "❌ Использование: /mypromo НАЗВАНИЕ тариф тип значение активации\n\n"
                                     "Примеры:\n"
                                     "/mypromo SUMMER2025 forever discount 100 10\n"
                                     "/mypromo WELCOME month discount 50 5\n"
                                     "/mypromo FREETRIAL forever free 0 1\n\n"
                                     "Тарифы: forever, month\n"
                                     "Типы: discount, free")
                return
            
            promo_code = parts[1].upper()  # Пользовательское название промокода
            tariff = parts[2].lower()
            promo_type = parts[3].lower()
            value = int(parts[4]) if parts[4].isdigit() else 0
            max_uses = int(parts[5]) if parts[5].isdigit() else 1
            
        else:
            # Старый формат: /createpromo тариф тип значение активации
            if len(parts) < 5:
                bot.reply_to(message, "❌ Использование: /createpromo тариф тип значение активации\n\n"
                                     "Пример: /createpromo forever discount 100 10")
                return
            
            tariff = parts[1].lower()
            promo_type = parts[2].lower()
            value = int(parts[3]) if parts[3].isdigit() else 0
            max_uses = int(parts[4]) if parts[4].isdigit() else 1
            # Генерируем случайный код
            promo_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        if tariff not in ['forever', 'month']:
            bot.reply_to(message, "❌ Тариф должен быть: forever или month")
            return
        
        if promo_type not in ['discount', 'free']:
            bot.reply_to(message, "❌ Тип должен быть: discount или free")
            return
        
        if max_uses < 1:
            bot.reply_to(message, "❌ Количество активаций должно быть не менее 1")
            return
        
        # Проверяем, не существует ли уже такой промокод
        if promo_code in promocodes:
            bot.reply_to(message, f"❌ Промокод {promo_code} уже существует! Придумайте другое название.")
            return
        
        promocodes[promo_code] = {
            'tariff': tariff,
            'type': promo_type,
            'value': value,
            'max_uses': max_uses,
            'used_count': 0,
            'used_by': [],
            'created_at': time.time(),
            'created_by': message.from_user.id
        }
        save_promos()
        
        if promo_type == 'discount':
            bot.reply_to(message, f"✅ Промокод создан!\n\n🎫 Код: `{promo_code}`\n📦 Тариф: {tariff}\n💰 Скидка: {value}₽\n🔄 Активаций: {max_uses}\n\nПользователи могут активировать его командой /promo {promo_code}", parse_mode='Markdown')
        else:
            bot.reply_to(message, f"✅ Промокод создан!\n\n🎫 Код: `{promo_code}`\n📦 Тариф: {tariff}\n🎁 Бесплатно\n🔄 Активаций: {max_uses}\n\nПользователи могут активировать его командой /promo {promo_code}", parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['listpromos'])
def list_promos(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    if not promocodes:
        bot.reply_to(message, "📭 Нет созданных промокодов")
        return
    
    text = "🎫 СПИСОК ПРОМОКОДОВ:\n\n"
    for code, data in promocodes.items():
        remaining = data['max_uses'] - data['used_count']
        emoji = "✅" if remaining > 0 else "❌"
        if data['type'] == 'discount':
            text += f"{emoji} `{code}`\n   📦 {data['tariff']} | 💰 -{data['value']}₽ | 🔄 {remaining}/{data['max_uses']}\n\n"
        else:
            text += f"{emoji} `{code}`\n   📦 {data['tariff']} | 🎁 Бесплатно | 🔄 {remaining}/{data['max_uses']}\n\n"
    
    bot.reply_to(message, text, parse_mode='Markdown')

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
    
    text = "👥 ПОЛЬЗОВАТЕЛИ:\n\n"
    for user_id, data in user_payments.items():
        status = "✅ Доступ есть" if data.get('has_access') else "❌ Нет доступа"
        paid = "💳 Оплатил" if data.get('paid') else "⏳ Не оплатил"
        text += f"👤 {user_id}: {status}, {paid}\n"
    bot.reply_to(message, text)

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
    text += f"Доступ: {'✅ Да' if data.get('has_access') else '❌ Нет'}\n"
    text += f"Оплата: {'✅ Оплатил' if data.get('paid') else '❌ Не оплатил'}\n"
    if data.get('expires_at'):
        expires_str = datetime.fromtimestamp(data['expires_at']).strftime('%d.%m.%Y %H:%M')
        text += f"Подписка до: {expires_str}\n"
    if data.get('type'):
        text += f"Тариф: {data['type']}\n"
    bot.reply_to(message, text)

@bot.message_handler(commands=['give'])
def give_subscription(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    parts = message.text.split()
    if len(parts) < 4:
        bot.reply_to(message, "❌ /give USER_ID ТАРИФ ДНЕЙ\nПример: /give 123456789 forever 30")
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
        bot.send_message(int(user_id), f"🎉 Администратор выдал вам подписку!\n📅 До: {expires_str}\n\nНажмите /start")
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
        
        # Получаем цену со скидкой
        amount = user_payments[user_id].get('amount', 0)
        original = user_payments[user_id].get('original_amount', amount)
        discount = user_payments[user_id].get('discount', 0)
        
        user_payments[user_id]['paid'] = True
        user_payments[user_id]['expires_at'] = expires_at
        user_payments[user_id]['approved_at'] = time.time()
        save_data()
        
        expires_str = datetime.fromtimestamp(expires_at).strftime('%d.%m.%Y %H:%M')
        
        markup = types.InlineKeyboardMarkup()
        btn_menu = types.InlineKeyboardButton('🔙 В главное меню', callback_data='main_menu')
        markup.add(btn_menu)
        
        # Формируем сообщение пользователю с информацией о скидке
        price_info = f"{amount} ₽"
        if discount > 0:
            price_info = f"{amount} ₽ (было {original} ₽, скидка {discount} ₽)"
        
        try:
            bot.send_message(
                int(user_id),
                f"✅ Ваш платеж подтверждён!\n\n"
                f"📦 Тариф: {user_payments[user_id]['type']}\n"
                f"💰 Оплачено: {price_info}\n"
                f"📅 Действует до: {expires_str}\n\n"
                f"🔑 ВАШИ VPN-КЛЮЧИ:\n\n{VPN_KEYS}\n\n"
                f"📖 Инструкция: скачайте Happ → + → Импорт из буфера",
                reply_markup=markup
            )
            bot.reply_to(message, f"✅ Ключи отправлены пользователю {user_id}")
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
    
    total = len(user_payments)
    with_access = sum(1 for d in user_payments.values() if d.get('has_access'))
    with_payment = sum(1 for d in user_payments.values() if d.get('paid'))
    
    text = f"📊 СТАТИСТИКА:\n\n"
    text += f"👥 Всего: {total}\n"
    text += f"🔓 Имеют доступ: {with_access}\n"
    text += f"✅ Оплатили: {with_payment}\n"
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
        bot.reply_to(message, "❌ Использование: /promo КОД")
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
    
    # Активируем промокод
    original_price = 499 if promo['tariff'] == 'forever' else 99
    
    if promo['type'] == 'discount':
        discount = promo['value']
        final_price = original_price - discount
        
        # Сохраняем скидку для конкретного тарифа
        if user_id not in user_payments:
            user_payments[user_id] = {}
        user_payments[user_id][f'discount_{promo["tariff"]}'] = discount
        save_data()
        
        promo['used_count'] += 1
        promo['used_by'].append(user_id)
        save_promos()
        
        remaining = promo['max_uses'] - promo['used_count']
        text = f"""✅ Промокод активирован!

📦 Тариф: {promo['tariff']}
💰 Скидка: {discount} ₽
💎 Цена без скидки: {original_price} ₽
🎯 Итоговая цена: {final_price} ₽

📌 Осталось активаций: {remaining}/{promo['max_uses']}

Теперь выберите «Купить подписку» → «{promo['tariff']}» в меню."""
        
    else:  # free
        discount = original_price
        final_price = 0
        
        if user_id not in user_payments:
            user_payments[user_id] = {}
        user_payments[user_id][f'discount_{promo["tariff"]}'] = discount
        save_data()
        
        promo['used_count'] += 1
        promo['used_by'].append(user_id)
        save_promos()
        
        remaining = promo['max_uses'] - promo['used_count']
        text = f"""🎉 Бесплатный промокод активирован!

📦 Тариф: {promo['tariff']} — БЕСПЛАТНО!
💰 Экономия: {original_price} ₽

📌 Осталось активаций: {remaining}/{promo['max_uses']}

✅ Теперь выберите «Купить подписку» → «{promo['tariff']}» в меню. Цена будет 0 ₽"""
    
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['getid'])
def get_id(message):
    bot.reply_to(message, f"Ваш ID: {message.chat.id}")

# ============ ГЛАВНОЕ МЕНЮ ============
def send_main_menu(chat_id):
    user_id = str(chat_id)
    print(f"🔍 send_main_menu для {user_id}, has_access={has_access(user_id)}")
    
    if has_access(user_id):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('💰 Купить подписку', callback_data='buy')
        btn2 = types.InlineKeyboardButton('📋 Моя подписка', callback_data='my_sub')
        btn3 = types.InlineKeyboardButton('🆘 Тех.Поддержка', callback_data='support')
        btn4 = types.InlineKeyboardButton('📖 Инструкция', callback_data='manual')
        btn5 = types.InlineKeyboardButton('🎫 Промокод', callback_data='promo')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(chat_id, "🏆 Добро пожаловать в VPN-бот!\nВыберите действие:", reply_markup=markup)
        return
    
    # Нет доступа
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

@bot.message_handler(commands=['start'])
def start(message):
    send_main_menu(message.chat.id)

# ============ ОБРАБОТЧИК КНОПКИ "ПОЛУЧИТЬ ДОСТУП" ============
@bot.callback_query_handler(func=lambda call: call.data == 'request_access')
def request_access_callback(call):
    user_id = call.from_user.id
    username = call.from_user.username
    
    if has_access(user_id):
        bot.answer_callback_query(call.id, "✅ У вас уже есть доступ!")
        send_main_menu(user_id)
        return
    
    send_access_request_to_admin(user_id, username)
    bot.answer_callback_query(call.id, "✅ Запрос отправлен администратору!")
    bot.send_message(user_id, "📩 Запрос отправлен администратору. Ожидайте подтверждения.")

# ============ ОБРАБОТЧИКИ КНОПОК ПОКУПКИ ============
@bot.callback_query_handler(func=lambda call: call.data == 'buy')
def handle_buy(call):
    if not has_access(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Сначала получите доступ к боту!", show_alert=True)
        send_main_menu(call.message.chat.id)
        return

    user_id = str(call.from_user.id)
    
    # Получаем скидку для каждого тарифа
    discount_forever = user_payments.get(user_id, {}).get('discount_forever', 0)
    discount_month = user_payments.get(user_id, {}).get('discount_month', 0)
    
    price_forever = 499 - discount_forever
    price_month = 99 - discount_month
    
    # Показываем цену со скидкой в кнопках
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(f'🔥 Навсегда ({price_forever} ₽)', callback_data='forever')
    btn2 = types.InlineKeyboardButton(f'📆 На месяц ({price_month} ₽)', callback_data='month')
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
    
    user_id = str(call.from_user.id)
    label = f"forever_{user_id}_{int(time.time())}"
    
    base_price = 499
    discount = user_payments.get(user_id, {}).get('discount_forever', 0)
    final_price = max(0, base_price - discount)
    
    # Сохраняем скидку в отдельное поле
    user_payments[user_id] = {
        'label': label,
        'amount': final_price,
        'original_amount': base_price,
        'discount': discount,
        'type': 'forever',
        'paid': False,
        'has_access': True  # Сохраняем доступ!
    }
    save_data()
    
    markup = types.InlineKeyboardMarkup()
    btn_check = types.InlineKeyboardButton('✅ Я оплатил', callback_data=f'check_{label}')
    btn_menu = types.InlineKeyboardButton('🔙 В главное меню', callback_data='main_menu')
    markup.add(btn_check, btn_menu)
    
    discount_text = f"\n\n💰 Скидка по промокоду: {discount}₽" if discount > 0 else ""
    
    text = f"""🔥 Подписка «Навсегда»

💎 Стоимость: {final_price} ₽{discount_text}

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
    
    user_id = str(call.from_user.id)
    label = f"month_{user_id}_{int(time.time())}"
    
    base_price = 99
    discount = user_payments.get(user_id, {}).get('discount_month', 0)
    final_price = max(0, base_price - discount)
    
    # Сохраняем скидку в отдельное поле
    user_payments[user_id] = {
        'label': label,
        'amount': final_price,
        'original_amount': base_price,
        'discount': discount,
        'type': 'month',
        'paid': False,
        'has_access': True  # Сохраняем доступ!
    }
    save_data()
    
    markup = types.InlineKeyboardMarkup()
    btn_check = types.InlineKeyboardButton('✅ Я оплатил', callback_data=f'check_{label}')
    btn_menu = types.InlineKeyboardButton('🔙 В главное меню', callback_data='main_menu')
    markup.add(btn_check, btn_menu)
    
    discount_text = f"\n\n💰 Скидка по промокоду: {discount}₽" if discount > 0 else ""
    
    text = f"""📆 Подписка «На месяц»

💎 Стоимость: {final_price} ₽{discount_text}

💳 Реквизиты: {WALLET_NUMBER}

📌 В комментарии напишите ID: {user_id}

❗️ После оплаты нажмите «Я оплатил»"""
    
    try:
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data.startswith('check_'))
def handle_check(call):
    label = call.data.replace('check_', '')
    user_id = call.from_user.id
    
    if str(user_id) not in user_payments:
        bot.answer_callback_query(call.id, "❌ Ошибка. Попробуйте снова.")
        return
    
    if user_payments[str(user_id)].get('paid', False):
        bot.answer_callback_query(call.id, "✅ Оплата уже подтверждена!")
        return
    
    payment_data = user_payments[str(user_id)]
    
    # Получаем цену со скидкой
    amount = payment_data.get('amount', payment_data.get('original_amount', 0))
    original = payment_data.get('original_amount', amount)
    discount = payment_data.get('discount', 0)
    
    # Формируем сообщение админу с полной информацией о цене
    price_info = f"{amount}₽"
    if discount > 0:
        price_info = f"{amount}₽ (было {original}₽, скидка {discount}₽)"
    
    bot.send_message(
        ADMIN_ID, 
        f"🔔 ПЛАТЁЖ!\n"
        f"👤 Пользователь: {user_id}\n"
        f"📦 Тариф: {payment_data['type']}\n"
        f"💰 Сумма: {price_info}\n"
        f"✅ /approve {user_id} 30\n"
        f"❌ /reject {user_id}"
    )
    bot.answer_callback_query(call.id, "✅ Заявка отправлена администратору!")
    bot.send_message(user_id, "📩 Заявка отправлена администратору. Ожидайте подтверждения.")

@bot.callback_query_handler(func=lambda call: call.data == 'promo')
def handle_promo_button(call):
    if not has_access(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Сначала получите доступ!", show_alert=True)
        send_main_menu(call.message.chat.id)
        return
    
    bot.send_message(call.message.chat.id, "🎫 Введите промокод: /promo КОД")
    try:
        bot.answer_callback_query(call.callback_query_id)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def handle_main_menu(call):
    user_id = call.from_user.id
    print(f"🔍 Кнопка main_menu нажата. Проверяем доступ для {user_id}...")
    
    if has_access(user_id):
        print("✅ Доступ есть, показываем главное меню")
        send_main_menu(call.message.chat.id)
    else:
        print("❌ Доступа нет, показываем экран запроса доступа")
        # Показываем экран получения доступа
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_bot1 = types.InlineKeyboardButton('🤖 ПЕРЕЙТИ В ipcorp_bot', url=BOT1_LINK)
        btn_bot2 = types.InlineKeyboardButton('🤖 ПЕРЕЙТИ В Excellentbot_bot', url=BOT2_LINK)
        btn_get_access = types.InlineKeyboardButton('🔓 ПОЛУЧИТЬ ДОСТУП', callback_data='request_access')
        markup.add(btn_bot1, btn_bot2, btn_get_access)
        
        bot.edit_message_text(
            "🔒 **У ВАС НЕТ ДОСТУПА К БОТУ!**\n\n"
            "📌 **Для получения доступа:**\n"
            "1️⃣ Нажмите на кнопки ниже\n"
            "2️⃣ В каждом боте нажмите «Запустить»\n"
            "3️⃣ Нажмите «ПОЛУЧИТЬ ДОСТУП»\n\n"
            "После этого администратор проверит ваш запрос и выдаст доступ.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    try:
        bot.answer_callback_query(call.id)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data in ['my_sub', 'support', 'manual'])
def handle_other(call):
    if not has_access(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Сначала получите доступ!", show_alert=True)
        send_main_menu(call.message.chat.id)
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
            print("✅ VPN-бот запущен!")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("🔄 Перезапуск через 5 секунд...")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()
