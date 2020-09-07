#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
def game_core_v1(number):
    '''Просто угадываем на random, никак не используя информацию о больше или меньше.
       Функция принимает загаданное число и возвращает число попыток'''
    count = 0
    while True:
        count+=1
        predict = np.random.randint(1,101) # предполагаемое число
        if number == predict: 
            return(count) # выход из цикла, если угадали
        
def score_game(game_core):
    '''Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число'''
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1,101, size=(1000))
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return(score)

def game_core_v3(number):
    trying = 1
    start = 0                               # задаем начальный диапазон поиска числа
    finish = 101                            # задаем конечный диапазон поиска числа
    predict = (start + finish) // 2           # задаем середину диапазона, с которой начнем поиск числа
    while number != predict:     # создаем цикл до тех пор, пока загаданное число не равно предсказанному
        if number > predict:           # если загаданное число больше предсказанного  
            start = predict            # сдвигаем начальный диапазон до среднего
            predict = predict + ((finish-start) //2 )
        elif number < predict:         # если загаданное число меньше предсказанного 
            finish = predict           # сдвигаем конечный диапазон до среднего
            predict = predict - ((finish-start) // 2)
        trying += 1                    # считаем количество попыток
    return(trying)


# In[4]:


# Проверяем
score_game(game_core_v3)


# In[ ]:




