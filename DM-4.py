from random import random
from math import sqrt

#Таблица игры
field = [[2, -3], [-1, 2]]

#Генератор случайных чисел
def rand(p):
    i = random()
    if i <= p:
        d = 0
    else:
        d = 1
    return d

#Подсчет и вывод данных
def calcul(ans, pA, pB, dev, exp):
    print('Вероятность выбора первой строки А:', pA)
    print('Вероятность выбора первого столбца B:', pB)
    print('Выиграш А:', ans[0], 'Выигрыш В:', ans[1])
    aver = ans[0]/exp
    print('Средний выиграш А за одну игру:', aver)
    expected = 8*pA*pB - 5*pA - 3*pB + 2
    print('Математическое ожидание:', expected)
    print('Среднеквадратичное отклоение:', dev)
    disper = (-2*pA*pB - 3*pB + 5*pA + 4) - expected**2
    print('Дисперсия:', disper)
    print('Теоретическое СКО:', sqrt(disper))



# Симуляция обычной игры
def exp(pA, pB):
    #количество игр
    exp = 100
    if (type(pA) == float or type(pA) == int) and (type(pB) == int or type(pB) == float):
        ans = [0, 0]
        ans_mat = []
        for i in range(exp):
            n = field[rand(pA)][rand(pB)]
            ans_mat.append(n)
            ans = [ans[0]+n, ans[1]-n]
        aver = ans[0]/exp
        dev = 0
        for i in ans_mat:
            dev += ((i - aver))**2
        dev = sqrt(dev/(exp-1))
        calcul(ans, pA, pB, dev, exp)


# Симуляция игры с подкреплением для игрока А
def exp_reinA(pA, pB):
    exp = 100
    if pA == 'reinforcement' and (type(pB) == int or type(pB) == float):
        ans = [0, 0]
        ans_mat = []
        sqr = [10, 10]
        pA = sqr[0]/(sqr[0]+sqr[1])
        for i in range(exp):
            randomise = rand(pA)
            n = field[randomise][rand(pB)]
            if n > 0:
                sqr[randomise] += 2
            pA = sqr[0]/(sqr[0]+sqr[1])
            ans_mat.append(n)
            ans = [ans[0]+n, ans[1]-n]
        aver = ans[0]/exp
        dev = 0
        for i in ans_mat:
            dev += ((i - aver))**2
        dev = sqrt(dev/(exp-1))
        calcul(ans, pA, pB, dev, exp)


# Симуляция с наказанием для игрока А
def exp_punishnA(pA, pB):
    exp = 100
    if pA == 'punishment' and (type(pB) == int or type(pB) == float):
        ans = [0, 0]
        ans_mat = []
        sqr = [100, 100]
        pA = sqr[0] / (sqr[0] + sqr[1])
        for i in range(exp):
            randomise = rand(pA)
            n = field[randomise][rand(pB)]
            if n < 0:
                sqr[randomise] += n
            pA = sqr[0] / (sqr[0] + sqr[1])
            ans_mat.append(n)
            ans = [ans[0] + n, ans[1] - n]
        aver = ans[0] / exp
        dev = 0
        for i in ans_mat:
            dev += ((i - aver)) ** 2
        dev = sqrt(dev / (exp-1))
        calcul(ans, pA, pB, dev,  exp)

# Симуляция с подкреплением для обоих игроков
def exp_reinAB(pA, pB):
    exp = 100
    if pA == 'reinforcement' and pB == 'reinforcement':
        ans = [0, 0]
        ans_mat = []
        sqrA = [10, 10]
        sqrB = [10, 10]
        pA = sqrA[0] / (sqrA[0] + sqrA[1])
        pB = sqrB[0] / (sqrB[0] + sqrB[1])
        for i in range(exp):
            randomiseA = rand(pA)
            randomiseB = rand(pB)
            n = field[randomiseA][randomiseB]
            if n < 0:
                sqrB[randomiseB] -= n
            else:
                sqrA[randomiseA] += n
            pA = sqrA[0] / (sqrA[0] + sqrA[1])
            pB = sqrB[0] / (sqrB[0] + sqrB[1])
            ans_mat.append(n)
            ans = [ans[0] + n, ans[1] - n]
        aver = ans[0] / exp
        dev = 0
        for i in ans_mat:
            dev += ((i - aver)) ** 2
        dev = sqrt(dev / (exp-1))
        calcul(ans, pA, pB, dev, exp)






print('Игроки равновероятно выбирают одну или другую строку/столбец')
exp(0.5, 0.5)
print('Игрок A равновероятно выбирает строку, а игрок B выбирает красный столбец втрое реже, чем синий.')
exp(0.5, 0.25)
print('Игрок А с подкреплением')
exp_reinA('reinforcement', 0.25)
print('Игрок А с наказанием')
exp_punishnA('punishment', 0.25)
print('Оба игрока с подкреплением')
exp_reinAB('reinforcement', 'reinforcement')
