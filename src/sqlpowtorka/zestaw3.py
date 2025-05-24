import sqlpowtorka.przygotowanie as prep
import os.path, os
import sqlite3 as sql

if os.path.exists('sklep.db'):
    os.unlink('sklep.db')
try:
    prep.dbinit()
    #Import zestaw1 here if you want changes applied to the
    #db from the tasks over there.
    if os.path.exists('sklep.db'):
        con = sql.connect('sklep.db')
        cur = con.cursor()
    else:
        raise Exception('The file sklep.db does not exist')
except Exception as e:
    print(e)
    raise

# 1. Wyświetl listę zamówień zawierającą imiona i nazwiska klientów posiadających zamówienia, id zamówienia oraz datę zmówienia wraz z kwotą zamówienia
query1 = '''
    SELECT Imie 'Imię', Nazwisko, ID_Zamowienia 'ID zamówienia', Data_Zamowienia 'Data zamówienia', Kwota
    FROM Klienci NATURAL JOIN Zamowienia;
'''
col_names = [desc[0] for desc in con.execute(query1).description]
# print(col_names)
# for t in cur.execute(query1):
#     print(*t)

# 2. Wyświetl wszystkich klientów wraz z ich zamówieniami, nawet jeżeli nie posiadają zamówień. Lista powinna zawierać id klienta, imię oraz nazwisko, id zamówienia, datę zamówienia
query2 = '''
    SELECT ID_Klienta 'ID Klienta', Imie 'Imię', Nazwisko, ID_Zamowienia 'ID zamówienia', Data_Zamowienia 'Data zamówienia'
    FROM Klienci NATURAL FULL OUTER JOIN Zamowienia;
'''
col_names = [desc[0] for desc in con.execute(query2).description]
# print(col_names)
# for t in cur.execute(query2):
#     print(*t)

# 3. Wyświetl klientów (id, imię, nazwisko), którzy złożyli zamówienia powyżej średniej kwoty zamówienia (średnia kwota obliczona na podstawie wszystkich zamówień = 4552.6)
query3 = '''
    SELECT ID_Klienta 'ID klienta', Imie 'Imię', Nazwisko
    FROM Klienci NATURAL JOIN Zamowienia
    WHERE Kwota > 
        (SELECT AVG(Kwota)
        FROM Zamowienia);
'''
col_names = [desc[0] for desc in con.execute(query3).description]
# print(col_names)
# for t in cur.execute(query3):
#     print(*t)

# 4. Wyświetl wszystkie informacje o zamówieniu/zamówieniach, które posiadają największą kwotę zamówienia
# The following query does not work in SQLite - lame
query4 = '''
    SELECT *
    FROM Zamowienia
    WHERE Kwota >= ALL
        (SELECT Kwota
        FROM Zamowienia);
'''
query4 = '''
    SELECT *
    FROM Zamowienia
    WHERE Kwota >=
        (SELECT MAX(Kwota)
        FROM Zamowienia);
'''
col_names = [desc[0] for desc in con.execute(query4).description]
# print(col_names)
# for t in cur.execute(query4):
#     print(*t)

# 5. Wyświetl informacje o zamówieniu zawierające id zamówienia, datę zamówienia, ilość z zamówienia, kwotę z zamówienia, nazwę produktu, cenę produktu, zliczoną ilość pozycji z tabeli Pozycje_Zamowienia, zliczoną wartość zamówienia na podstawie ceny i ilości z tabeli Pozycje_Zamowienia
query51 = '''
    CREATE VIEW zliczone_pozycje AS
        SELECT ID_Zamowienia, COUNT(*) AS ilosc_pozycji
        FROM Pozycje_Zamowienia
        GROUP BY ID_Zamowienia;
'''
query52 = '''
    CREATE VIEW zliczone_wartosci AS
        SELECT ID_Zamowienia, SUM(Ilosc * Cena) AS wartosc
        FROM Pozycje_Zamowienia NATURAL JOIN Produkty
        GROUP BY ID_Zamowienia;
'''
query53 = '''
    SELECT ID_Zamowienia, ID_Produktu, Data_Zamowienia, Ilosc,
        Kwota, Nazwa, Cena, ilosc_pozycji, wartosc
    FROM zliczone_pozycje NATURAL JOIN zliczone_wartosci
        NATURAL JOIN
            (SELECT ID_Zamowienia, ID_Produktu
            FROM Pozycje_Zamowienia) AS R NATURAL JOIN
                Zamowienia NATURAL JOIN Produkty;
'''
queries5 = [query51, query52, query53]
for q in queries5:
    cur.execute(q)
col_names = [desc[0] for desc in con.execute(query53).description]
# print(col_names)
# for t in cur.execute(query53):
#     print(*t)

# 6. Wyświetl sumy ilości i wartości produktów z każdego zamówienia zarówno z tabeli Zamówienia jak i z tabeli Pozycje_Zamowienia. Znajdź błędne zamówienie dla którego te wartości nie są zgodne.
query61 = '''
    SELECT ID_Zamowienia, Ilosc ilosc, Kwota wartosc
    FROM Zamowienia;
'''
col_names = [desc[0] for desc in con.execute(query61).description]
print(col_names)
for t in cur.execute(query61):
    print(*t)
query62 = '''
    SELECT ID_Zamowienia, SUM(Ilosc) as ilosc, SUM(Ilosc * Cena) AS wartosc
    FROM Pozycje_Zamowienia NATURAL JOIN Produkty
    GROUP BY ID_Zamowienia;
'''
col_names = [desc[0] for desc in con.execute(query62).description]
print(col_names)
for t in cur.execute(query62):
    print(*t)
query63 = '''
    CREATE VIEW A AS
        SELECT ID_Zamowienia, Ilosc ilosc, Kwota wartosc
        FROM Zamowienia;
'''
query64 = '''
    CREATE VIEW B AS
        SELECT ID_Zamowienia, SUM(Ilosc) as ilosc, SUM(Ilosc * Cena) AS wartosc
        FROM Pozycje_Zamowienia NATURAL JOIN Produkty
        GROUP BY ID_Zamowienia;
'''
for q in [query63, query64]:
    cur.execute(q)
# The following query does not work in sqlite3 - lame
query65 = '''
    ((SELECT ID_Zamowienia, Ilosc ilosc, Kwota wartosc
    FROM Zamowienia)
    EXCEPT
    (SELECT ID_Zamowienia, SUM(Ilosc) as ilosc, SUM(Ilosc * Cena) AS wartosc
    FROM Pozycje_Zamowienia NATURAL JOIN Produkty
    GROUP BY ID_Zamowienia))
    UNION
    ((SELECT ID_Zamowienia, SUM(Ilosc) as ilosc, SUM(Ilosc * Cena) AS wartosc
    FROM Pozycje_Zamowienia NATURAL JOIN Produkty
    GROUP BY ID_Zamowienia)
    EXCEPT
    (SELECT ID_Zamowienia, Ilosc ilosc, Kwota wartosc
    FROM Zamowienia))
'''
query65 = '''
    SELECT ID_Zamowienia, Ilosc ilosc, Kwota wartosc
    FROM Zamowienia
    EXCEPT
    SELECT ID_Zamowienia, SUM(Ilosc) as ilosc, SUM(Ilosc * Cena) AS wartosc
    FROM Pozycje_Zamowienia NATURAL JOIN Produkty
    GROUP BY ID_Zamowienia
    '''
col_names = [desc[0] for desc in con.execute(query65).description]
print(col_names)
for t in cur.execute(query65):
    print(*t)