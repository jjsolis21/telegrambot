import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Enviar una imagen al iniciar
    photo_path = 'images/bingo1.png'  # Asegúrate de que esta ruta sea correcta
    try:
        with open(photo_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption="¡Bienvenido a 𝗦𝘂́𝗽𝗲𝗿 𝗕𝗶𝗻𝗴𝗼 2️⃣3️⃣! 🎉")
    except FileNotFoundError:
        await update.message.reply_text("Lo siento, no se pudo encontrar la imagen de bienvenida.")
    
    await mostrar_menu(update)

async def mostrar_menu(update: Update):
    keyboard = [
        [InlineKeyboardButton("📜 𝗥𝗘𝗚𝗟𝗔𝗦", callback_data='reglas')],
        [InlineKeyboardButton("🏆 𝗣𝗥𝗘𝗠𝗜𝗢𝗦", callback_data='premios')],
        [InlineKeyboardButton("💳 𝗖𝗢𝗠𝗣𝗥𝗔𝗥 𝗖𝗔𝗥𝗧𝗢𝗡𝗘𝗦", callback_data='comprar_cartones')],
        [InlineKeyboardButton("🔢 𝗖𝗢𝗠𝗕𝗜𝗡𝗔𝗖𝗜𝗢𝗡 𝗗𝗘 𝗚𝗔𝗡𝗔𝗥", callback_data='combinacion_ganar')],
        [InlineKeyboardButton("📲  𝗣𝗔𝗚𝗢 𝗠𝗢́𝗩𝗜𝗟", callback_data='pago_movil')],
        [InlineKeyboardButton("📆 𝗗𝗜𝗔𝗦 𝗗𝗘 𝗝𝗨𝗘𝗚𝗢", callback_data='dia_juego')],
        [InlineKeyboardButton("👥 𝗨𝗡𝗜𝗥𝗠𝗘 𝗔𝗟 𝗚𝗥𝗨𝗣𝗢",  url='https://t.me/superbingo23')],
        [InlineKeyboardButton("💬 Asistente en vivo", url='https://t.me/superbingo_23')]  # Nuevo botón
        
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Selecciona una opción:", reply_markup=reply_markup)


async def valor_carton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Enviar imagen y botón "Comprar cartón"
    photo_path = 'images/valor_carton.png'  # Asegúrate de que esta ruta sea correcta
    try:
        await update.callback_query.answer()  # Acknowledge the callback
        await update.callback_query.message.reply_photo(photo=open(photo_path, 'rb'))
        
        keyboard = [[InlineKeyboardButton("🛒 Comprar Cartón", callback_data='comprar_carton')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text("¿Deseas comprar un cartón?", reply_markup=reply_markup)
    except FileNotFoundError:
        await update.callback_query.message.reply_text("Lo siento, no se pudo encontrar la imagen del valor del cartón.")

async def comprar_carton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Enviar imagen con 10 botones inline para seleccionar el número de cartones
    photo_path = 'images/comprar_carton.png'  # Asegúrate de que esta ruta sea correcta
    try:
        await update.callback_query.answer()  # Acknowledge the callback
        await update.callback_query.message.reply_photo(photo=open(photo_path, 'rb'))
        
        # Crear un teclado vertical con 10 botones
        keyboard = [[InlineKeyboardButton(f"{i} Carton{'es' if i > 1 else ''}", callback_data=f'carton_{i}')] for i in range(1, 11)]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text("\n\n"
        "𝙎𝙚𝙡𝙚𝙘𝙘𝙞𝙤𝙣𝙖 𝙘𝙪𝙖́𝙣𝙩𝙤𝙨 𝙘𝙖𝙧𝙩𝙤𝙣𝙚𝙨 𝙙𝙚𝙨𝙚𝙖𝙨 𝙘𝙤𝙢𝙥𝙧𝙖𝙧:👇", reply_markup=reply_markup)
    except FileNotFoundError:
        await update.callback_query.message.reply_text("Lo siento, no se pudo encontrar la imagen para comprar cartones.")

async def seleccionar_carton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Determinar cuántos cartones se han seleccionado y enviar el total a pagar
    await update.callback_query.answer()  # Acknowledge the callback
    carton_count = int(update.callback_query.data.split('_')[1])  # Obtener el número de cartones
    total = carton_count * 20  # Calcular el total
    
    # Enviar la imagen y el mensaje del total a pagar
    photo_path = 'images/pago_movil.png'  # Asegúrate de que esta ruta sea correcta
    try:
        # Crear el botón inline para enviar pago
        send_payment_button = InlineKeyboardButton("📎 Enviar pago 📸", url='https://t.me/superbingo_23')
        keyboard = [[send_payment_button]]  # Crear un teclado con el botón

        # Determinar el emoji a mostrar
        if carton_count == 1:
            emoji = "1️⃣"  # Emoji para 1 cartón
        else:
            emoji = f"{carton_count}️⃣"  # Emoji para más de 1 cartón

        # Construir el mensaje con los saltos de línea
        message_text = (
            f"🗣 Usted desea comprar:{emoji} Carton{'es' if carton_count > 1 else ''}.\n\n"
            f"𝗧𝗼𝘁𝗮𝗹 𝗮 𝗽𝗮𝗴𝗮𝗿: {total} Bs.\n\n"
            "𝗗𝗮𝘁𝗼𝘀 𝗱𝗲 𝗣𝗮𝗴𝗼𝗺𝗼́𝘃𝗶𝗹𝗕𝗗𝗩:\n"
            "Cédula: V20556084\n"
            "Teléfono: 04249062486\n"
            "Banco: 0102 - Banco de Venezuela\n\n"
            "Una vez realizado el pago, por favor enviar el capture 👇"
        )

        await update.callback_query.message.reply_photo(photo=open(photo_path, 'rb'), caption=message_text, reply_markup=InlineKeyboardMarkup(keyboard))
    except FileNotFoundError:
        await update.callback_query.message.reply_text("Lo siento, no se pudo encontrar la imagen de pago móvil.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Crear el teclado de nuevo para mantenerlo visible
    keyboard = [
        [InlineKeyboardButton("📜 𝗥𝗘𝗚𝗟𝗔𝗦", callback_data='reglas')],
        [InlineKeyboardButton("🏆 𝗣𝗥𝗘𝗠𝗜𝗢𝗦", callback_data='premios')],
        [InlineKeyboardButton("💳 𝗖𝗢𝗠𝗣𝗥𝗔𝗥 𝗖𝗔𝗥𝗧𝗢𝗡𝗘𝗦", callback_data='comprar_cartones')],
        [InlineKeyboardButton("🔢 𝗖𝗢𝗠𝗕𝗜𝗡𝗔𝗖𝗜𝗢𝗡 𝗗𝗘 𝗚𝗔𝗡𝗔𝗥", callback_data='combinacion_ganar')],
        [InlineKeyboardButton("📲 𝗣𝗔𝗚𝗢 𝗠𝗢́𝗩𝗜𝗟", callback_data='pago_movil')],
        [InlineKeyboardButton("📆 𝗗𝗜𝗔𝗦 𝗗𝗘 𝗝𝗨𝗘𝗚𝗢", callback_data='dia_juego')],
        [InlineKeyboardButton("👥 𝗨𝗡𝗜𝗥𝗠𝗘 𝗔𝗟 𝗚𝗥𝗨𝗣𝗢",  url='https://t.me/superbingo23')],
        [InlineKeyboardButton("💬 Asistente en vivo", url='https://t.me/superbingo_23')]  # Nuevo botón
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)


# Manejo del callback para el botón "REGLAS"
    if query.data == 'reglas':
        photo_path = 'images/REGLAS.png'  # Asegúrate de que esta ruta sea correcta
        try:
            with open(photo_path, 'rb') as photo:
                await query.message.reply_photo(photo=photo, caption="Estas son las 𝗥𝗘𝗚𝗟𝗔𝗦 del Super Bingo 23👆 \n\n @superbingo23")
            
            # Agregar un botón para volver al menú principal
            
            back_button = [[InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data='volver_menu')]]
            back_markup = InlineKeyboardMarkup(back_button)
            

            await query.message.reply_text(text="¿Deseas conocer más sobre nuestro Bingo? 👇", reply_markup=back_markup)  # Enviar solo el botón
        except FileNotFoundError:
            await query.message.reply_text("Lo siento, no se pudo encontrar la imagen de las reglas.")
        
        await query.edit_message_reply_markup(reply_markup=reply_markup)  # Mantener el menú visible

    #VOLVER AL MENU PRINCIPAL
    elif query.data == 'volver_menu':
        await mostrar_menu(query)  # Llama a la función para mostrar el menú principal

    # PREMIOS
    elif query.data == 'premios':
        photo_path = 'images/premios.png'  # Asegúrate de que esta ruta sea correcta
        try:
            with open(photo_path, 'rb') as photo:
                await query.message.reply_photo(photo=photo, caption="Estos son los premios a repartir de esta semana👆 \n"
                                                "\n"
                "@superbingo23" )
         # Agregar un botón para volver al menú principal
            
            back_button = [[InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data='volver_menu')]]
            back_markup = InlineKeyboardMarkup(back_button)
            

            await query.message.reply_text(text="¿Deseas conocer más sobre nuestro Bingo? 👇", reply_markup=back_markup)  # Enviar solo el botón
        except FileNotFoundError:
            await query.message.reply_text("Lo siento, no se pudo encontrar la imagen de las reglas.")
        
        await query.edit_message_reply_markup(reply_markup=reply_markup)  # Mantener el menú visible


# CARTONES DISPONIBLES

    elif query.data == 'cartones':
        photo_path = 'images/GRUPO_TELEGRAM.png'  # Asegúrate de que esta ruta sea correcta
        try:
            with open(photo_path, 'rb') as photo:
                await query.message.reply_photo(photo=photo, caption="Escanea el 𝗤𝗥 o clic en el usuario⬇️ \n⁣"
                 "👉 @superbingo23 👈" )
         # Agregar un botón para volver al menú principal
            
            back_button = [[InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data='volver_menu')]]
            back_markup = InlineKeyboardMarkup(back_button)
            

            await query.message.reply_text(text="¿Deseas conocer más sobre nuestro Bingo? 👇", reply_markup=back_markup)  # Enviar solo el botón
        except FileNotFoundError:
            await query.message.reply_text("Lo siento, no se pudo encontrar la imagen de las reglas.")
        
        await query.edit_message_reply_markup(reply_markup=reply_markup)  # Mantener el menú visible

# MENU PAGO MÓVIL
    elif query.data == 'pago_movil':
        photo_path = 'images/pago_movil.png'  # Ruta de la imagen
        try:
            with open(photo_path, 'rb') as photo:
                await query.message.reply_photo(photo=photo, caption="Una vez realizado el pago, por favor enviar la captura👆\n⁣"
                 "@superbingo23" )
         # Agregar un botón para volver al menú principal
            
            back_button = [[InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data='volver_menu')]]
            back_markup = InlineKeyboardMarkup(back_button)
            

            await query.message.reply_text(text="¿Deseas conocer más sobre nuestro Bingo? 👇", reply_markup=back_markup)  # Enviar solo el botón
        except FileNotFoundError:
            await query.message.reply_text("Lo siento, no se pudo encontrar la imagen de las reglas.")
        
        await query.edit_message_reply_markup(reply_markup=reply_markup)  # Mantener el menú visible

