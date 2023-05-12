"""
### FIXRobot FIX50 pytest failure testcases
"""
__author__ = "Anand P. Subramanian (quickfixrobot@gmail.com)"
__date__ = "23 July 2016 - Till Date"
__copyright__ = "FIXRobot  Copyright (C) 2023  Anand P. Subramanian."
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
from FIXRobot.FIXRobot.FIXRobotClass import *

#FIXRobot testcase extending unittest.TestCase class
@pytest.mark.usefixtures("setUpFIX50ClientAndExchange")
class Test_Class:
    #Negative testcase for OrderList where fix message arguments are passed as template names.
    @pytest.mark.fix50failure
    @pytest.mark.xfail
    def test_OrderList_ShouldFail(self, setUpFIX50ClientAndExchange):
        clientAndExchange = setUpFIX50ClientAndExchange
        self.exch = clientAndExchange[0]
        self.client = clientAndExchange[1]

        returnValue = self.exch.clearMessageStore()
        assert returnValue == True
        time.sleep(1)

        returnValue = self.client.clearMessageStore()
        assert returnValue == True
        time.sleep(1)

        returnMessageInitiator = self.client.sendMessage("NewOrderListNewPass")
        if returnMessageInitiator:
            assert returnMessageInitiator.getHeader().getField(35) == "E"
        time.sleep(1)

        returnMessageAcceptor = self.exch.receiveMessage("NewOrderListNewFail")
        if returnMessageAcceptor:
            assert returnMessageAcceptor.getHeader().getField(35) == "E"
        time.sleep(1)

    #Negative testcase for OrderList reverse flow where fix message arguments are passed as template names.
    @pytest.mark.fix50failure
    @pytest.mark.xfail
    def test_OrderListReverse_ShouldFail(self, setUpFIX50ClientAndExchange):
        clientAndExchange = setUpFIX50ClientAndExchange
        self.exch = clientAndExchange[0]
        self.client = clientAndExchange[1]

        returnValue = self.exch.clearMessageStore()
        assert returnValue == True
        time.sleep(1)

        returnValue = self.client.clearMessageStore()
        assert returnValue == True
        time.sleep(1)

        returnValue = self.exch.sendMessage("NewOrderListNewPass")
        assert returnValue != None
        time.sleep(1)

        returnValue = self.client.receiveMessage("NewOrderListNewFail")
        assert returnValue != None
        time.sleep(1)

    #Negative testcase for NewOrderSingle and Fill where fix message arguments are passed as template names.
    @pytest.mark.fix50failure
    @pytest.mark.xfail
    def test_NewOrderSingleFilled_ShouldFail(self, setUpFIX50ClientAndExchange):
        clientAndExchange = setUpFIX50ClientAndExchange
        self.exch = clientAndExchange[0]
        self.client = clientAndExchange[1]

        returnValue = self.exch.clearMessageStore()
        assert returnValue == True
        time.sleep(1)

        returnValue = self.client.clearMessageStore()
        assert returnValue == True
        time.sleep(1)

        returnMessageInitiator = self.client.sendMessage("NewOrderSinglePass")
        if returnMessageInitiator:
            assert returnMessageInitiator.getHeader().getField(35) == "D"
        time.sleep(1)

        returnMessageAcceptor = self.exch.receiveMessage("NewOrderSingleFail")
        if returnMessageAcceptor:
            assert returnMessageAcceptor.getHeader().getField(35) == "D"
        time.sleep(1)

        returnMessageAcceptor = self.exch.sendMessage("ExecutionReportPass")
        if returnMessageAcceptor:
            assert returnMessageAcceptor.getHeader().getField(35) == "8"
        time.sleep(1)

        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportFail")
        if returnMessageInitiator:
            assert returnMessageInitiator.getHeader().getField(35) == "8"
        time.sleep(1)

        returnValue = self.exch.logDumpMessageStore()
        assert returnValue == True
        time.sleep(1)

    #Negative testcase for OrderList where fix message arguments are passed as template names.
    @pytest.mark.fix50failure
    @pytest.mark.xfail
    def test_OrderListStringFail(self, setUpFIX50ClientAndExchange):
        clientAndExchange = setUpFIX50ClientAndExchange
        self.exch = clientAndExchange[0]
        self.client = clientAndExchange[1]
        returnValue = self.exch.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnValue = self.client.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnMessageInitiator = self.client.sendMessage("NewOrderListNew")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "E")
        time.sleep(1)
        returnMessageAcceptor = self.exch.receiveMessage("NewOrderListNewErr")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "E")
        time.sleep(1)
        returnValue = self.exch.logDumpMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
