import json, sys, os
from twisted.web import server
from twisted.web.wsgi import WSGIResource
from twisted.python.threadpool import ThreadPool
from twisted.internet import reactor
from twisted.application import service, strports

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app import create_app

wsgiThreadPoll = ThreadPool()
wsgiThreadPoll.start()

reactor.addSystemEventTrigger('after', 'shutdown', wsgiThreadPoll.stop)

application = create_app()

wsgiAppResource = WSGIResource(reactor, wsgiThreadPoll, application)

application = service.Application("file server")
server = strports.service('tcp:9091', server.Site(wsgiAppResource))
server.setServiceParent(application)
