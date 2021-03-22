#ServiceLoader.py
from API import *

from EchoService import *
# from DanilatorService import *
# from ReminderService import *
# from MusicService import *
from MasterService import *
from ExperimentalService import *
# from SupertoolsService import *
# from InnovationService import *
# from ScraperService import *
# from PistonService import *
# from StockService import *
from Challenge18Service import *
# from TofaatTevaService import *
# from ClearVisionService import *

from threading import Thread

# masterServices = ["Master","Experimental","TofaatTeva"]
masterServices = ["Master",]

class ServiceLoader(object):
    def LoadServices(send, backup, genLink, list = ["Master", "Challenge18"], master = None):
    # def LoadServices(send, backup, genLink, list = ["Master", "Echo", "Experimental"], master = None):
    # def LoadServices(send, backup, genLink, list = ["Master"], master = None):
        services = {}
        for service in list:
            if service in masterServices :
                services[service] = ServiceLoader.LoadService(service, send, backup, genLink, master = master)
            else:
                services[service] = ServiceLoader.LoadService(service, send, backup, genLink)
        return services

    def LoadService(service, send, backup, genLink, master = None):
        # Load Dynamicly
        # api = API(service, send, backup, genLink)
        foundServiceClass = None
        # if service is "Echo":
        #     foundServiceClass = EchoService
        if service is "Master":
            foundServiceClass = MasterService
        # if service is "Experimental":
        #     foundServiceClass = ExperimentalService
        if service is "Challenge18":
            foundServiceClass = Challenge18Service

        if foundServiceClass is not None:
            api = API(service, send, backup, genLink)
            ServiceLoader.startService(foundServiceClass, db={}, api=api, master = master)
            return {"obj": foundServiceClass.share, "api":api}


        return None

    def startService(service_class, db = None, api = None, master = None):
        serviceThread = Thread(target = ServiceLoader.startServiceAsync, args = [[service_class, db, api, master]])
        serviceThread.start()

    def startServiceAsync(data):
        service_class, db, api, master = data
        if master is None:
            x = service_class(db, api)
            x.go()
        else:
            x = service_class(db,api,master)
            x.go()
