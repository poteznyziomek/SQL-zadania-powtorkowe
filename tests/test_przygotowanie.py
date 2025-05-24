import unittest, os.path, os
import sqlite3 as sql
import sqlpowtorka.przygotowanie as prep

class DataBaseCreation(unittest.TestCase):

    def setUp(self):
        '''Create the database and connect to it.'''
        try:
            prep.create_tables()
        except Exception as e:
            if os.path.exists('sklep.db'):
                os.unlink('sklep.db')
            print(e)
            raise

        if os.path.exists('sklep.db'):
            self.con = sql.connect('sklep.db')
            self.cur = self.con.cursor()
        else:
            raise Exception('Failed to connect to the database: sklep.db does not exist.')

    
    def tearDown(self):
        '''Close connection to sklep.db and delete its file.'''
        self.con.close()
        cur_dir = os.getcwd()
        (head, tail) = os.path.split(cur_dir)
        if tail == 'tests':
            os.chdir('..')
            cur_dir = os.getcwd()
            (head, tail) = os.path.split(cur_dir)
        if os.path.exists('sklep.db'):
            os.unlink('sklep.db')
        else:
            raise Exception(f'no file named sklep.db inside {tail}.')
    
    def test_existance_Klienci(self):
        '''Table Klienci exists and is empty.'''
        query = '''
            SELECT *
            FROM Klienci;
        '''
        res = self.cur.execute(query)
        self.assertListEqual(res.fetchall(), [])

    def test_existance_Zamowienia(self):
        '''Table Zamowienia exists and is empty.'''
        query = '''
            SELECT *
            FROM Klienci;
        '''
        res = self.cur.execute(query)
        self.assertListEqual(res.fetchall(), [])

    def test_existance_Produkty(self):
        '''Table Produkty exists and is empty.'''
        query = '''
            SELECT *
            FROM Klienci;
        '''
        res = self.cur.execute(query)
        self.assertListEqual(res.fetchall(), [])

    def test_existance_Pozycje_Zamowienia(self):
        '''Table Pozycje_Zamowienia exists and is empty.'''
        query = '''
            SELECT *
            FROM Klienci;
        '''
        res = self.cur.execute(query)
        self.assertListEqual(res.fetchall(), [])


class DataBaseValues(unittest.TestCase):

    def setUp(self):
        '''Create the database and connect to it.'''
        try:
            prep.create_tables()
            prep.populate_tables()
        except Exception as e:
            if os.path.exists('sklep.db'):
                os.unlink('sklep.db')
            print(e)
            raise

        if os.path.exists('sklep.db'):
            self.con = sql.connect('sklep.db')
            self.cur = self.con.cursor()
        else:
            raise Exception('Failed to connect to the database: sklep.db does not exist.')
    
    def tearDown(self):
        '''Close connection to sklep.db and delete its file.'''
        self.con.close()
        cur_dir = os.getcwd()
        (head, tail) = os.path.split(cur_dir)
        if tail == 'tests':
            os.chdir('..')
            cur_dir = os.getcwd()
            (head, tail) = os.path.split(cur_dir)
        if os.path.exists('sklep.db'):
            os.unlink('sklep.db')
        else:
            raise Exception(f'no file named sklep.db inside {tail}.')

    def test_values_Klienci(self):
        '''Klienci table should be populated with tuples.'''
        query = '''
            SELECT *
            FROM Klienci;
        '''
        tuples = [
            (1, 'Jan', 'Kowalski', 'jan.kowalski@example.com', '123456789'),
            (2, 'Anna', 'Nowak', '@example.com', '987654321'),
            (3, 'Piotr', 'Wiśniewski', 'piotr.w@example.com', '555555555'),
            (4, 'Maria', 'Zielińska', 'm.zielinska@example.com', '777888999'),
            (5, 'Maria', 'Zielińska', 'm.zielinska@example.com', '777888999')
        ]
        res = self.cur.execute(query)
        self.assertListEqual(tuples, res.fetchall())

    def test_values_Zamowienia(self):
        '''Zamowienia table should be populated with tuples.'''
        query = '''
            SELECT *
            FROM Zamowienia;
        '''
        tuples = [
            (1, 1, '2025-05-10', 3575.00, 2),
            (2, 2, '2025-05-11', 6575.00, 7),
            (3, 1, '2025-06-01', 4700.00, 2),
            (4, 3, '2025-06-03', 1200.00, 1),
            (5, 4, '2025-05-15', 7075.00, 3),
            (6, 1, '2025-05-16', 14000.00, 4),
            (7, 1, '2025-05-16', 1400.00, 2),
            (8, 3, '2025-05-30', 3500.00, 1),
            (9, 3, '2025-05-11', 3500.00, 1),
            (10, 1, '2025-05-13', 1.00, 1)
        ]
        res = self.cur.execute(query)
        self.assertListEqual(tuples, res.fetchall())

    def test_values_Produkty(self):
        '''Produkty table should be populated with tuples.'''
        query = '''
            SELECT *
            FROM Produkty;
        '''
        tuples = [
            (1, 'Laptop', 3500.00),
            (2, 'Myszka', 75.00),
            (3, 'Monitor', 1200.00),
            (4, 'Klawiatura', 200.00)
        ]
        res = self.cur.execute(query)
        self.assertListEqual(tuples, res.fetchall())

    def test_values_Pozycje_Zamowienia(self):
        ''' table should be populated with tuples.'''
        query = '''
            SELECT *
            FROM Pozycje_Zamowienia;
        '''
        tuples = [
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
            (18, 10, 4, 1)
        ]
        res = self.cur.execute(query)
        self.assertListEqual(tuples, res.fetchall())


if __name__ == '__main__':
    unittest.main(verbosity=2)