"""
### fixrobot conftest.py for pytest test fixtures
"""
__author__ = "Anand P. Subramanian (quickfixrobot@gmail.com)"
__date__ = "23 July 2016 - Till Date"
__copyright__ = "fixrobot  Copyright (C) 2023  Anand P. Subramanian."
__license__ = "1.1"
__version__ = "License: GGPLv3+ GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>."
__credits__ = "Anand P. Subramanian"
__URL__ = "https://github.com/quickfixrobot/FIXRobot/"
import sys
import os
import time
import quickfix as fix

import pytest

sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), os.pardir))
from fixrobot.fixrobot.fixrobot import *

@pytest.fixture(scope="class")
def setUpFIX50ClientAndExchange():
    os.environ["FIXROBOTPATH"] = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(os.environ["FIXROBOTPATH"])
    exch_conn_name = "EXCHANGEFIX50"
    exch_connection = fixrobot()
    time.sleep(1)
    exch_connection.startAcceptor(exch_conn_name)
    time.sleep(1)

    exchTearDownCount = 1
    time.sleep(1)

    os.environ["FIXROBOTPATH"] = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(os.environ["FIXROBOTPATH"])
    client_conn_name = "CLIENTFIX50"
    print(sys.path)
    client_connection = fixrobot()
    time.sleep(1)
    client_connection.startInitiator(client_conn_name)
    time.sleep(1)
    clientTearDownCount = 1
    exchAndClient = (exch_connection, client_connection)
    yield exchAndClient

    returnValue = client_connection.clearMessageStore()
    returnValue = exch_connection.clearMessageStore()

    time.sleep(1)
    #After the client connection is used in the end closing the connection
    client_connection.stopInitiator()
    time.sleep(1)
    client_connection.receiveMessage("LogoutPass")
    time.sleep(1)
    clientTearDownCount = clientTearDownCount - 1

    #After the exchange connection is used in the end closing the connection
    time.sleep(1)
    exch_connection.stopAcceptor()
    time.sleep(1)
    exch_connection.receiveMessage("LogoutPass")
    time.sleep(1)
    exchTearDownCount = exchTearDownCount - 1

@pytest.fixture(scope="class")
def setUpFIX42ClientAndExchange():
    os.environ["FIXROBOTPATH"] = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(os.environ["FIXROBOTPATH"])
    exch_conn_name = "EXCHANGEFIX42"
    exch_connection = fixrobot()
    time.sleep(1)
    exch_connection.startAcceptor(exch_conn_name)
    time.sleep(1)

    exchTearDownCount = 1
    time.sleep(1)

    os.environ["FIXROBOTPATH"] = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(os.environ["FIXROBOTPATH"])
    client_conn_name = "CLIENTFIX42"
    print(sys.path)
    client_connection = fixrobot()
    time.sleep(1)
    client_connection.startInitiator(client_conn_name)
    time.sleep(1)
    clientTearDownCount = 1
    exchAndClient = (exch_connection, client_connection)
    yield exchAndClient

    returnValue = client_connection.clearMessageStore()
    returnValue = exch_connection.clearMessageStore()

    time.sleep(1)
    #After the client connection is used in the end closing the connection
    client_connection.stopInitiator()
    time.sleep(1)
    client_connection.receiveMessage("LogoutPass")
    time.sleep(1)
    clientTearDownCount = clientTearDownCount - 1

    #After the exchange connection is used in the end closing the connection
    time.sleep(1)
    exch_connection.stopAcceptor()
    time.sleep(1)
    exch_connection.receiveMessage("LogoutPass")
    time.sleep(1)
    exchTearDownCount = exchTearDownCount - 1