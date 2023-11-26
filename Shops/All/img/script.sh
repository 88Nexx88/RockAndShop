# Переходите в директорию с вашими изображениями

# Конвертация всех jpg в png
for file in *.jpg; do
  convert "$file" "$(basename "$file" .jpg).png"
done
python3 main.py