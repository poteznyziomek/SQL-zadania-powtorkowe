import sqlite3 as sql
import os.path

def create_tables():
	'''Create empty database sklep.db with 4 tables.'''
	con = sql.connect('sklep.db')
	cur = con.cursor()

	create_Klienci = '''
		CREATE TABLE Klienci (
			ID_Klienta INT,
			Imie VARCHAR(50),
			Nazwisko VARCHAR(50),
			Email VARCHAR(100) ,
			Telefon VARCHAR(20)
		);
	'''
	create_Zamowienia = '''
		CREATE TABLE Zamowienia (
			ID_Zamowienia INT,
			ID_Klienta INT,
			Data_Zamowienia DATE,
			Kwota DECIMAL(10, 2),
			Ilosc INT
		);
	'''
	create_Produkty = '''
		CREATE TABLE Produkty (
			ID_Produktu INT,
			Nazwa VARCHAR(100),
			Cena DECIMAL(10, 2)
		);
	'''
	create_Pozycje_Zamowienia = '''
		CREATE TABLE Pozycje_Zamowienia (
			ID_Pozycji INT PRIMARY KEY,
			ID_Zamowienia INT,
			ID_Produktu INT,
			Ilosc INT
		);
	'''
	tables = [create_Klienci, create_Zamowienia,
		   create_Produkty, create_Pozycje_Zamowienia]
	for table in tables:
		cur.execute(table)
	con.commit()
	con.close()

def populate_tables():
	'''Insert values into tables.'''
	if os.path.exists('sklep.db'):
		con = sql.connect('sklep.db')
		cur = con.cursor()
	else:
		raise Exception('sklep.db does not exist.')
	query1 = '''
		INSERT INTO Klienci VALUES
		(1, 'Jan', 'Kowalski', 'jan.kowalski@example.com', '123456789'),
		(2, 'Anna', 'Nowak', '@example.com', '987654321'),
		(3, 'Piotr', 'Wiśniewski', 'piotr.w@example.com', '555555555'),
		(4, 'Maria', 'Zielińska', 'm.zielinska@example.com', '777888999'),
		(5, 'Maria', 'Zielińska', 'm.zielinska@example.com', '777888999');
	'''
	query2 = '''
		INSERT INTO Zamowienia VALUES
		(1, 1, '2025-05-10', 3575.00, 2),
		(2, 2, '2025-05-11', 6575.00, 7),
		(3, 1, '2025-06-01', 4700.00, 2),
		(4, 3, '2025-06-03', 1200.00, 1),
		(5, 4, '2025-05-15', 7075.00, 3),
		(6, 1, '2025-05-16', 14000.00, 4),
		(7, 1, '2025-05-16', 1400.00, 2),
		(8, 3, '2025-05-30', 3500.00, 1),
		(9, 3, '2025-05-11', 3500.00, 1),
		(10, 1, '2025-05-13', 1.00, 1);
	'''
	query3 = '''
		INSERT INTO Produkty VALUES
		(1, 'Laptop', 3500.00),
		(2, 'Myszka', 75.00),
		(3, 'Monitor', 1200.00),
		(4, 'Klawiatura', 200.00);
	'''
	query4 = '''
		INSERT INTO Pozycje_Zamowienia VALUES
		(1, 1, 1, 1),
		(2, 1, 2, 1),
		(3, 2, 1, 1),
		(4, 2, 2, 1),
		(5, 2, 3, 2),
		(6, 2, 4, 3),
		(7, 3, 1, 1),
		(8, 3, 3, 1),
		(9, 4, 3, 1),
		(10, 5, 1, 2),
		(11, 5, 2, 1),
		(12, 6, 1, 4),
		(13, 7, 3, 1),
		(14, 7, 4, 1),
		(15, 8, 1, 1),
		(16, 9, 1, 1),
		(17, 9, 2, 1),
		(18, 10, 4, 1);
	'''
	queries = [query1, query2, query3, query4]
	for query in queries:
		cur.execute(query)
	con.commit()
	con.close()

def dbinit():
	'''Create tables and populate them.'''
	create_tables()
	populate_tables()