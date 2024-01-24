##Handles all the database operations
import sqlite3

conn = sqlite3.connect("APP.db")
c = conn.cursor()
c.execute(f"""CREATE TABLE IF NOT EXISTS users(
            user_ID int NOT NULL,
            userName varchar(255) NOT NULL,
            password varchar(255) NOT NULL,
            PRIMARY KEY(user_ID)
            )""")
c.execute(f"""CREATE TABLE IF NOT EXISTS messages(
            date varChar(255) NOT NULL,
            userName varchar(255) NOT NULL,
            topic varchar(255) NOT NULL,
            message varchar(255) NOT NULL,
            message_ID int NOT NULL,
            FOREIGN KEY(userName) REFERENCES users(userName)
            )""")
c.execute(f"""CREATE TABLE IF NOT EXISTS messageRatingData(
            userName varchar(255) NOT NULL,
            message_ID int NOT NULL,
            structure blob,
            quality blob,
            likeStat blob,
            dislikeStat blob,
            FOREIGN KEY(userName) REFERENCES users(userName)
            FOREIGN KEY(message_ID) REFERENCES messages(message_ID)
            )""")

c.execute(f"""CREATE TABLE IF NOT EXISTS messageDrafts(
            date varChar(255) NOT NULL,
            userName varchar(255) NOT NULL,
            topic varchar(255) NOT NULL,
            draft varchar(255) NOT NULL,
            draft_ID int NOT NULL,
            FOREIGN KEY(userName) REFERENCES users(userName)
            )""")

c.execute(f"""CREATE TABLE IF NOT EXISTS messageRatingUserList(
            message_ID int NOT NULL,
            likeList str DEFAULT "[]",
            dislikeList str DEFAULT "[]",
            structureList str DEFAULT "[]",
            qualityList str DEFAULT "[]",
            FOREIGN KEY(message_ID) REFERENCES messageRatingData(message_ID),
            FOREIGN KEY(message_ID) REFERENCES messages(message_ID)
            )"""
        )

conn.commit()
conn.close()


