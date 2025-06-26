#!/bin/bash

set -e  # Прекратить выполнение при ошибке

cd "$(dirname "$0")"

echo "Запуск бота...\n"

if ! python3 "code/start_bot.py"; then
    echo "Ошибка при выполнении start_bot.py"
    exit 1
fi