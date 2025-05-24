import sqlpowtorka.przygotowanie as prep
import os.path, os
import sqlite3 as sql

if os.path.exists('sklep.db'):
    os.unlink('sklep.db')
try:
    prep.dbinit()
    if os.path.exists('sklep.db'):
        con = sql.connect('sklep.db')
        cur = con.cursor()
    else:
        raise Exception('no file named sklep.db')
except Exception as e:
    print(e)
    raise

# 1. Utwórz tabelę ,,Produkty_temp” zawierającą następujące kolumny:
#    ID_Produktu – liczba całkowita,
#    Nazwa – typ znakowy o rozmiarze 100,
#    Cena – liczba rzeczywista z dwoma miejscami po przecinku
query1 = '''
    CREATE TABLE Produkty_temp(
        ID_Produktu INT,
        Nazwa CHAR(100),
        Cena DECIMAL(38, 2)
    );
'''
cur.execute(query1)

# 2. Wstaw poniższe dane do utworzonej w p. 1 tabeli:
# | ID_Produktu |  Nazwa |   Cena  |
# | ----------- | ------ | ------- |
# |      1      | Laptop | 3500,00 |
# |      2      | Myszka |  75,00  |
query2 = '''
    INSERT INTO Produkty_temp VALUES
    (1, 'Laptop', 3500.00),
    (2, 'Myszka', 75.00);
'''
cur.execute(query2)

# 3. Dodaj kolumnę “Uwagi”, która może przechowywać 255 znaków
query3 = '''
    ALTER TABLE Produkty_temp ADD  Uwagi VARCHAR(255);
'''
cur.execute(query3)

# 4. Uzupełnij dowolnym komentarzem kolumnę “Uwagi” dla istniejących
# produktów (dla każdego produktu powinna być inna wartość w kolumnie „Uwagi”)
query4 = '''
    UPDATE Produkty_temp
    SET Uwagi = 'Uwaga! Moj nr ID to: ' || ID_Produktu;
'''
cur.execute(query4)

# 5. Sprawdź czy wszystkie dane w tabeli są uzupełnione
query5 = '''
    SELECT *
    FROM Produkty_temp
    WHERE (ID_Produktu IS NULL) OR (Nazwa IS NULL) OR (Cena IS NULL) OR (Uwagi IS NULL);
'''
res5 = cur.execute(query5)
# print(res5.fetchall())

# 6. Zaktualizuj adres email klienta o id 2 do poprawnej wartości
query6 = '''
    UPDATE Klienci
    SET Email = 'anna.nowak@example.com'
    WHERE ID_Klienta = 2;
'''
cur.execute(query6)
res = cur.execute('select * from Klienci;')
# print(res.fetchall())

# 7. Usuń wiersz o ID_Produktu = 2
query7 = '''
    DELETE FROM Produkty_temp
    WHERE ID_Produktu = 2;
'''
cur.execute(query7)
res = cur.execute('select * from Produkty_temp;')
# print(res.fetchall())

# 8. Usuń zamówienia o wartości poniżej 2 zł
value = 2 #zł
query8 = f'''
    DELETE FROM Zamowienia
    WHERE Kwota < {value};
'''
cur.execute(query8)
res = cur.execute('select * from Zamowienia;')
# print(len(res.fetchall()))

# 9. Usuń tabelę „Produkty_temp”
query9 = '''
    DROP TABLE Produkty_temp;
'''
cur.execute(query9)
# res = cur.execute('select * from Produkty_temp;')
# print(res.fetchall())
con.commit()
con.close()