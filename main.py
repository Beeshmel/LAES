from tkinter import messagebox
import numpy
def butclick():
    T = int(ent1.get())
    p = int(ent2.get())
    Gmass=int(ent3.get())
    if T < 220 or T > 330:
        while T < 220 or T > 330:
            if T < 220:
                messagebox.showerror('Температура введена неверно', 'Слишком низкое значение')
            else:
                messagebox.showerror('Температура введена неверно',"Слишком высокое значение")
            T = 300
    if p < 98000 or p > 105000:
        while p < 98000 or p > 105000:
            if p < 98000:
                messagebox.showerror('Давление введено неверно', 'Слишком низкое значение')
            else:
                messagebox.showerror('Давление введено неверно', "Слишком высокое значение")
            p = 101235
    #Расчет простой установки
    if (330 >= int(ent1.get()) >= 220) and (98000 <= int(ent2.get()) <= 105000):
        import math
        import CoolProp
        from CoolProp.CoolProp import PropsSI
        new_win = Toplevel()
        # print("Удельная теплоемкость равна, кДж/кг*К:", Cp1) Cp1 = PropsSI('C', 'T', T, 'P', p, 'Air')
        H1 = PropsSI('H', 'T', T, 'P', p, 'Air')        # print("Энтальпия равна Дж:", H1)
        S1 = PropsSI('S', 'T', T, 'P', p, 'Air')        # print("Энтропия равна, Дж/к:", S1)
        R = 287 # универсальная газовая постоянная Дж/кг*К
        kiz = 0.8 #изотермический коэффициент для расчета работы компрессора
        ks = 0.7 #коэффициент для расчета детандера
        Tf = PropsSI('T','P|liquid', 10e4,'Q',0,'Air')

        if Cycle.get()==1:
            H2 = PropsSI('H', 'T', T, 'P', 10e6, 'Air')
            Hf = PropsSI('H', 'T', Tf, 'P|liquid', 10e4, 'Air')
            x = (H1 - H2) / (H1 - Hf)  # коэффициент ожижения
            l = ((R * T * math.log(10e6 / p) / kiz))
            lx = l / x  # удельная работа
            ref_cof = (H1 - H2) / l  # холодильный коэффициент
            Sf = PropsSI('S', 'T', Tf, 'P|liquid', 10e4, 'Air')
            ref_cof_id = (H1 - Hf) / (
                    T * (S1 - Sf) - (H1 - Hf))  # Холодильный коэффициент идеального ожижительного цикла
            k_term = ref_cof / ref_cof_id  # Степень термодинамического совершенства
            CapitalCost = 300000000

        if Cycle.get()==2:
            # цикл с двойным дросселированием
            H2 = PropsSI('H', 'T', T, 'P', 10e6, 'Air')
            H3 = PropsSI('H', 'T', T, 'P', 20e6, 'Air')
            Hf = PropsSI('H', 'T', Tf, 'P|liquid', 10e4, 'Air')
            m= 0.8
            x= (m * H1 + (1 - m) * H2 - H3) / (H1 - Hf)
            l= ((R * T * math.log(20e6 / p)) / kiz)
            lx = l / x
            ref_cof = (H1 - H3) / l
            Sf = PropsSI('S', 'T', Tf, 'P|liquid', 10e4, 'Air')
            ref_cof_id = (H1 - Hf) / (T * (S1 - Sf) - (H1 - Hf))
            k_term = ref_cof / ref_cof_id
            CapitalCost = 350000000

        if Cycle.get()==3:
            # цикл высокого давления с 2 детандерами
            H2 = PropsSI('H', 'T', T, 'P', 10e6, 'Air')
            H3 = PropsSI('H', 'T', Tf, 'P|gas', 10e4, 'Air')
            H6 = PropsSI('H', 'T', 90, 'P', 10e6, 'Air')
            H7 = PropsSI('H', 'T', Tf, 'P|liquid', 10e6, 'Air')
            Hf = PropsSI('H', 'T', Tf, 'P|liquid', 10e4, 'Air')
            Hs1 = H2 - H3
            Hs2 = H6 - H7
            m=0.2
            x = (H1 - H2 + m * Hs1 * ks + (1-m) * Hs2 * ks) / (H1 - Hf)
            l = ((R * T * math.log(10e6 / p)) / kiz) - m * Hs1 * ks * kiz - (1-m) * Hs2 * ks * kiz
            lx = l / x
            ref_cof = (H1 - H2 + m * Hs1 * ks + (1-m) * Hs2 * ks) / l
            Sf = PropsSI('S', 'T', Tf, 'P|liquid', 10e4, 'Air')
            ref_cof_id = (H1 - Hf) / (T * (S1 - Sf) - (H1 - Hf))
            k_term = ref_cof / ref_cof_id
            CapitalCost = 500000000

        if Cycle.get()==4:
            # цикл Гейландта
            H2 = PropsSI('H', 'T', T, 'P', 10e6, 'Air')
            H3= PropsSI('H', 'T', Tf, 'P|gas', 10e4, 'Air')
            Hf= PropsSI('H', 'T', Tf, 'P|liquid', 10e4, 'Air')
            Hs= H2 - H3
            x = (H1 - H2 + 0.2 * Hs * ks) / (H1 - Hf)
            l = (R * T * math.log(10e6 / p)) / kiz - 0.2 * Hs * ks * kiz
            lx = l / x
            ref_cof = (H1 - H2 + 0.2 * Hs * ks) / l
            Sf = PropsSI('S', 'T', Tf, 'P|liquid', 10e4, 'Air')
            ref_cof_id = (H1 - Hf) / (T * (S1 - Sf) - (H1 - Hf))
            k_term = ref_cof / ref_cof_id
            CapitalCost = 550000000

        if int(ent_gas.get())>=300:
            CostkWh=1.88
            Costkg=(l*CostkWh)/(x*3.6*10e5*kiz*ks) #цена 1 кг жидкого воздуха (массовый расход сокращается)
            Cp = PropsSI('C', 'T', T, 'P', p, 'Air')
            Ghour=Gmass*3600
            k=1.4
            M=0.029
            T_out = float(ent_gas.get())
            A= (Ghour*R*T_out*math.log(700))/(3600*M)                #l =M m R T ln (V2V1)
            #L_ad_st=Cp*T_out(1-1/(1-1**((k-1)/k)))*0.8
            Cost_G=Costkg*Ghour    #Стоимость жидкого воздуха, выработанного в секунду
            Cost_E=A*6.24
            Economy = (Cost_E - Cost_G)/A
            Profit = A*Economy*8*365
            Economy_effect = Profit/CapitalCost

        # Вывод данных
        new_win.title('Результаты расчета')
        new_win.geometry('600x600+900+200')
        new_win.resizable(False, False)
        # Информация о программе COOLPROP
        lab_new0 = Label(new_win,
                         text='Для расчета характеристик установки использовалась библиотека CoolProp ' + CoolProp.__version__,
                         font=("Arial", 8, 'normal'))
        lab_new0.place(x=100, y=575)

        lab1 = Label(new_win,
                           text='Этап ожижения',
                           font=("Arial", 11, 'bold'))
        lab1.place(x=25, y=20)
        lab2 = Label(new_win,
                           text='Коэффициент ожижения ' + str(float('{:.3f}'.format(x))),
                           font=("Arial", 10, 'normal'))
        lab2.place(x=25, y=50)
        lab3 = Label(new_win,
                           text='Удельная работа ' + str(float('{:.3f}'.format(lx / 1000))) + ' кДж/кг сж.в.',
                           font=("Arial", 10, 'normal'))
        lab3.place(x=25, y=70)
        lab4 = Label(new_win, text='Холодильный коэффициент ' + str(
            float('{:.1f}'.format(ref_cof * 100))) + ' %', font=("Arial", 10, 'normal'))
        lab4.place(x=25, y=90)
        lab5 = Label(new_win, text='Холодильный коэффициент идеального ожижительного цикла ' + str(
            float('{:.1f}'.format(ref_cof_id * 100))) + ' %', font=("Arial", 10, 'normal'))
        lab5.place(x=25, y=110)
        lab6 = Label(new_win, text='Степень термодинамического совершенства ' + str(
            float('{:.3f}'.format(k_term))), font=("Arial", 10, 'normal'))
        lab6.place(x=25, y=130)

        lab11 = Label(new_win, text='Экономический расчет ', font=("Arial", 11, 'bold'))
        lab11.place(x=25, y=170)
        lab12 = Label(new_win, text='Cтоимость килограмма жидкого воздуха в рублях ' + str(
            float('{:.2f}'.format(Costkg))), font=("Arial", 10, 'normal'))
        lab12.place(x=25, y=190)
        lab13 = Label(new_win, text='Экономия в час на 1кВт ' + str(
            float('{:.2f}'.format(Economy))), font=("Arial", 10, 'normal'))
        lab13.place(x=25, y=210)

