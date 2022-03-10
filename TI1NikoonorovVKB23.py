from tkinter import *


# Алгоритм проверки на простое число за n\2
def prime(k):
    if k == 2 or k == 3:
        return True
    if k % 2 == 0 or k < 2:
        return False
    for i in range(3, int(k ** 0.5) + 1, 2):
        if k % i == 0:
            return False
    return True


# Рекурсивный алгоритм расширенного алгоритма евклида
# возвращяет (g, x, y) такие что: a*x + b*y = g = gcd(a, b)
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        b_div_a, b_mod_a = divmod(b, a)
        g, y, x = egcd(b_mod_a, a)
        return g, x - b_div_a * y, y


# Нахождение мультипликативного обратного в поле
# возвращает x такой что (x * a) % m == 1
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('нахождение мультипликативного обратного в поле  ' + m + 'не существует')
    else:
        return x % m


# Обратная польская запись (постфиксная запись)
def rpn(s):
    lex = parse(s)
    s2 = []
    r = []
    oper = ["+", "-", "*", "/", "(", ")"]
    for a in lex:
        if a == "(":
            s2 = [a] + s2
        elif a in oper:
            if s2 == []:
                s2 = [a]
            elif a == ")":
                while True:
                    q = s2[0]
                    s2 = s2[1:]
                    if q == "(":
                        break
                    r += [q]
            elif prior(s2[0]) < prior(a):
                s2 = [a] + s2
            else:
                while True:
                    if s2 == []:
                        break
                    q = s2[0]
                    r += [q]
                    s2 = s2[1:]
                    if prior(q) == prior(a):
                        break
                s2 = [a] + s2
        else:
            r += [a]
    while s2 != []:
        q = s2[0]
        r += [q]
        s2 = s2[1:]
    return r


# Расстановка приоритетов
def prior(o):
    if o == "+" or o == "-":
        return 1
    elif o == "*" or o == "/":
        return 2
    elif o == "(":
        return 0


# Возвращает масив из чисел и знаков (последовательность не меняется)
def parse(s):
    op = ["+", "-", "*", "/", "(", ")"]
    ins = []
    tmp = ""
    for a in s:
        if a != " ":
            if a == "^":
                raise Exception('введение степени возможно только в формате n*n*...*n')
            elif a == "," or a == ".":
                raise Exception('ожидается ввод целых чисел')
            else:
                if a in op:
                    if tmp != "":
                        ins += [tmp]
                    ins += [a]
                    tmp = ""
                else:
                    tmp += a
    if tmp != "":
        ins += [tmp]
    return ins


# Алгоритм расчёта
def Counting(input, size):
    flag = True
    output = ""
    while len(input) > 1:
        i: int = 0
        for a in input:
            if a == "+":
                output = (int(input[i - 2]) % size + int(input[i - 1]) % size) % size
                input[i - 2] = str(output)
                del input[i - 1]
                del input[i - 1]
                print(output, input, '+')
                break
            elif a == "-":
                output = (int(input[i - 2]) % size - int(input[i - 1]) % size) % size
                input[i - 2] = str(output)
                del input[i - 1]
                del input[i - 1]
                print(output, input, '-')
                break
            elif a == "*":
                print(input[i - 2])
                print(input[i - 1])
                output = (int(input[i - 2]) % size * int(input[i - 1]) % size) % size
                input[i - 2] = str(output)
                del input[i - 1]
                del input[i - 1]
                print(output, input, '*')
                break
            elif a == "/":
                print(input[i - 2])
                print(input[i - 1])
                print((int(input[i - 1]) % size))
                # Проверка деления на ноль
                if (int(input[i - 1]) % size) != 0:
                    output = (int(input[i - 2]) % size * modinv((int(input[i - 1]) % size), size)) % size
                    input[i - 2] = str(output)
                    del input[i - 1]
                    del input[i - 1]
                    print(output, input, '/')
                    break
                else:
                    output = 'обнаруженно деление на ноль'
                    flag = False
                    break
            elif flag == False:
                break
            i += 1
        if flag == False:
            break
    return output


# Обработчик нажатия на кнопку
def clicked():
    func = inputfunc.get()
    field = inputfield.get()

    try:
        if prime(int(field)) == True:
            func = rpn(func)
            lbloutput.configure(text=Counting(func, int(field)))
            if Counting(func, int(field)) == 'обнаруженно деление на ноль':
                print('обнаруженно деление на ноль')
            else:
                print(Counting(func, field))
        else:
            lbloutput.configure(text="Значение поля не является простым числом")
    except Exception:
        lbloutput.configure(text="некорректный формат ввода")
    if Counting(func, int(field)) == 'обнаруженно деление на ноль':
        print(Counting(func, int(field)))
    print(Counting(func, int(field)), "asd")



window = Tk()
window.title("LB1 Калькулятор выражений в полях")
window.geometry('400x160')

inputfunc = StringVar()
inputfield = StringVar()

lbl1 = Label(window, text="Введите выражение:")
lbl1.grid(column=0, row=0)
lbl2 = Label(window, text="Поле:")
lbl2.grid(column=2, row=0)
lbloutput = Label(window, text="Результат:")
lbloutput.grid(column=0, row=3)
lbloutput = Label(window, text="")
lbloutput.grid(column=0, row=4)

txtin = Entry(window, width=30, textvariable=inputfunc)
txtin.grid(column=0, row=2)
txtin.insert(0, "2+44*(56-12)/15-66")
txtfield = Entry(window, width=8, textvariable=inputfield)
txtfield.insert(0, "7")
txtfield.grid(column=2, row=2)

btnrez = Button(window, text="Вычислить", command=clicked)
btnrez.grid(column=3, row=2)

window.mainloop()

