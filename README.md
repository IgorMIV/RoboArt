# Библиотека для управления роботом - художником

Подключение и инициализация библиотеки:
```python
from roboart import *
roboart = RoboArt()
```

Метод очистки кисти:
```python
roboart.clean_brush()
```

Методы набора краски на кисть:
```python
roboart.take_paint(BrushColors.white)
roboart.take_paint(BrushColors.green)
roboart.take_paint(BrushColors.red)
roboart.take_paint(BrushColors.blue)
roboart.take_paint(BrushColors.black)
roboart.take_paint(BrushColors.yellow)
```

Методы рисования:
```python
roboart.draw_line([(x1, y1), (x2, y2), (x3, y3)]) # Рисование линии
roboart.draw_point((x, y)) # Рисование точки
```

Пример рисования линии зелёного цвета:
```python
roboart.clean_brush()
roboart.take_paint(BrushColors.green) 
roboart.draw_line([(200, 200), (150, 130), (90, 20)])
```

Пример рисования точки красного цвета:
```python
roboart.clean_brush()
roboart.take_paint(BrushColors.red) 
roboart.draw_point((110, 130))
```

Визуализация текущей программы:
```python
roboart.visualize()
```

Отправка программы на робота:
```python
roboart.paint()
```

Возврат расстояния, которое робот проедет в плоскости XY (полное/рисуя):
```python
full, paint = roboart.calculate_distance()
print("Full:", full, "Paint:", paint)
```

Экспорт программы для робота в файл:
```python
program_text = roboart.get_program_text()
file = open("programfile.txt", "w")
file.write(program_text)
file.close()
```