from tkinter import *

win0 = Tk()
win0.title('LAES Project')
win0.geometry('600x600+200+200')
win0.resizable(False, False)

# Ввод и проверка парметров окружающей среды

Abstract = Text(width=78, height=5, font = ("Arial", 9))
Abstract.insert(INSERT, 'Принцип работы криогенного энергетического хранилища основан на следующих процессах: \n\n1. Ожижение воздуха в нерабочее время;\n3. Хранение жидкого воздуха в теплоизолированных резервуарах;\n3. Выработка электроэнергии за счет приведения в действие турбин подогретым воздухом.')
Abstract.place(x=25, y=25)

lab0 = Label(win0, text='Параметры окружающей среды:', font = ("Arial", 10, 'bold'))
lab0.place(x=25, y=125)

lab1 = Label(win0, text='Введите температуру окружающей среды в К:')
lab1.place(x=25, y=150)

ent1 = Entry(win0, bd=2)
ent1.place(x=450, y=150)
ent1.insert(0, '300')

lab2 = Label(win0, text='Введите давление окружающей среды в Па:')
lab2.place(x=25, y=175)

ent2 = Entry(win0, bd=2)
ent2.place(x=450, y=175)
ent2.insert(0, '101325')

lab3 = Label(win0, text='Массовый расход в кг/с:')
lab3.place(x=25, y=200)

