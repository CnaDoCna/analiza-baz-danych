import os.path
import pandas as pd
import scipy.stats as ss
import matplotlib.pyplot as plt
import numpy as np
dane=pd.read_csv(r"athlete_events.csv")
print(dane.describe())
plt.rcParams['font.size']=12
plt.rcParams['axes.labelsize']=12

## wypelniam NA kolumny Medal zerami; zamieniam nazwy medali na wartosci liczbowe
def kolumnaMedalLiczbowe(dane):
    dane.Medal=dane.Medal.fillna(0)
    dane.Medal=dane.Medal.replace("Gold", 3)
    dane.Medal=dane.Medal.replace("Silver", 2)
    dane.Medal=dane.Medal.replace("Bronze", 1)


## wypelniam NA kolumn Height, Weight, Age średnimi wartości tych kolumn; zapisuje do pliku dane wartości Height, Weight, Age oraz sume wartosci Medal poszczegolnych zawodnikow
## w dalszej pracy pobieram dane z raz stworzonego pliku dla zaoszczędzenia czasu
def plikDaneZawodnikow(dane):
    kolumnaMedalLiczbowe(dane)
    wiekZawodnikow=np.array([])
    wagaZawodnikow=np.array([])
    wzrostZawodnikow=np.array([])
    medaleZawodnikow=np.array([])
    dane.Age=dane.Age.fillna(dane.Age.mean())
    dane.Height=dane.Height.fillna(dane.Height.mean())
    dane.Weight=dane.Weight.fillna(dane.Weight.mean())

    for i in range(1,max(dane.ID)):

        wiek=dane.loc[dane["ID"]==i, "Age"].values.mean()
        wiekZawodnikow=np.append(wiekZawodnikow, wiek)

        wzrost=dane.loc[dane["ID"]==i, "Height"].values.mean()
        wzrostZawodnikow=np.append(wzrostZawodnikow, wzrost)

        waga=dane.loc[dane["ID"]==i, "Weight"].values.mean()
        wagaZawodnikow=np.append(wagaZawodnikow, waga)

        medale=dane.loc[dane["ID"]==i, "Medal"].values.sum()
        medaleZawodnikow=np.append(medaleZawodnikow, medale)

    a=np.asarray([wiekZawodnikow, wzrostZawodnikow, wagaZawodnikow, medaleZawodnikow])
    np.savetxt("wiek_wzrost_waga_medal.csv", a)


## średnia, mediana, odchylenie standardowe używanych zmiennych
def opisZmiennych(dane):
    medale=np.loadtxt("wiek_wzrost_waga_medal.csv")[3]
    print("\nDane dla zmiennej Medal (dla pojedynczych zawodników): ")
    print("N: ", len(medale))
    print("x¯: ", round(np.mean(medale),2))
    print("Me: ", round(np.median(medale),2))
    print("SD: ", round(np.std(medale),2))

    medale2=dane.Year[(pd.notnull(dane.Medal))].value_counts()
    print("\nDane dla zmiennej Medal (dla pojedynczych lat): ")
    print("N: ", medale2.count())
    print("x¯: ", round(medale2.mean(),2))
    print("Me: ", round(medale2.median(),2))
    print("SD: ", round(medale2.std(),2))

    print("\nDane dla zmiennej Wiek (dla pojedynczych zawodników): ")
    print("N: ", dane.Age.count())
    print("x¯: ", round(dane.Age.mean(),2))
    print("Me: ", round(dane.Age.median(),2))
    print("SD: ", round(dane.Age.std(),2))

    print("\nDane dla zmiennej Wzrost (dla pojedynczych zawodników): ")
    print("N: ", dane.Height.count())
    print("x¯: ", round(dane.Height.mean(),2))
    print("Me: ", round(dane.Height.median(),2))
    print("SD: ", round(dane.Height.std(),2))

    print("\nDane dla zmiennej Waga (dla pojedynczych zawodników): ")
    print("N: ", dane.Weight.count())
    print("x¯: ", round(dane.Weight.mean(),2))
    print("Me: ", round(dane.Weight.median(),2))
    print("SD: ", round(dane.Weight.std(),2))

    print("\nCałkowita liczba zawodników: ", len(medale))
    print("\nCałkowita liczba pomiarów: ", len(dane))