class dataBaseHandler:
    """
    Creates a dataBaseHandler Object that is used to manipulate the database
    """
    def __init__(self):
        self._userItems = []
        self._messageItems = []

    def __len__(self):
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        item = c.fetchall()
        conn.commit()
        conn.close()
        return len(item)

    def __iter__(self):
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        item = c.fetchall()
        conn.commit()
        conn.close()
        return iter(item)

    def addUser(self, new_item):
        """
        Adds a new user to the database
        :param new_item: Tuple in the format (user_ID, username, password)
        :return: none
        """
        self._userItems.append(new_item)
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute(f"INSERT INTO users VALUES (?,?,?)", (new_item[0], new_item[1], new_item[2]))
        conn.commit()
        conn.close()

    def lookUpUserID(self, key):
        """
        Looks up a specific record using user_ID
        :param key: user_ID
        :return: A tuple containing user record.
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()

        c.execute(f"SELECT * from users WHERE user_ID = (?)", (key, ))

        item = c.fetchall()
        conn.commit()
        conn.close()
        return item

    def lookUpUserName(self, userName):
        """
        Looks up a specific record using userName
        :param userName: The username
        :return: A tuple containing user record.
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute(f"SELECT * from users WHERE userName = (?)", (userName,))
        item = c.fetchall()
        conn.commit()
        conn.close()
        return item

    def removeUser(self, key):
        """
        removes a user from the database
        :param key: user_ID
        :return: removed user record
        """
        try:
            conn = sqlite3.connect('APP.db')
            c = conn.cursor()
            c.execute(f"DELETE from users WHERE user_ID = (?)", (key,))
            item = c.fetchall()
            conn.commit()
            conn.close()
            return item
        except IndexError:
            print("Not present in Database.")


    def deleteTableUsers(self):
        """
        Delete the users table
        :return: null
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("DROP TABLE users")
        conn.commit()
        conn.close()


    def __iter__(self):
        pass

    def displayTableUsers(self):
        """
        Displays all the user records
        :return: list of all the user records
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        item = c.fetchall()
        conn.commit()
        conn.close()
        return item

    def addMessage(self, new_item):
        """
        Adds a new message to the table
        :param new_item: message information in the form of a tuple
        :return: null
        """
        self._messageItems.append(new_item)
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("INSERT INTO messages VALUES (?,?,?,?, ?)",
                  (new_item[0], new_item[1], new_item[2], new_item[3], new_item[4]))
        # Adding initial ratings, like and dislike counts.
        # The rating system is assumed to be from 0 to 10, so averages are added.
        # Initial like and dislike counts are set to 0.
        c.execute("INSERT INTO messageRatingData VALUES (?,?,?,?,?,?)", (new_item[1], new_item[4], "0", "0", "0", "0"))
        c.execute("INSERT INTO messageRatingUserList VALUES (?, ?, ?, ?, ?)", (new_item[4], "[]", "[]", "[]", "[]"))
        conn.commit()
        conn.close()

    def lookUpuserMessages(self, userName):
        """
        Looks up all the messages of a particular user
        :param userName: userName
        :return: List of all the messages
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute(f"SELECT * from messages WHERE userName = (?)", (userName,))
        item = c.fetchall()
        conn.commit()
        conn.close()
        return item

    def lookUpSpecificMessage(self, messageID):
        """
        Looks up a specific message of a user
        :param messageID: Unique ID of the message
        :return: Returns the specific message
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT * from messages WHERE message_ID = (?)", (messageID,))
        item = c.fetchall()
        conn.commit()
        conn.close()
        return item

    def lookUpSpecificSubstring(self, s):
        """
        Returns all the messages containing the specific substring
        :param s: The substring
        :return:
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT * from messages")
        item = c.fetchall()
        conn.commit()
        conn.close()
        matches = []
        for i in item:
            index = i[3].lower().find(s.lower())
            if index != -1:
                matchItem = i
                matches.append(matchItem)
        return matches


    def updateMessageRating(self, messageID, structure, quality, likeStat, dislikeStat):
        """
        Updates the message ratings for an individual message
        :param messageID: The unique message ID
        :param structure: The rating for the structure
        :param quality: The rating for the quality
        :param likeStat: The like count
        :param dislikeStat: The dislike count
        :return:
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("""UPDATE messageRatingData SET structure = (?), quality = (?), likeStat = (?), dislikeStat = (?) 
                  WHERE message_ID = (?)""", (structure, quality, likeStat, dislikeStat, messageID))
        conn.commit()
        conn.close()

    def getSpecificMessageRatings(self, messageID):
        """
        Returns the ratings for a specific message
        :param messageID: The unique messageID
        :return:
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT * from messageRatingData WHERE message_ID = (?)", (messageID, ))
        item = c.fetchall()
        returnTuple = (item[0][2], item[0][3], item[0][4], item[0][5])
        conn.commit()
        conn.close()
        return returnTuple

    def saveDraft(self, new_item):
        """
        Saves a new draft
        :param new_item: Tuple in the format (time, username, topic, content, draftid)
        :return: null
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("INSERT INTO messageDrafts VALUES (?,?,?,?,?)",
                  (new_item[0], new_item[1], new_item[2], new_item[3], new_item[4]))

        conn.commit()
        conn.close()

    def editDraft(self, draftID, editVal):
        """
        Edits a saved draft
        :param draftID: The unique draft ID
        :editVal: The Updated draft message
        :return: The deleted item
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("UPDATE messageDrafts SET draft = (?) WHERE draft_ID = (?)", (editVal, draftID))
        item = c.fetchall()
        conn.commit()
        conn.close()
        return item

    def deleteDraft(self, draftID):
        """
        Deletes a draft
        :param draftID: Unique draft ID
        :return: the deleted item
        """
        try:
            conn = sqlite3.connect('APP.db')
            c = conn.cursor()
            c.execute("DELETE from messageDrafts WHERE draft_ID = (?)", (draftID,))
            item = c.fetchall()
            conn.commit()
            conn.close()
            return item
        except IndexError:
            print("Does not exist")

    def lookUpSpecificDraft(self, draftID):
        """
        Looks up a specific draft of a user
        :param draftID: Unique draft ID o
        :return: Returns the specific draft
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT * from messageDrafts WHERE draft_ID = (?)", (draftID,))
        item = c.fetchall()
        conn.commit()
        conn.close()
        return item

    def editMessage(self, messageID, editVal):
        """

        :param messageID: THe unique message ID
        :return: The edited item
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("UPDATE messages SET message = (?) WHERE message_ID = (?)", (editVal, messageID))
        item = c.fetchall()
        conn.commit()
        conn.close()
        return item


    def deleteMessage(self, messageID):
        """
        Deletes a message
        :param messageID: Unique message ID
        :return: the deleted item
        """
        try:
            conn = sqlite3.connect('APP.db')
            c = conn.cursor()
            c.execute("DELETE from messages WHERE message_ID = (?)", (messageID,))
            c.execute("DELETE from messageRatingData WHERE message_ID = (?)", (messageID,))
            item = c.fetchall()
            conn.commit()
            conn.close()
            return item
        except IndexError:
            print("Does not exist")

    def deleteTableMessages(self):
        """
        Delete the messages table
        :return: null
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("DROP TABLE messages")
        c.execute("DROP TABLE messageRatingData")
        conn.commit()
        conn.close()


    def displayTableMessages(self):
        """
        Displays all the messages
        :return: null
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT * FROM messages")
        item = c.fetchall()
        conn.commit()
        conn.close()
        return item

    def displayTableMessageRatings(self):
        """
        Displays all the message ratings.
        :return: null
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT * FROM messageRatingData")
        item = c.fetchall()
        conn.commit()
        conn.close()
        return item

    def getLikeList(self, message_ID):
        """

        :param message_ID: the message ID of the specific message
        :return: The Likelist of the message
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT likeList FROM messageRatingUserList WHERE message_ID = (?)", (message_ID, ))
        item = c.fetchone()
        conn.commit()
        conn.close()
        return item
    
    def setLikeList(self, message_ID, data):
        """

        :param message_ID: The specific message id of the message
        :param data: The new value to be set
        :return: null
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("UPDATE messageRatingUserList SET likeList = (?) WHERE message_ID = (?)", (data, message_ID))
        conn.commit()
        conn.close()
    
    def getDislikeList(self, message_ID):
        """

        :param message_ID: the message ID of the specific message
        :return: The dislikelist of the message
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT dislikeList FROM messageRatingUserList WHERE message_ID = (?)", (message_ID, ))
        item = c.fetchone()
        conn.commit()
        conn.close()
        return item
    
    def setDislikeList(self, message_ID, data):
        """

        :param message_ID: The specific message id of the message
        :param data: The new value to be set
        :return: null
        """

        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("UPDATE messageRatingUserList SET dislikeList = (?) WHERE message_ID = (?)", (data, message_ID))
        conn.commit()
        conn.close()

    def getQualityList(self, message_ID):
        """
        :param message_ID: the message ID of the specific message
        :return: The quality rating list of the message
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT qualityList FROM messageRatingUserList WHERE message_ID = (?)", (message_ID, ))
        item = c.fetchone()
        conn.commit()
        conn.close()
        return item

    def setQualityList(self, message_ID, data):
        """

        :param message_ID: The specific message id of the message
        :param data: The new value to be set
        :return: null
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("UPDATE messageRatingUserList SET qualityList = (?) WHERE message_ID = (?)", (data, message_ID))
        conn.commit()
        conn.close()

    def getStructureList(self, message_ID):
        """
        :param message_ID: the message ID of the specific message
        :return: The structure rating list of the message
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT structureList FROM messageRatingUserList WHERE message_ID = (?)", (message_ID, ))
        item = c.fetchone()
        conn.commit()
        conn.close()
        return item

    def setStructureList(self, message_ID, data):
        """

        :param message_ID: The specific message id of the message
        :param data: The new value to be set
        :return: null
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("UPDATE messageRatingUserList SET structureList = (?) WHERE message_ID = (?)", (data, message_ID))
        conn.commit()
        conn.close()

    def getUserID(self, username):
        """

        :param username: The username of the user
        :return: The user ID of the user with the username
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE userName = (?)", (username, ))
        item = c.fetchone()[0]
        conn.commit()
        conn.close()
        return item

    def getPassword(self, userID):
        """

        :param userID: The userID of the user whose password is requrired
        :return: The password
        """

        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE user_ID = (?)", (userID, ))
        item = c.fetchone()[0]
        conn.commit()
        conn.close()
        return item

    def setPassword(self, username, password):
        """

        :param username: The username of the user
        :param password: The new password
        :return: null
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("UPDATE users SET password = (?) WHERE userName = (?)", (password, username))
        conn.commit()
        conn.close()

    def setUsername(self, username, userID):
        """

        :param username: The new username
        :param userID: The userID of the user
        :return: null
        """
        conn = sqlite3.connect('APP.db')
        c = conn.cursor()
        c.execute("UPDATE users SET userName = (?) WHERE user_ID = (?)", (username, userID))
        conn.commit()
        conn.close()

