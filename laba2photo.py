from PIL import Image #открываеет обрабатывает сохраняет
import os #папки файлы пути
from datetime import datetime

while True:
    nomer=input("выберите image1.jpg (ввести 1) \nили image2.png (ввести 2): ")
    if nomer=='1':
        imya="image1.JPG"
        break
    elif nomer=='2':
        imya="image2.png"
        break
    else:
        print("нет, введите 1 или 2")

puti=os.path.join("..","data",'input',imya) #путь к файлу
print(os.path.abspath(puti))

kartinka=None
try:
    kartinka=Image.open(puti)
    kartinka=kartinka.convert("RGB")
    print("Размер фотографии:", kartinka.size)

except FileNotFoundError:
    print("Ошибка: файл не найден")
except PermissionError:
    print(f"Ошибка: Нет прав на чтение файла {imya}. Обратитесь к администратору")
except IOError:
    print("Ошибка ввода-вывода при открытии файла")

if kartinka is None:
    raise SystemExit

#свертка
def svertka(kartinka):
    yadro=[
    [1,1,1,1,1],
    [1,1,1,1,1],
    [1,1,1,1,1],
    [1,1,1,1,1],
    [1,1,1,1,1]
    ]
    delit=25
    rez=kartinka.copy()
    shir,visot=kartinka.size

    for y in range(2,visot-2):
        for x in range(2,shir-2):
            sumKRA=0
            sumZEL=0
            sumSIN=0
            for dy in range(-2,3):#смещение координата
                for dx in range(-2,3):
                    px=x+dx  #координата пикселя
                    py=y+dy
                    kra,zel,sin=kartinka.getpixel((px,py))#цвет пикселя по координатам
                    koef=yadro[dy+2][dx+2]
                    sumKRA+=kra*koef
                    sumZEL+=zel*koef
                    sumSIN+=sin*koef
            sredKRA=sumKRA//delit
            sredZEL=sumZEL//delit
            sredSIN=sumSIN//delit
            rez.putpixel((x, y), (sredKRA, sredZEL, sredSIN))

    return rez

#серый мир
def seriMir(kartinka):
    sumKRA = 0
    sumZEL = 0
    sumSIN = 0
    shir, visot = kartinka.size
    for y in range(visot):
        for x in range(shir):
            kra,zel,sin=kartinka.getpixel((x,y))
            sumKRA+=kra
            sumZEL+=zel
            sumSIN+=sin

    kolvo=shir*visot
    sredKRA=sumKRA/kolvo
    sredZEL=sumZEL/kolvo
    sredSIN=sumSIN/kolvo
    sredObsh = (sredKRA+sredZEL+sredSIN)/3

    koefKRA=sredObsh/sredKRA #для приближ к общему
    koefZEL=sredObsh/sredZEL
    koefSIN=sredObsh/sredSIN

    rez=kartinka.copy()

    for y in range(visot):
        for x in range(shir):
            kra,zel,sin=kartinka.getpixel((x,y))

            novKRA=int(kra*koefKRA)
            novZEL=int(zel*koefZEL)
            novSIN=int(sin*koefSIN)

            novKRA=min(255,max(0,novKRA))#ограничиваем диапазон
            novZEL=min(255,max(0,novZEL))
            novSIN=min(255,max(0,novSIN))

            rez.putpixel((x,y),(novKRA,novZEL,novSIN))

    return rez


while True:
    vibor=input("Выберите обработку:\n1 - свертка(1.10)\n2 - серый мир(0.08)\n3 - обе обработки(1.20)\nВаш выбор: ")
    if vibor=='1':
        break
    elif vibor=='2':
        break
    elif vibor=='3':
        break
    else:
        print("введите 1, 2 или 3")

if vibor=='1':
    rez=svertka(kartinka)
    print("Обработка завершена")

elif vibor=='2':
    rez=seriMir(kartinka)
    print("Обработка завершена")

elif vibor=='3':
    rez=svertka(kartinka)
    rez=seriMir(rez)
    print("Обработка завершена")


if vibor=='1':
    metod="Свертка"
elif vibor=='2':
    metod="Серый мир"
elif vibor=='3':
    metod="Свертка + Серый мир"

dataVremya=datetime.now()
putiLog=os.path.join("..","logs","history.txt")

with open(putiLog,'a',encoding='utf-8') as fail:
    fail.write(f"Дата и время: {dataVremya} | Файл: {imya} | Метод: {metod}\n")
print("Журнал открыт")

putiVihod=os.path.join("..","data","output","result.jpg")

try:
    rez.save(putiVihod)
    print("Изображение сохранено")
except PermissionError:
    print("Ошибка: нет прав на сохранение файла")
except IOError:
    print("Ошибка ввода-вывода при сохранении изображения")

