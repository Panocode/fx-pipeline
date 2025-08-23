import schedule
import time
import subprocess
import logging
from datetime import datetime

# Настраиваем логгер
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def run_etl():
    logging.info("🚀 Запуск ETL задачи...")
    try:
        # Запускаем твой etl.py
        result = subprocess.run(
            ["python", "etl.py"], capture_output=True, text=True
        )

        if result.returncode == 0:
            logging.info("✅ ETL завершен успешно")
            logging.debug(result.stdout)
        else:
            logging.error("❌ Ошибка ETL")
            logging.error(result.stderr)
    except Exception as e:
        logging.exception(f"⚠️ Исключение при запуске ETL: {e}")

# Планируем запуск ETL каждые 5 минут
schedule.every(5).minutes.do(run_etl)

logging.info("📅 Планировщик запущен. Жду расписание...")

while True:
    schedule.run_pending()
    logging.info(f"💓 Heartbeat — контейнер жив ({datetime.now().strftime('%H:%M:%S')})")
    time.sleep(60)