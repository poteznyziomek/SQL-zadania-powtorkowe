import sqlpowtorka.przygotowanie as prep
import os.path, os
import sqlite3 as sql

if os.path.exists('sklep.db'):
    os.unlink('sklep.db')
try:
    prep.dbinit()
    #Import zestaw1 here if you want changes to the db
    #from tasks over there.
    if os.path.exists('sklep.db'):
        con = sql.connect('sklep.db')
        cur = con.cursor()
    else:
        raise Exception('no file named sklep.db')
except Exception as e:
    print(e)
    raise

tables = ['Klienci', 'Zamowienia',
          'Produkty', 'Pozycje_Zamowienia'
]
query_attributes = '''
    SELECT *
    FROM {};
'''
# Dictionary with key = name of the table in the db and
# value = attributes of the corresponging table.
attributes_list = {table:attributes for table, attributes in zip(tables, [[desc[0] for desc in con.execute(q).description] for q in [query_attributes.format(item) for item in tables]])}

# 1. Wyświetl zawartość wszystkich 3 tabel i zobacz jakie dane zawierają
# for table in tables:
#     print(f'Tabela {table}')
#     print(attributes_list[table])
#     res = cur.execute(query_attributes.format(table))
#     for t in res.fetchall():
#         print(t)
#     print()

# 2. Wyświetl tylko imię i nazwisko klienta o ID 1
query1 = '''
    SELECT Imie 'Imię', Nazwisko
    FROM Klienci
    WHERE ID_Klienta = 1;
'''
res = cur.execute(query1)
# print(res.fetchall())

# 3. Wyświetl wszystkie zamówienia złożone po 30 maja 2025
query2 = '''
    SELECT *
    FROM Zamowienia
    WHERE Data_Zamowienia > '2025-05-30';
'''
res = cur.execute(query2)
# print(res.fetchall())

# 4. Znajdź zamówienia, w których zamówiono więcej niż 3 sztuki
query3 = '''
    SELECT *
    FROM Zamowienia
    WHERE Ilosc > 3;
'''
res = cur.execute(query3)
# print(res.fetchall())

# 5. Wyświetl unikalne adresy email klientów
query4 = '''
    SELECT DISTINCT Imie 'Imię', Nazwisko, Email
    FROM Klienci;
'''
res = cur.execute(query4)
# print(res.fetchall())

# 6. Wyświetl liczbę wszystkich zamówień
query5 = '''
    SELECT COUNT(*)
    FROM Zamowienia;
'''
res = cur.execute(query5)
# print(res.fetchall())

# 7. Wyświetl liczbę zamówień każdego klienta
query6 = '''
    SELECT ID_Klienta, Imie 'Imię', Nazwisko, COUNT(*) AS 'Ilość zamówień'
    FROM Klienci NATURAL JOIN Zamowienia
    GROUP BY ID_Klienta;
'''
col_names = [desc[0] for desc in con.execute(query6).description]
# print(col_names)
# for t in cur.execute(query6):
#     print(*t)

# 8. Oblicz łączną liczbę zamówionych produktów dla każdego klienta
query7 = '''
    SELECT ID_Klienta, Imie 'Imię', Nazwisko, SUM(Ilosc) AS 'Ilość zamówionych produktów'
    FROM Klienci NATURAL JOIN Zamowienia
    GROUP BY ID_Klienta;
'''
col_names = [desc[0] for desc in con.execute(query7).description]
# print(col_names)
# for t in cur.execute(query7):
#     print(*t)

# 9. Oblicz średnią ilość sztuk na zamówienie
query8 = '''
    SELECT AVG(Ilosc) 'średnia ilość sztuk na zamówienia'
    FROM Zamowienia;
'''
col_names = [desc[0] for desc in con.execute(query8).description]
# print(col_names)
# for t in cur.execute(query8):
#     print(*t)

