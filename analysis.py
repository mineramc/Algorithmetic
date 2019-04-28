import os
import psycopg2
import random
import time
#replacement for real query from app
query = True



class Tag:
    def __init__(self, operation, tier):
        self.tier = tier
        self.operation = operation

        if self.operation == "a":
            self.num1 = random.randint(1, 5 ** self.tier)
            self.num2 = random.randint(1, 5 ** self.tier)
            self.answer = self.num1 + self.num2
        elif self.operation == "m":
            self.num1 = random.randint(1, 2 ** self.tier)
            self.num2 = random.randint(1, 2 ** self.tier)
            self.answer = self.num1 * self.num2
        elif self.operation == "s" and self.tier >= 3:
            self.num1 = random.randint(1, 5 ** self.tier)
            self.num2 = random.randint(1, 5**self.tier)
            self.answer = self.num1 - self.num2
        elif self.operation == "s" and self.tier < 3:
            self.num2 = random.randint(1, 5**self.tier)
            self.num1 = random.randint(self.num2, 5**self.tier)
            self.answer = self.num1 - self.num2
        else:
            self.num2 = random.randint(1, 2**self.tier)
            self.num1 = self.num2 * random.randint(1, 2**self.tier)
            self.answer = int(self.num1 / self.num2)

    def getTier(self):
        return self.tier

    def getOperation(self):
        return self.operation

    def getAns(self):
        return self.answer

    def getProblem(self):
        question = ""
        question += str(self.num1)
        if self.operation == "a":
            question += "+"
            question += str(self.num2)
        elif self.operation == "s":
            question += "-"
            question += str(self.num2)
        elif self.operation == "m":
            question += "*"
            question += str(self.num2)
        else:
            question += "/"
            question += str(self.num2)

        return question


def parseTag(tag):
    return str(tag.getOperation()) + str(tag.getTier())


def lowTier(information):
    mini = 2000000000
    counter = 0
    target = 0
    for i in range(8):
        if i%2 != 0 and int(information[i]) < mini:
            mini = int(information[i])
            target = counter
        counter += 1
    lowest = (information[target-1], int(information[target]))
    return lowest


os.environ['DATABASE_URL'] = 'postgres://ekirkjbjamwpuk:ac7ebcbf546993450ac6081d88b0c3d92cb2d856b4d99d2cd74c0b379cbc8c09@ec2-54-225-242-183.compute-1.amazonaws.com:5432/d3c2hbdtu8ra5c'
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


while 1:

    # get whether or not it needs a question from the SQL database
    cur = conn.cursor()
    cur.execute("SELECT * FROM updates;")
    query = cur.fetchone()[1]  # problemState from SQL database (true = generate problem)
    cur.close()

    # get current tag status from database
    cur = conn.cursor()
    cur.execute("SELECT * FROM stat;")
    info = cur.fetchone()[3]
    cur.close()

    if query:
        if int(info[1]) == 9 and int(info[3]) == 9 and int(info[5]) == 9 and int(info[7]) == 9:
            a1 = 2 * random.randint(0, 3) + 1
            a2 = a1-1
            tag = Tag(info[a2], int(info[a1]))
        else:
            a = lowTier(info)
            tag = Tag(a[0], int(a[1]))
        problem = tag.getProblem()
        answer = tag.getAns()
        returnTag = parseTag(tag)

        print(problem)
        print(answer)
        print(returnTag)

        cur = conn.cursor()
        cur.execute("INSERT INTO problem (problem, answer, tags) VALUES (%s, %s, %s)", (problem, answer, returnTag))
        cur.execute("SELECT aid FROM problem WHERE problem = %s", (problem,))
        curID = cur.fetchone()[0]
        cur.execute("UPDATE transfer SET aid = %s, problem = %s WHERE aid = %s", (curID, problem, curID-1))
        # toggle question state back to false (question is submitted)
        cur = conn.cursor()
        cur.execute("UPDATE updates SET qs1 = %s WHERE id = %s", ("false", "1"))
        conn.commit()
        cur.close()

        # update overall tags for current performance
        cur = conn.cursor()
        cur.execute("UPDATE stat SET tags = %s WHERE aid = %s", (info, 1))
        conn.commit()
        cur.close()

    time.sleep(0.1)