ent3 = Entry(win0, bd=2)
ent3.place(x=450, y=200)
ent3.insert(0, '20')
Gmass = ent3.get()

lab5 = Label(win0, text='Отметьте дополнительные параметры установки:', font = ("Arial", 10, 'bold'))
lab5.place(x=25, y=250)

Cycle = IntVar()
Cycle.set(1)
linde_checkbutton = Radiobutton(text="Цикл с дросселированием", variable=Cycle, value=1)
linde_checkbutton.place(x=25, y=275)

linde2_checkbutton = Radiobutton(text="Цикл с двойным дросселированием", variable=Cycle, value=2)
linde2_checkbutton.place(x=25, y=300)

det_checkbutton = Radiobutton(text="Цикл с двумя детандарами", variable=Cycle, value=3)
det_checkbutton.place(x=25, y=325)

Heylandt_checkbutton = Radiobutton(text="Цикл Гейландта", variable=Cycle, value=4)
Heylandt_checkbutton.place(x=25, y=350)

gas = Label(win0, text='Нагрев газа с помощью выхлопных газов, температура, в К:')
gas.place(x=25, y=400)

ent_gas = Entry(win0, bd=2)
ent_gas.place(x=450, y=400)
ent_gas.insert(0, '300')

recovery = IntVar()
recovery_checkbutton = Checkbutton(text="С рекуперацией тепла внутри цикла ", variable=recovery, offvalue=0, onvalue=1)
recovery_checkbutton.place(x=25, y=425)


but1 = Button(win0, text='  Расчет установки  ', font = ("Arial", 10, 'bold'), background='white', command=butclick)
but1.place(x=250, y=550)

win0.mainloop()
