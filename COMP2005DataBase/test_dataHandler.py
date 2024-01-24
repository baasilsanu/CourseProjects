from dataHandler import dataBaseHandler
from unittest import TestCase

class TestUserStorage(TestCase):
    def setUp(self):
        self.handler = dataBaseHandler()

    def tearDown(self):
        self.handler.removeUser("10")

    def test_addUser(self):
        user = (10, "John", "12345")
        self.handler.addUser(user)
        self.assertEqual(self.handler.lookUpUserID(user[0])[0], user)

    def test_lookUpUserID(self):
        user = (10, "John", "12345")
        self.handler.addUser(user)
        self.assertEqual(self.handler.lookUpUserID(user[0])[0], user)

    def test_lookUpUserName(self):
        user = (10, "John", "12345")
        self.handler.addUser(user)
        self.assertEqual(self.handler.lookUpUserName(user[1])[0], user)

    def test_removeUser(self):
        user = (10, "John", "12345")
        self.handler.addUser(user)
        self.handler.removeUser(user[0])
        with self.assertRaises(IndexError):
            self.assertNotEqual(self.handler.lookUpUserName(user[1])[0], user)

class TesttopicStorage(TestCase):
    def setUp(self):
        self.handler = dataBaseHandler()
        user = (11, "Johnny", "12345")
        self.handler.addUser(user)
        topic = ("21-02-2023 17:42", "Johnny", "Hello", "1")
        self.handler.addtopic(topic)

    def tearDown(self):
        user = (11, "Johnny", "12345")
        topic = ("21-02-2023 17:42", "Johnny", "Hello", "1")
        self.handler.deletetopic(topic[1], topic[3])
        self.handler.removeUser(str(user[0]))

    def test_addtopic(self):
        user = (11, "Johnny", "12345")
        topic = ("21-02-2023 17:42", "Johnny", "Hello", 1)
        self.assertEqual(self.handler.lookUpSpecifictopic(user[1], topic[3])[0], topic)

    def test_deletetopic(self):
        user = (11, "Johnny", "12345")
        topic = ("21-02-2023 17:42", "Johnny", "Hello", 1)
        self.handler.addtopic(topic)
        self.handler.deletetopic(topic[1], topic[3])
        with self.assertRaises(IndexError):
            self.assertNotEqual(self.handler.lookUpSpecifictopic(user[1], topic[3])[0], topic)

    def test_getRatings(self):
        user = (11, "Johnny", "12345")
        topic = ("21-02-2023 17:42", "Johnny", "Hello", 1)
        self.assertEqual(self.handler.getSpecifictopicRatings("Johnny", 1), (5, 5, 0, 0))

    def test_getSubstring(self):
        user = (11, "Johnny", "12345")
        topic = ("21-02-2023 17:42", "Johnny", "Hello", 1)
        self.assertEqual(self.handler.lookUpSpecificSubstring("llo"), topic)







if '__name__' == '__main__':
    unittest.main()