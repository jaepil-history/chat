#!/usr/bin/env python
#
# Copyright (c) 2013-2014 Appspand, Inc.

import sys

import mongoengine

from tornado import httpserver
from tornado import ioloop
from tornado import options
from tornado import web

from config.loader import load_appcfg
from common import cache
import interop.service
from log import logger


class Application(web.Application):
    pass


def build_url_handlers():
    from net.http import urls as http_urls
    from net.websocket import urls as ws_urls

    handlers = http_urls.handlers + ws_urls.handlers

    return handlers


def init_database(config):
    database = config.database

    redis = database.redis
    if redis.enabled:
        cache.init(host=redis.host, port=redis.port,
                   password=redis.password, pool_size=redis.connection_pool,
                   socket_timeout=redis.timeout, db=redis.db)

        redis = cache.get_connection()
        redis.ping()

    mongodb = database.mongodb
    mongoengine.connect(db="chat",
                        host=mongodb.connection_uri,
                        max_pool_size=mongodb.connection_pool,
                        socketTimeoutMS=mongodb.timeout)
    logger.access.debug("mongodb connection url: %s" % mongodb.connection_uri)


def init_server(config, port):
    url_handlers = build_url_handlers()
    application = Application(
        handlers=url_handlers,
        debug=config.debug,
        config=config
    )
    for host_name in config.server.hosts:
        application.add_handlers(host_name.host, url_handlers)

    http_server = httpserver.HTTPServer(application)
    http_server.listen(port)


def init_service(config):
    if config.interop:
        interop.service.start()

    # if config.application.stage == "local":
    #     return

    # import newrelic.agent
    # newrelic.agent.initialize("../conf/newrelic.ini",
    #                           config.application.stage)
    # newrelic.agent.register_application()


def run_server(config):
    ioloop.IOLoop.instance().start()


def main():
    if len(sys.argv) < 2:
        print "main.py [config] [task id]"
        return False

    options.parse_command_line()
    config = load_appcfg(sys.argv[1])
    task_id = 0
    if len(sys.argv) > 2:
        task_id = int(sys.argv[2])

    listen_port = config.server.base_port + task_id

    logger.init(config=config, task_id=task_id)
    logger.general.debug("Configuration dump: %s" % config.to_json())

    init_database(config=config)

    init_server(config=config, port=listen_port)
    init_service(config=config)

    logger.general.debug("Chat server is started...")
    logger.general.debug("Task ID: %d" % task_id)
    logger.general.debug("HTTP listen port: %d" % listen_port)

    run_server(config=config)

    return 0


if __name__ == "__main__":
    main()
