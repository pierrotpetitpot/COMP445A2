#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021
#
# Distributed under terms of the MIT license.

"""
Description:

"""
import asyncio
import logging
import sys
from pip._vendor.distlib.compat import raw_input
import patterns
import view
from client import *

logging.basicConfig(filename='view.log', level=logging.DEBUG)
logger = logging.getLogger()


class IRCClient(patterns.Subscriber):
    HEADER = 64
    PORT = 5050
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    SERVER = "192.168.1.26"
    ADDR = (SERVER, PORT)

    def __init__(self, nickname):
        super().__init__()
        self.username = nickname
        self._run = True

    def set_view(self, view):
        self.view = view

    def update(self, msg):
        # Will need to modify this
        if not isinstance(msg, str):
            raise TypeError(f"Update argument needs to be a string")
        elif not len(msg):
            # Empty string
            return
        logger.info(f"IRCClient.update -> msg: {msg}")
        self.process_input(msg)

    def process_input(self, msg):
        # Will need to modify this
        self.add_msg(msg)
        if msg.lower().startswith('/quit'):
            # Command that leads to the closure of the process
            raise KeyboardInterrupt

    def add_msg(self, msg):
        self.view.add_msg(self.username, msg)

    async def run(self):
        """
        Driver of your IRC Client
        """
        # Remove this section in your code, simply for illustration purposes
        for x in range(10):
            self.add_msg(f"call after View.loop: {x}")
            await asyncio.sleep(2)

    def close(self):
        # Terminate connection
        logger.debug(f"Closing IRC Client object")
        pass


def main(args):
    # Pass your arguments where necessary
    client = IRCClient(args[0])

    logger.info(f"Client object created")
    with view.View() as v:
        logger.info(f"Entered the context of a View object")
        client.set_view(v)
        logger.debug(f"Passed View object to IRC Client")
        v.add_subscriber(client)
        logger.debug(f"IRC Client is subscribed to the View (to receive user input)")

        async def inner_run():
            await asyncio.gather(
                v.run(),
                client.run(),
                return_exceptions=True,
            )

        try:
            asyncio.run(inner_run())
        except KeyboardInterrupt as e:
            logger.debug(f"Signifies end of process")
    client.close()


def parsingNickname(nickCommand):
    aList = nickCommand.split()
    if aList[0] == "NICK":
        return aList[1]
    else:
        print("ERROR: INVALID COMMAND")
        sys.exit()


def parsingUser():
    pass


if __name__ == "__main__":
    args = []

    print("HELLO WELCOME.\n")
    nickCommand = raw_input("PLEASE INPUT YOUR NICK COMMAND  format: NICK <nickname>\n")
    stringNick = nickCommand
    send(stringNick)  # let server verify if nickname already exists. If it already exists the code breaks in server.py

    nickName = parsingNickname(stringNick)  # we parse and only take the nickname
    args.append(nickName)

    # not sure what to put in for the user command aside  from the port..
    # user = raw_input("PLEASE INPUT YOUR USER COMMAND format: USER <username> <hostname> <servername> <realname>\n")

    main(args)
