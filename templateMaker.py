#templateMaker.py
from pprint import pprint as pp

def cleanTask(task, name):
    switch = {"@":"\"", "image/":"image/{0}/"}
    f = task
    for k in switch:
        f = f.replace(k,switch[k]).strip("\n")

    return f
def addTest(template, tests = {"505":{"11:47:00":"image/{0}/18.png"}}, name = "XXXNAMEXXX"):
    for newDay in tests:
        template[newDay] = {}
        for t in tests[newDay]:
            template[newDay][t] =  tests[newDay][t].format(name)
    return template
def rawToTemplate(rawTxt, name = "XXXNAMEXXX",lastDay = 18, taskTime = "20:00", preTimeMorning = "12:00", preTimeEvening = "18:00", space = 8, extra = {"19:45:00":"#totalPoints","20:00:00":"image/{0}/{1}.png","20:00:{0}":"image/{0}/{1}.opus"}):
    # alldays = rawTxt.split("%%%%%%%%%%%%")
    # pre = alldays[:-1*lastDay]
    # days = alldays[-1*lastDay:]
    # alldays = rawTxt.split("%%%%%%%%%%%%")
    pre = rawTxt.split("$$$$$$$$$$$$$$$$$")[0].split("%%%%%%%%%%%%")
    days =  rawTxt.split("$$$$$$$$$$$$$$$$$")[1].split("%%%%%%%%%%%%")
    template = {}
    lastSeconds = 0
    for i in range(len(pre)):
        I = (i-(len(pre)-1)) # starts at Minus days in pre up to 0
        # print("pre DAY",I)
        template[I] = {}
        counter = 0
        afterMorning = False
        for task in pre[i].split("#######################"):
            if "~~~~~~~~~~~~~~~~~~~~~~~" in task:
                afterMorning = True
                counter = 0
            else:
                counter += 1
                preT = preTimeMorning + ""
                if afterMorning:
                    preT = preTimeEvening + ""
                addT = ":"
                seconds = int(space*(counter)%60)
                lastSeconds = int(space*(counter+1)%60)
                secondsT = str(seconds)
                if len(secondsT) < 2:
                    secondsT = "0"+secondsT
                addT = addT + secondsT
                if space*(counter) > 60:
                    minutes = int(space*(counter)/60)
                    if minutes > 0:
                        preT = preT[:-1*len(str(minutes))]+str(minutes)
                preT += addT
                template[I][preT] = cleanTask(task,name).format(name,I)

    for i in range(len(days)):
        cDay = i+1 # starts from day 1
        template[cDay] = {}
        counter = 0
        for task in days[i].split("#######################"):
            counter += 1
            taskT = taskTime + ""
            addT = ":"
            seconds = int(space*(counter)%60)
            lastSeconds = int(space*(counter+1)%60)
            secondsT = str(seconds)
            if len(secondsT) < 2:
                secondsT = "0"+secondsT
            addT = addT + secondsT
            if space*(counter) > 60:
                minutes = int(space*(counter)/60)
                if minutes > 0:
                    taskT = taskT[:-1*len(str(minutes))]+str(minutes)
            taskT += addT
            template[cDay][taskT] = cleanTask(task,name).format(name,cDay)
        for e in extra:
            formattedExtra = extra[e].format(name,cDay)
            if not ("#totalPoints" in formattedExtra and cDay == 1):
            # if not any(any(formattedExtra.strip() == s for s in subList) for subList in template[cDay].values()):
                already = False
                for v in list(template[cDay].values()):
                    if formattedExtra in v:
                        already = True
                if not already:
                    lastSecondsT = str(lastSeconds)
                    if len(str(lastSeconds)) < 2:
                        lastSecondsT = "0"+lastSecondsT
                    template[cDay][e.format(lastSecondsT)] = formattedExtra
                    # print(".......\n")
                else:
                    pass
                # print("ALREADY\n")

    return addTest(template,name = name)
