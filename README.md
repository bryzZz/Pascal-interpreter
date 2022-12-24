# Pascal-interpreter

Нужно запустить сервер
```
python3 ./server.py
```

Затем запустить клиент и выбрать все настройки
```
python3 ./client.py
```

### Пример

Код test3.txt
``` Pascal
BEGIN
  y := 2;
  BEGIN
    a := 3;
    a := a;
    b := 10 + a + 10 * y / 4;
    c := a - b;
  END;
  x := 11;
END.
```

Запуск скрипта
```
python3 ./client.py

Path to your code: /home/nikita/isu/Pascal-interpreter/data/test3.txt
Tree or Variables? (0 or 1): 1
```

Результат
```
{'y': 2.0, 'x': 11.0, '1': {'a': 3.0, 'b': 18.0, 'c': -15.0}}
```
