import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

productos = [
    {"codigo": 1, "producto": "Peras", "precio": 4000, "cantidad": 65},
    {"codigo": 2, "producto": "Limones", "precio": 1500, "cantidad": 25},
    {"codigo": 3, "producto": "Moras", "precio": 2000, "cantidad": 30},
    {"codigo": 4, "producto": "Piñas", "precio": 3000, "cantidad": 15},
    {"codigo": 5, "producto": "Tomates", "precio": 1000, "cantidad": 30},
    {"codigo": 6, "producto": "Fresas", "precio": 3000, "cantidad": 12},
    {"codigo": 7, "producto": "Frunas", "precio": 300, "cantidad": 50},
    {"codigo": 8, "producto": "Galletas", "precio": 500, "cantidad": 400},
    {"codigo": 9, "producto": "Chocolates", "precio": 1200, "cantidad": 500},
    {"codigo": 10, "producto": "Arroz", "precio": 1200, "cantidad": 60}
]

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('¡Hola, soy tu bot! Usa /help para ver los comandos disponibles.')

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Comandos disponibles:\n'
                              '/start - Iniciar el bot\n'
                              '/help - Mostrar esta ayuda\n'
                              '/insertar - Insertar un nuevo producto\n'
                              '/actualizar - Actualizar un producto existente\n'
                              '/borrar - Borrar un producto\n'
                              '/listar - Listar todos los productos\n'
                              '/inventario - Mostrar el inventario total\n'
                              '/alerta - Mostrar el producto que está a punto de agotarse')

async def listar(update: Update, context: CallbackContext) -> None:
    mensaje = "Productos en inventario:\n"
    for producto in productos:
        mensaje += f"{producto['codigo']}: {producto['producto']} - Precio: {producto['precio']} - Cantidad: {producto['cantidad']}\n"
    await update.message.reply_text(mensaje)

async def insertar(update: Update, context: CallbackContext) -> None:
    try:
        codigo = int(context.args[0])
        producto = context.args[1]
        precio = int(context.args[2])
        cantidad = int(context.args[3])
        productos.append({"codigo": codigo, "producto": producto, "precio": precio, "cantidad": cantidad})
        await update.message.reply_text(f"Producto {producto} insertado con éxito.")
    except (IndexError, ValueError):
        await update.message.reply_text("Uso: /insertar <código> <producto> <precio> <cantidad>")

async def actualizar(update: Update, context: CallbackContext) -> None:
    try:
        codigo = int(context.args[0])
        cantidad = int(context.args[1])
        for producto in productos:
            if producto["codigo"] == codigo:
                producto["cantidad"] += cantidad
                await update.message.reply_text(f"Producto {producto['producto']} actualizado con éxito.")
                return
        await update.message.reply_text("Producto no encontrado.")
    except (IndexError, ValueError):
        await update.message.reply_text("Uso: /actualizar <código> <cantidad>")

async def borrar(update: Update, context: CallbackContext) -> None:
    try:
        codigo = int(context.args[0])
        global productos
        productos = [producto for producto in productos if producto["codigo"] != codigo]
        await update.message.reply_text(f"Producto con código {codigo} borrado con éxito.")
    except (IndexError, ValueError):
        await update.message.reply_text("Uso: /borrar <código>")

async def inventario(update: Update, context: CallbackContext) -> None:
    inventario_total = sum(producto["precio"] * producto["cantidad"] for producto in productos)
    await update.message.reply_text(f"El valor total del inventario es: {inventario_total}")

async def alerta(update: Update, context: CallbackContext) -> None:
    productos_bajos = [producto for producto in productos if producto["cantidad"] <= (producto["cantidad"] * 0.1)]
    if productos_bajos:
        mensaje = "Productos que están a punto de agotarse:\n"
        for producto in productos_bajos:
            mensaje += f"{producto['producto']} - Cantidad: {producto['cantidad']}\n"
        await update.message.reply_text(mensaje)
    else:
        await update.message.reply_text("No hay productos que estén a punto de agotarse.")

async def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    if update and update.message:
        await update.message.reply_text('Ocurrió un error. Por favor, intenta de nuevo más tarde.')

def main() -> None:
    application = Application.builder().token("6363416885:AAHoQxlBorfpX-qQDer5j7RvLzi704dhziw").build()

    application.add_handler(CommandHandler("Iniciar", start))
    application.add_handler(CommandHandler("Comandos", help_command))
    application.add_handler(CommandHandler("listar", listar))
    application.add_handler(CommandHandler("insertar", insertar))
    application.add_handler(CommandHandler("actualizar", actualizar))
    application.add_handler(CommandHandler("borrar", borrar))
    application.add_handler(CommandHandler("inventario", inventario))
    application.add_handler(CommandHandler("alerta", alerta))

    application.add_error_handler(error_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
