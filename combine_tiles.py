from PIL import Image
import os

# Папка, где лежат картинки
key_word = 'sviter'
input_dir = "/home/user/Files/12/texture/" + key_word
input_file = '/home/user/Files/12u/whitewood2.png'
# Итоговый файл

output_file = f"/home/user/Files/12/texture/{key_word}.png"

# Загружаем 9 картинок
files = sorted(os.listdir(input_dir))[:9]
# files = [input_file] * 9
images = [Image.open(os.path.join(input_dir, f)) for f in files]

# Проверим размер
w, h = images[0].size

# Создаём пустой квадрат 3х3
result = Image.new("RGB", (w * 3, h * 3))

# Вставляем изображения в сетку
for idx, img in enumerate(images):
    x = (idx % 3) * w
    y = (idx // 3) * h
    result.paste(img, (x, y))

# Сохраняем
result.save(output_file)
print(f"Собрано {output_file}")
