#templateMaker.py

def cleanTask(task, name):
    switch = {"@":"\"", "image/":"image/{0}/"}
    f = task
    for k in switch:
        f = f.replace(k,switch[k])

    return f

def rawToTemplate(rawTxt, name = "XXXNAMEXXX",lastDay = 18, taskTime = "20:00", preTime = "20:00", space = 8, extra = {"19:45:00":"#totalPoints","20:00:00":"image/{0}/{1}.png","20:00:{0}":"image/{0}/{1}.opus"}):
    alldays = rawTxt.split("%%%%%%%%%%%%")
    pre = alldays[:-1*lastDay]
    days = alldays[-1*lastDay:]
    template = {}
    lastSeconds = 0
    # for i in range(len(pre)):
    #     I = -1 * (i-(len(pre)-1))
    #     template[I] = {}
    #     counter = 0
    #     for task in pre[i].split("#######################"):
    #         counter += 1
    #         preT = preTime + ""
    #         addT = ":"
    #         seconds = int(space*(counter)%60)
    #         lastSeconds = int(space*(counter+1)%60)
    #         secondsT = str(seconds)
    #         if len(secondsT) < 2:
    #             secondsT = "0"+secondsT
    #         addT = addT + secondsT
    #         if space*(counter) > 60:
    #             minutes = int(space*(counter)/60)
    #             if minutes > 0:
    #                 preT = preT[:-1*len(str(minutes))]+str(minutes)
    #         preT += addT
    #         template[(i+1)][preT] = cleanTask(task,name)

    for i in range(len(days)):
        template[(i+1)] = {}
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
            template[(i+1)][taskT] = cleanTask(task,name)
        for e in extra:
            lastSecondsT = str(lastSeconds)
            if len(str(lastSeconds)) < 2:
                lastSecondsT = "0"+lastSecondsT
            template[(i+1)][e.format(lastSecondsT)] = extra[e].format(name,(i+1))
    return template
