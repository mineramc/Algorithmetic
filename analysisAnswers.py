import os
import psycopg2
import time


os.environ['DATABASE_URL'] = 'postgres://ekirkjbjamwpuk:ac7ebcbf546993450ac6081d88b0c3d92cb2d856b4d99d2cd74c0b379cbc8c09@ec2-54-225-242-183.compute-1.amazonaws.com:5432/d3c2hbdtu8ra5c'
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

totalCorrect = 0
totalCorrects = [0, 0, 0, 0]
total = 0
totals = [0, 0, 0, 0]

def parseTag(tag):  # tag is in the form a#s#m#d#
    mini = 2000000000
    counter = 0
    target = 0
    for i in range(8):
        if i % 2 != 0 and int(tag[i]) < mini:
            mini = int(tag[i])
            target = counter
        counter += 1
    active = tag[target - 1] + tag[target]
    return active


def initApp(activeID): # loop through all existing problems and answers
    cur = conn.cursor()
    cur.execute("SELECT * FROM answers")

    # Loop through all existing answers to error check/reboot on recovery
    for row in cur:

        global total
        global totalCorrect
        global totals
        global totalCorrects

        # increment total number of questions
        total += 1

        curProblems = conn.cursor()
        test = str(activeID)
        curProblems.execute("SELECT * FROM problem WHERE aid = %s;", (test,))  # aID = ID of active problem
        aTemp = curProblems.fetchone()
        correct = aTemp[2]
        curProblems.close()

        # get answer (aTemp)
        curAnswers = conn.cursor()
        curAnswers.execute("SELECT * FROM answers WHERE aid = %s;", (test,))  # aID = ID of active problem
        aTemp1 = curAnswers.fetchone()
        answer = aTemp1[2]  # answer = inputted answer
        curAnswers.close()

        # get active tag
        tags = aTemp[3]
        print(tags)

        # compare answers
        cur = conn.cursor()
        isCorrect = str(float(correct) == float(answer))
        cur.execute("UPDATE answers SET isc = %s WHERE aid = %s", (isCorrect, activeID))
        conn.commit()
        print(aTemp)
        activeID += 1

        isCorrect = float(correct) == float(answer)
        # update total questions per category
        if tags[0] == "a":
            totals[0] += 1
        elif tags[0] == "s":
            totals[1] += 1
        elif tags[0] == "m":
            totals[2] += 1
        else:
            totals[3] += 1

        # update total correct per category
        if bool(isCorrect):
            totalCorrect += 1
            if tags[0] == "a":
                totalCorrects[0] += 1
            elif tags[0] == "s":
                totalCorrects[1] += 1
            elif tags[0] == "m":
                totalCorrects[2] += 1
            else:
                totalCorrects[3] += 1
        cur.close()
    cur = conn.cursor()
    cur.execute("UPDATE stat SET cate = %s WHERE aid = %s", ('.'.join(list(map(str, totals))), "1"))
    cur.execute("UPDATE stat SET totalcate = %s WHERE aid = %s", ('.'.join(list(map(str, totalCorrects))), "1"))
    conn.commit()
    cur.close()
    return activeID


cur = conn.cursor()
cur.execute("SELECT * FROM problem;")
aID = int(cur.fetchone()[0])
aID = initApp(aID)
print(aID)

while 1:
    #curAnswers.execute("SELECT * FROM ")
    # update statistics table

    # check if answer is posted
    cur = conn.cursor()
    cur.execute("SELECT * FROM updates;")
    answerState = cur.fetchone()
    cur.close()


    # if answer inputted
    if answerState[0]:

        total += 1 # increment total by 1

        # Get current problem and answer
        curProblems = conn.cursor()
        test = str(aID)
        curProblems.execute("SELECT * FROM problem WHERE aid = %s;", (test,))  # aID = ID of active problem
        aTemp = curProblems.fetchone()
        correct = aTemp[2]
        curProblems.close()

        # get inputted answer (aTemp)
        curAnswers = conn.cursor()
        curAnswers.execute("SELECT * FROM answers WHERE aid = %s;", (test,))  # aID = ID of active problem
        aTemp1 = curAnswers.fetchone()
        answer = aTemp1[2]  # answer = inputted answer
        curAnswers.close()

        # get active tag
        active = aTemp[3]
        print(active)

        # get all tags
        cur = conn.cursor()
        cur.execute("SELECT * FROM stat")
        aTemp1 = cur.fetchone()
        cur.close()
        tags = aTemp1[3]
        tagList = list(tags)

        # find index of active tag
        indexA = tags.index(active[0])

        # compare answers
        cur = conn.cursor()
        isCorrect = str(float(correct) == float(answer))
        cur.execute("UPDATE answers SET isc = %s WHERE aid = %s", (isCorrect, aID))
        conn.commit()
        print(aTemp)

        # update total questions per category
        if active[0] == "a":
            totals[0] += 1
        elif active[0] == "s":
            totals[1] += 1
        elif active[0] == "m":
            totals[2] += 1
        else:
            totals[3] += 1

        # lower tier if incorrect, increase tier if correct
        isCorrect = float(correct) == float(answer)
        if isCorrect:
            currentTier = int(active[1])
            if currentTier + 1 < 10:
                active = active[0] + str(currentTier + 1)
            totalCorrect += 1

            # increment total correct by 1 for the category
            if active[0] == "a":
                totalCorrects[0] += 1
            elif active[0] == "s":
                totalCorrects[1] += 1
            elif active[0] == "m":
                totalCorrects[2] += 1
            else:
                totalCorrects[3] += 1

        else:
            currentTier = int(active[1])
            print(currentTier)
            if currentTier - 1 > 0:
                active = active[0] + str(currentTier - 1)
            print(currentTier)


        # update overall tags

        tagList[indexA] = active[0]
        tagList[indexA+1] = active[1]
        tags = ''.join(tagList)
        cur.execute("UPDATE stat SET tags = %s WHERE aid = %s", (tags, 1))

        # set answerState to false
        cur.execute("UPDATE updates SET as1 = %s WHERE id = %s", ("false", "1"))
        conn.commit()

        # generate new problem
        cur.execute("UPDATE updates SET qs1 = %s WHERE id = %s", ("true", "1"))
        conn.commit()

        # update total correct and total questions
        cur.execute("UPDATE stat SET cate = %s WHERE aid = %s", ('.'.join(list(map(str, totalCorrects))), "1"))
        cur.execute("UPDATE stat SET totalcate = %s WHERE aid = %s", ('.'.join(list(map(str, totals))), "1"))
        conn.commit()
        cur.close()
        aID += 1

    time.sleep(0.1)


cur.close()
conn.close()