# MENU COMBINACION DE GANAR

    elif query.data == 'combinacion_ganar':
        photo_path = 'images/COMBINACIONES.png'  # Asegúrate de que esta ruta sea correcta
        try:
            with open(photo_path, 'rb') as photo:
                await query.message.reply_photo(photo=photo, caption="Cada 𝗥𝗢𝗡𝗗𝗔 tiene un combinación de ganar distinta.👆 \n"
                                                "\n"
                "@superbingo23" )
         # Agregar un botón para volver al menú principal
            
            back_button = [[InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data='volver_menu')]]
            back_markup = InlineKeyboardMarkup(back_button)
            

            await query.message.reply_text(text="¿Deseas conocer más sobre nuestro Bingo? 👇", reply_markup=back_markup)  # Enviar solo el botón
        except FileNotFoundError:
            await query.message.reply_text("Lo siento, no se pudo encontrar la imagen de las reglas.")
        
        await query.edit_message_reply_markup(reply_markup=reply_markup)  # Mantener el menú visible

# DIA DE JUEGO

    elif query.data == 'dia_juego':
        photo_path = 'images/DIA_JUEGO.png'  # Asegúrate de que esta ruta sea correcta
        try:
            with open(photo_path, 'rb') as photo:
                await query.message.reply_photo(photo=photo, caption="Por ahora solo los 𝗦𝗔́𝗕𝗔𝗗𝗢𝗦 4️⃣PM⏰ \n"
                                                "\n"
                "@superbingo23" )
         # Agregar un botón para volver al menú principal
            
            back_button = [[InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data='volver_menu')]]
            back_markup = InlineKeyboardMarkup(back_button)
            

            await query.message.reply_text(text="¿Deseas conocer más sobre nuestro Bingo? 👇", reply_markup=back_markup)  # Enviar solo el botón
        except FileNotFoundError:
            await query.message.reply_text("Lo siento, no se pudo encontrar la imagen de las reglas.")
        
        await query.edit_message_reply_markup(reply_markup=reply_markup)  # Mantener el menú visible




def main():
    application = ApplicationBuilder().token("7192465698:AAEEXir3g6M3g71-r0OnFORIEGOZlMrRIsc").build()  # Asegúrate de usar tu token real

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(valor_carton, pattern='valor_carton'))
    application.add_handler(CallbackQueryHandler(comprar_carton, pattern='comprar_carton'))
    application.add_handler(CallbackQueryHandler(seleccionar_carton, pattern='carton_\\d+'))  # Manejar selección de cartones
    application.add_handler(CallbackQueryHandler(button_callback))


    application.run_polling()

if __name__ == "__main__":
    main()