## "Czy wzrost zawodnika różnicuje szansę zdobycia medalu?"
## wczytuję z pliku dane dotyczace wzrostu i medali zawodnikow; sprawdzam korelacje
def pytanie1(dane):
    wzrostZawodnikow=np.loadtxt("wiek_wzrost_waga_medal.csv")[1]
    medaleZawodnikow=np.loadtxt("wiek_wzrost_waga_medal.csv")[3]

    plt.hist(wzrostZawodnikow)
    plt.xlabel("wzrost [cm]")
    plt.ylabel("liczba medalistów [-]")
    plt.show()

    print("\n\n1. Czy wzrost zawodnika różnicuje szansę zdobycia medalu?")
    print("\nKorelacja Pearsona wzrostu i wartości zdobytych medali: ", ss.pearsonr(wzrostZawodnikow, medaleZawodnikow))


## "Kto w danym roku zdobył dla swojego kraju większą liczbę medali, kobiety czy mężczyźni?"
## sumuję liczbe nie-zerowych wartości kolumny Medal (medali) dla poszczególnych wartości kolumny Sex (płci) i dla poszczególnych wartości kolumny Year (lat)
## sprawdzam normalość rozkładu medalistek i medalistow dla Year; sprawdzam istotność różnic dla prób niezależnych
def pytanie2(dane):
    medaleKobiet=dane.Year[(dane.Sex=="F") & (pd.notnull(dane.Medal))]
    medaleMezczyzn=dane.Year[(dane.Sex=="M") & (pd.notnull(dane.Medal))]

    ileKobiet= medaleKobiet.value_counts().values
    ileMezczyzn= medaleMezczyzn.value_counts().values
    rokK=medaleKobiet.value_counts().index.values
    rokM=medaleMezczyzn.value_counts().index.values

    plt.bar(rokK, ileKobiet, color="m", label="kobiety", width=0.5)
    plt.bar(rokM+0.5, ileMezczyzn, color="b", label="mężczyźni", width=0.5)
    plt.legend()
    plt.xlabel("rok [-]")
    plt.ylabel("liczba medalistów [-]")
    plt.show()

    print("\n\n2. Kto w danym roku zdobył dla swojego kraju większą liczbę medali, kobiety czy mężczyźni?")
    print("\nTest normalności Shapiro-Wilka:", "\nKobiety:", ss.shapiro(ileKobiet), "\nMężczyźni:", ss.shapiro(ileMezczyzn))
    print("\nTest t: \n", ss.ttest_ind(ileKobiet, ileMezczyzn))
    print("\nLiczba zdobytych medali przez kobiety we wszystkich latach: ", "\nN: ", ileKobiet.sum(), "\nx¯: ", round(ileKobiet.mean(),2), "\nSD: ", round(ileKobiet.std(),2))
    print("Liczba zdobytych medali przez mężczyzn we wszystkich latach: ", "\nN: ", ileMezczyzn.sum(), "\nx¯: ", round(ileMezczyzn.mean(),2), "\nSD: ", round(ileMezczyzn.std(),2))



## "Czy wiek zawodnika zwiększa szansę na zdobycie medalu?"
## wczytuję z pliku dane dotyczace wieku i medali zawodnikow; sprawdzam korelacje
def pytanie3(dane):
    wiekZawodnikow=np.loadtxt("wiek_wzrost_waga_medal.csv")[0]
    medaleZawodnikow=np.loadtxt("wiek_wzrost_waga_medal.csv")[3]

    plt.hist(wiekZawodnikow)

    plt.xlabel("wiek [-]")
    plt.ylabel("liczba medalistów [-]")
    plt.show()

    print("\n\n3. Czy wiek zawodnika zwiększa szansę na zdobycie medalu?")
    print("\nKorelacja Pearsona wieku i wartości zdobytych medali: ", ss.pearsonr(wiekZawodnikow, medaleZawodnikow))


## "Który z zawodników zdobył podczas swojej kariery sportowej najwięcej medali?"
## liczę, która wartość kolumny Name (imiona) wystepuje najczęściej pod warunkiem posiadania nie-zerowej wartości kolumny Medal (medalu)
def pytanie4(dane):
    medalisci=dane.Name[(pd.notnull(dane.Medal))].value_counts()

    print("\n\n4. Który z zawodników zdobył podczas swojej kariery sportowej najwięcej medali?")
    print("\nImię medalisty:                        Liczba medali:\n", medalisci[0:100], "\n")



