# Базовые алгоритмы растеризации
## Быстрова Вероника, 3 курс 13 группа

## Описание
В приложении реализованы следующие базовые алгоритмы растеризации отрезков и кривых:
- пошаговый алгоритм
- алгоритм ЦДА
- алгоритм Брезенхема
- алгоритм Брезенхема для окружности

## Используемые технологии
- Python

## Используемые библиотеки. Сборка
```
pip install matplotlib
```
Для сборки в exe файл нужно дополнительно установить библиотеку PyInstaller
```
pip install pyinstaller
```
Для компиляции использовать следующую команду
```
pyinstaller --onefile -w main.py
```

## Сопроводительная документация
### UI - приложения
<img width="960" alt="Снимок" src="https://user-images.githubusercontent.com/79499241/235101727-fb845945-5c71-4917-a57a-bc63020f62c7.PNG">

### алгоритм Брезенхема
(1, 6), (9, 4)
dx = 8, dy = 2
sx = 1, sy = -1
e = 6

1. e2 = 6 * 2 = 12 > -2; e = 6 - 2 = 4; (2, 6)
2. e2 = 4 * 2 = 8 > -2; e = 4 - 2 = 2; (3, 6)
3. e2 = 2 * 2 = 4 > -2; e = 2 - 2 = 0; e2 = 4 < 8; e = 0 + 8 = 8; (4, 5)
4. e2 = 8 * 2 = 16 > -2; e = 8 - 2 = 6; (5, 5)
5. e2 = 6 * 2 = 12 > -2; e = 6 - 2 = 4; (6, 5)
6. e2 = 4 * 2 = 8 > -2; e = 4 - 2 = 2; (7, 5)
7. e2 = 2 * 2 = 4 > -2; e = 2 - 2 = 0; e2 = 4 < 8; e = 0 + 8 = 8; (8, 4)
8. e2 = 8 * 2 = 16 > -2; e = 8 - 2 = 6; (9, 4)

### пошаговый алгоритм
x = 1; k = -0.25; b = 6.25

1. x = 1; y = -0.25 * 1 + 6.25 = 6; (1, 6)
2. x = 2; y = - 0.25 * 2 + 6.25 = 5.75 => 6 (2, 6)
3. (3, 6)
4. (4, 5)
5. (5, 5)
6. (6, 5)
7. (7, 5)
8. (8, 4)
9. (9, 4)

### ЦДА
(1, 6), (9, 4)
dx = 8; dy = -2; steps = 8
x_inc = 1;
y_inc = -0.25

1. (1, 6); x = 1 + 1 = 2; y = 6 - 0.25 = 5.75 => 6
2. (2, 6); x = 2 + 1 = 3; y = 5.75 - 0.25 = 5.5 => 6
3. (3, 6); x = 3 + 1 = 4; y = 5.5 - 0.25 = 5.25 => 5
4. (4, 5);
5. (5, 5);
6. (6, 5);
7. (7, 5);
8. (8, 4);
9. (9, 4);

### алгоритм Брезенхема для окружности
x0 = 0, y0 = 0, r = 7
x = 0; y = r = 7; e = 3 - 2r = -11
Пока x < y:
(0, 7)
1. e < 0; e = e + 4x + 6 = -5; x = x + 1 = 1; (1, 7)
2. e < 0; e = e + 4x + 6 = 5; x = x + 1 = 2; (2, 7)
3. e > 0; e = e + 4(x-y) + 10 = -5; x = x + 1 = 3; y = y - 1 = 6; (3, 6)
4. e < 0; e = e + 4x + 6 = 13; x = x + 1 = 4; (4, 6)
5. e > 0; e = e + 4(x-y) + 10 = 15; x = x + 1 = 5; y = y - 1 = 5; (5, 5)

## Время работы
Step by step. Time spent: 0.0  
Bresenham line. Time spent: 0.05164313316345215  
DDA. Time spent: 0.03949570655822754  
Bresenham circle. Time spent: 1.7198050022125244  