"""
FIXRobot FIX50 negative testcases
"""
__author__ = "Anand P. Subramanian (quickfixrobot@gmail.com)"
__date__ = "23 July 2016 - Till Date"
__copyright__ = "FIXRobot  Copyright (C) 2016  Anand P. Subramanian."
__license__ = "1.0"
__version__ = "License: GGPLv3+ GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>."
__credits__ = "Anand P. Subramanian"
__URL__ = "https://github.com/quickfixrobot/FIXRobot/"
import sys
import os
import time
import quickfix as fix
import unittest
sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), os.pardir))
from FIXRobot import *


class FIXRobotUnitTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ["FIXROBOTPATH"] = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        print os.environ["FIXROBOTPATH"]
        exch_conn_name = "EXCHANGEFIX50"
        client_conn_name = "CLIENTFIX50"
        cls.exch = FIXRobot()
        cls.client = FIXRobot()
        cls.exch.startAcceptor(exch_conn_name)
        time.sleep(1)
        cls.client.startInitiator(client_conn_name)
        time.sleep(1)
        cls.exch.receiveMessage("LogonPass")
        time.sleep(1)
        cls.client.receiveMessage("LogonPass")
        time.sleep(1)
        cls.tearDownCount = 1

    @classmethod
    def tearDownClass(cls):
        returnValue = cls.exch.clearMessageStore()
        returnValue = cls.client.clearMessageStore()
        cls.client.stopInitiator()
        time.sleep(1)
        cls.exch.stopAcceptor()
        time.sleep(1)
        cls.exch.receiveMessage("LogoutPass")
        time.sleep(1)
        cls.client.receiveMessage("LogoutPass")
        time.sleep(1)
        cls.tearDownCount = cls.tearDownCount + 1

    @unittest.expectedFailure
    def test_OrderList_ShouldFail(self):
        returnValue = self.exch.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnValue = self.client.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnMessageInitiator = self.client.sendMessage("NewOrderListNewPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "E")
        time.sleep(1)
        returnMessageAcceptor = self.exch.receiveMessage("NewOrderListNewFail")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "E")
        time.sleep(1)

    @unittest.expectedFailure
    def test_OrderListReverse_ShouldFail(self):
        returnValue = self.exch.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnValue = self.client.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnValue = self.exch.sendMessage("NewOrderListNewPass")
        self.assertNotEqual(returnValue, None)
        time.sleep(1)
        returnValue = self.client.receiveMessage("NewOrderListNewFail")
        self.assertNotEqual(returnValue, None)
        time.sleep(1)

    @unittest.expectedFailure
    def test_NewOrderSingleFilled_ShouldFail(self):
        returnValue = self.exch.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnValue = self.client.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)

        returnMessageInitiator = self.client.sendMessage("NewOrderSinglePass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "D")
        time.sleep(1)
        returnMessageAcceptor = self.exch.receiveMessage("NewOrderSingleFail")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "D")
        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage("ExecutionReportPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportFail")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)
        returnValue = self.exch.logDumpMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)

    @unittest.expectedFailure
    def test_OrderListStringFail(self):
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

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FIXRobotUnitTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