## "Który kraj posiada najwięcej medalistów wśród kobiet, a który wśród mężczyzn?"
## sumuję liczbe najcześciej występujących wartości kolumny NOC (krajów) pod warunkiem posiadania nie-zerowych wartości kolumny Medal (medalu) dla poszczególnych wartości kolumny Sex (płci)
## sprawdzam normalość rozkładu medalistek i medalistow dla NOC; sprawdzam istotność różnic dla prób niezależnych
def pytanie5(dane):
    krajeKobiet=dane.NOC[(dane.Sex=="F") & (pd.notnull(dane.Medal))]
    krajeMezczyzn=dane.NOC[(dane.Sex=="M") & (pd.notnull(dane.Medal))]

    ileKobiet=krajeKobiet.value_counts()
    ileMezczyzn=krajeMezczyzn.value_counts()
    print("K:\n",ileKobiet[0:3])
    print("M:\n", ileMezczyzn[0:3])
    plt.xticks(rotation=90)

    plt.bar(ileKobiet.index[0:40], ileKobiet[0:40], color="m", label="kobiety", width=0.5, align="edge")
    plt.bar(ileMezczyzn.index[0:40], ileMezczyzn[0:40], color="b", label="mężczyźni", width=0.35)
    plt.legend()
    plt.xlabel("Narodowy Komitet Olimpijski [-]")
    plt.ylabel("liczba medalistów [-]")
    plt.show()

    print("\n\n5. Który kraj posiada najwięcej medalistów wśród kobiet, a który wśród mężczyzn?")
    print("\nTest normalności Shapiro-Wilka:", "\nK:", ss.shapiro(ileKobiet), "\nM:", ss.shapiro(ileMezczyzn))
    print("\nTest t: \n", ss.ttest_ind(ileKobiet, ileMezczyzn))
    print("\nLiczba medalistek dla wszystkich krajów: ", "\nN: ", ileKobiet.sum(), "\nx¯: ", round(ileKobiet.mean(),2), "\nSD: ", round(ileKobiet.std(),2))
    print("Liczba medalistów dla wszystkich krajów: ", "\nN: ", ileMezczyzn.sum(), "\nx¯: ", round(ileMezczyzn.mean(),2), "\nSD: ", round(ileMezczyzn.std(),2))



## "Czy różnica w wagach pomiędzy zawodnikami ma wpływ na ilość zdobytych przez nich medali?"
## wczytuję z pliku dane dotyczace wagi i medali zawodnikow; sprawdzam korelacje
def pytanie6(dane):
    wagaZawodnikow=np.loadtxt("wiek_wzrost_waga_medal.csv")[2]
    medaleZawodnikow=np.loadtxt("wiek_wzrost_waga_medal.csv")[3]

    plt.hist(wagaZawodnikow)
    plt.xlabel("waga [kg]")
    plt.ylabel("liczba medalistów [-]")
    plt.show()

    print("\n\n6. Czy różnica w wagach pomiędzy zawodnikami ma wpływ na ilość zdobytych przez nich medali?")
    print("\nKorelacja  Pearsona wzrostu i wartości zdobytych medali: ", ss.pearsonr(wagaZawodnikow, medaleZawodnikow))


## "Czy wiek oraz waga zawodników są od siebie zależne?"
## wczytuję z pliku dane dotyczace wagi i wieku zawodnikow; sprawdzam korelacje
def pytanie7(dane):
    wiekZawodnikow=np.loadtxt("wiek_wzrost_waga_medal.csv")[0]
    wagaZawodnikow=np.loadtxt("wiek_wzrost_waga_medal.csv")[2]

    print("\n\n7. Czy wiek oraz waga zawodników są od siebie zależne?")
    print("\nKorelacja Pearsona wieku i wagi: ", ss.pearsonr(wiekZawodnikow, wagaZawodnikow))


## sprawdzam, czy we wspólnej lokacji istnieje plik wiek_wzrost_waga_medal.csv; jeżeli nie, tworzę go (zajmuje to pare minut)
if not os.path.isfile("wiek_wzrost_waga_medal.csv"):
    plikDaneZawodnikow(dane)
opisZmiennych(dane)
# pytanie1(dane)
# pytanie2(dane)
# pytanie3(dane)
# pytanie4(dane)
# pytanie5(dane)
# pytanie6(dane)
# pytanie7(dane)