# 10. Oblicz maksymalną i minimalną ilość sztuk w jednym zamówieniu
query91 = '''
    SELECT MAX(Ilosc) 'Maksymalna ilość sztuk w jednym zamówieniu'
    FROM Zamowienia;
'''
query92 = '''    
    SELECT MIN(Ilosc) 'Minimalna ilość sztuk w jednym zamówieniu'
    FROM Zamowienia;
'''
col_names = [desc[0] for desc in con.execute(query91).description]
# print(col_names)
# for t in cur.execute(query91):
#     print(*t)
col_names = [desc[0] for desc in con.execute(query92).description]
# print(col_names)
# for t in cur.execute(query92):
#     print(*t)

# 11. Podaj klientów, którzy złożyli więcej niż 2 zamówienia
query10 = '''
    SELECT Imie 'Imię', Nazwisko
    FROM Klienci NATURAL JOIN Zamowienia
    GROUP BY ID_Klienta
    HAVING COUNT(ID_Zamowienia) > 2;
'''
col_names = [desc[0] for desc in con.execute(query10).description]
# print(col_names)
# for t in cur.execute(query10):
#     print(*t)

# 12. Podaj daty, w których złożono więcej niż jedno zamówienie
query11 = '''
    SELECT Data_Zamowienia
    FROM Zamowienia
    GROUP BY Data_Zamowienia
    HAVING COUNT(*) > 1;
'''
col_names = [desc[0] for desc in con.execute(query11).description]
# print(col_names)
# for t in cur.execute(query11):
#     print(*t)

# 13. Zlicz liczbę unikalnych klientów, którzy złożyli zamówienia
query12 = '''
    SELECT COUNT(*) AS 'Unikalni klienci, którzy złożyli zamówienia'
    FROM Klienci NATURAL JOIN 
        (SELECT DISTINCT ID_Klienta
        FROM Zamowienia);
    '''
col_names = [desc[0] for desc in con.execute(query12).description]
# print(col_names)
# for t in cur.execute(query12):
#     print(*t)

# 14. Podaj ID klienta i łączną liczbę zamówionych sztuk, posortowaną malejąco
query13 = '''
    SELECT ID_Klienta, SUM(Ilosc) 'łączna liczba zamówionych sztuk'
    FROM Klienci NATURAL JOIN Zamowienia
    GROUP BY ID_Klienta
    ORDER BY SUM(Ilosc) DESC;
    '''
col_names = [desc[0] for desc in con.execute(query13).description]
# print(col_names)
# for t in cur.execute(query13):
#     print(*t)

# 15. Znajdź średnią liczbę sztuk w zamówieniu na klienta
query14 = '''
    SELECT ID_Klienta, AVG(Ilosc) 'średnia liczba zamówionych sztuk'
    FROM Zamowienia
    GROUP BY ID_Klienta;'''
col_names = [desc[0] for desc in con.execute(query14).description]
# print(col_names)
# for t in cur.execute(query14):
#     print(*t)

# 16. Znajdź klientów, którzy złożyli dokładnie 4 zamówienia
query15 = '''
    SELECT ID_Klienta, Imie 'Imię', Nazwisko, COUNT(ID_Zamowienia)
    FROM Klienci NATURAL JOIN Zamowienia
    GROUP BY ID_Klienta
    HAVING COUNT(ID_Zamowienia) = 4;'''
col_names = [desc[0] for desc in con.execute(query15).description]
# print(col_names)
# for t in cur.execute(query15):
#     print(*t)

# 17. Dla każdego klienta wyświetl łączną liczbę zamówień oraz sumę ich wartości
query16 = '''
    SELECT ID_Klienta 'ID', Imie 'Imię', Nazwisko, COUNT(ID_Zamowienia) 'łączna liczba zamówień', SUM(Kwota) 'wartość'
    FROM Klienci NATURAL JOIN Zamowienia
    GROUP BY ID_Klienta;'''
col_names = [desc[0] for desc in con.execute(query16).description]
print(col_names)
for t in cur.execute(query16):
    print(*t)