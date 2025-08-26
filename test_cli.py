from InquirerPy import inquirer

choice = inquirer.select(
    message="Выберите базу данных:",
    choices=["PostgreSQL", "ClickHouse", "Выход"],
).execute()

print("Вы выбрали:", choice)
