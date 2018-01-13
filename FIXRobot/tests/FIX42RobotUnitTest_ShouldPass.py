"""
### FIXRobot FIX42 positive testcases
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
sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), os.pardir))
from FIXRobot import *

import unittest

#FIXRobot testcase extending unittest.TestCase class
class FIXRobotUnitTest(unittest.TestCase):

    #Testcase setup class method only called once in the beginning.
    @classmethod
    def setUpClass(cls):
        os.environ["FIXROBOTPATH"] = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        print os.environ["FIXROBOTPATH"]
        exch_conn_name = "EXCHANGEFIX42"
        client_conn_name = "CLIENTFIX42"
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

    #Testcase teardown class method only called once in the end.
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

    #Positive testcase for NewOrderSingle and Fill where fix message arguments are passed as strings.
    def test_NewOrderSingleFilled_AsStrings_ShouldPass(self):
        returnValue = self.exch.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnValue = self.client.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnMessageInitiator = self.client.sendMessage(
            "NewOrderSingle", "|35=D|$setField( ClOrdID )|21=1|55=MSFT|54=1|$setField( SendingTime )|$setField(TransactTime)|40=2|38=100|44=10.50|59=0|")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "D")
        time.sleep(1)
        returnMessageAcceptor = self.exch.receiveMessage(
            "NewOrderSingle", "|35=D|$setField( ClOrdID )|21=1|55=MSFT|54=1|$setField( SendingTime )|$setField(TransactTime)|40=2|38=100|44=10.50|59=0|")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "D")
        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage(
            "ExecutionReport", "|35=8|$setField( ClOrdID,  IN, ClOrdID )|$setField( OrderID )|$setField( ExecID )|20=0|150=0|39=0|55=MSFT|38=100|54=1|44=10.50|151=100|14=0|6=0.0|")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReport", "|35=8|$setField( ClOrdID,  IN, ClOrdID )|$setField( OrderID )|$setField( ExecID )|20=0|150=0|39=0|55=MSFT|38=100|54=1|44=10.50|151=100|14=0|6=0.0|")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage(
            "ExecutionReport", "|35=8|$setField( ClOrdID,  IN, ClOrdID )|$setField( OrderID )|$setField( ExecID )|20=0|150=2|39=2|55=MSFT|38=100|54=1|44=10.50|32=100|31=10.50|151=0|14=100|6=10.50|")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReport", "|35=8|$setField( ClOrdID,  IN, ClOrdID )|$setField( OrderID )|$setField( ExecID )|20=0|150=2|39=2|55=MSFT|38=100|54=1|44=10.50|32=100|31=10.50|151=0|14=100|6=10.50|")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)

    #Positive testcase for NewOrderSingle and Filled where fix message arguments are passed as template names.
    def test_NewOrderSingleFilled_AsNames_ShouldPass(self):
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
        returnMessageAcceptor = self.exch.receiveMessage("NewOrderSinglePass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "D")
        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage("ExecutionReportAckPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportAckPass")
        if returnMessageInitiator:

            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage(
            "ExecutionReportFillPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportFillPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)
        returnValue = self.exch.logDumpMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)

    #Positive testcase for NewOrderSingle and CancelRequest where fix message arguments are passed as template names.
    def test_NewOrderSingleOrderCancelRequest_AsNames_ShouldPass(self):
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
        returnMessageAcceptor = self.exch.receiveMessage("NewOrderSinglePass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "D")
        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage("ExecutionReportAckPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportAckPass")
        if returnMessageInitiator:
            self.assertEqual(

                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.sendMessage(
            "OrderCancelRequestPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "F")
        time.sleep(1)
        returnMessageAcceptor = self.exch.receiveMessage(
            "OrderCancelRequestPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "F")
        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage(
            "ExecutionReportCancelledPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportCancelledPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")

        time.sleep(1)

    #Positive testcase for NewOrderSingle and CancelReplaceRequest where fix message arguments are passed as template names.
    def test_NewOrderSingleOrderCancelReplaceRequest_AsNames_ShouldPass(self):
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
        returnMessageAcceptor = self.exch.receiveMessage("NewOrderSinglePass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "D")

        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage("ExecutionReportAckPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportAckPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.sendMessage(
            "OrderCancelReplaceRequestPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "G")
        time.sleep(1)
        returnMessageAcceptor = self.exch.receiveMessage(
            "OrderCancelReplaceRequestPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "G")
        time.sleep(1)

        returnMessageAcceptor = self.exch.sendMessage(
            "ExecutionReportReplacedPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportReplacedPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)

    #Positive testcase for TestRequest and Heartbeat where fix message arguments are passed as template names.
    def test_TestRequestHeartBeat_AsNames_ShouldPass(self):
        returnValue = self.exch.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnValue = self.client.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnMessageInitiator = self.client.sendMessage("TestRequestPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "1")

        time.sleep(1)
        returnValue = self.exch.logDumpMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnMessageAcceptor = self.exch.receiveMessage("TestRequestPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "1")
        time.sleep(1)
        returnValue = self.exch.logDumpMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage("HeartbeatPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "0")
        time.sleep(1)

    #Positive testcase for OrderList and Fill where fix message arguments are passed as template names.
    def test_OrderListAckFill_AsNames_ShouldPass(self):
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
        returnMessageAcceptor = self.exch.receiveMessage("NewOrderListNewPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "E")
        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage(
            "ExecutionReportListFill1Pass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportListFill1Pass")

        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage(
            "ExecutionReportListFill2Pass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportListFill2Pass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage(
            "ExecutionReportListFill3Pass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)

        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportListFill3Pass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage(
            "ExecutionReportListFill4Pass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportListFill4Pass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)

    #Positive testcase for OrderList and Fill reverse flow where fix message arguments are passed as template names.
    def test_OrderListAckFillReverse_AsNames_ShouldPass(self):
        returnValue = self.exch.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnValue = self.client.clearMessageStore()

        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage("NewOrderListNewPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "E")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage(
            "NewOrderListNewPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "E")
        time.sleep(1)
        returnMessageInitiator = self.client.sendMessage(
            "ExecutionReportListFill1Pass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageAcceptor = self.exch.receiveMessage(
            "ExecutionReportListFill1Pass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)

        returnMessageInitiator = self.client.sendMessage(
            "ExecutionReportListFill2Pass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageAcceptor = self.exch.receiveMessage(
            "ExecutionReportListFill2Pass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageInitiator = self.client.sendMessage(
            "ExecutionReportListFill3Pass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageAcceptor = self.exch.receiveMessage(
            "ExecutionReportListFill3Pass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")

        time.sleep(1)
        returnMessageInitiator = self.client.sendMessage(
            "ExecutionReportListFill4Pass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)
        returnMessageAcceptor = self.exch.receiveMessage(
            "ExecutionReportListFill4Pass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)

    #Positive testcase for TestRequest and Heartbeat in reverse flow where fix message arguments are passed as template names.
    def test_TestRequestHeartBeatReverse_AsNames_ShouldPass(self):
        returnValue = self.exch.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnValue = self.client.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnMessageAcceptor = self.exch.sendMessage("TestRequestPass")

        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "1")
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage("TestRequestPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "1")
        time.sleep(1)
        returnMessageAcceptor = self.exch.receiveMessage("HeartbeatPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "0")
        time.sleep(1)

    #Positive testcase for get sender and target message sequence number.
    def test_getSenderAndTargetMsgSeqNum_ShouldPass(self):
        senderValue = self.client.getExpectedSenderNum()
        targetValue = self.client.getExpectedTargetNum()
        self.assertEqual(type(senderValue), type(targetValue))

    #Positive testcase for ResendRequest where fix message arguments are passed as template names.
    def test_ResendRequest_AsNames_ShouldPass(self):
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

        returnMessageAcceptor = self.exch.receiveMessage("NewOrderSinglePass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "D")
        time.sleep(1)

        returnMessageAcceptor = self.exch.sendMessage("ExecutionReportAckPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)

        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportAckPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)

        returnMessageAcceptor = self.exch.sendMessage(
            "ExecutionReportFillPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "8")
        time.sleep(1)

        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportFillPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)

        returnValue = self.exch.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnValue = self.client.clearMessageStore()
        self.assertEqual(returnValue, True)
        time.sleep(1)
        senderValue = self.client.getExpectedSenderNum()
        targetValue = self.client.getExpectedTargetNum()
        returnValue = self.client.setNextTargetMsgSeqNum(targetValue - 2)
        self.assertEqual(returnValue, True)

        time.sleep(1)
        returnMessageInitiator = self.client.sendMessage("TestRequestPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "1")
        time.sleep(1)
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnMessageInitiator = self.client.receiveMessage("HeartbeatPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "0")
        time.sleep(1)
        self.assertEqual(returnValue, True)
        time.sleep(1)
        returnMessageAcceptor = self.exch.receiveMessage("ResendRequestPass")
        if returnMessageAcceptor:
            self.assertEqual(
                returnMessageAcceptor.getHeader().getField(35), "2")
        time.sleep(1)
        returnValue = self.client.logDumpMessageStore()

        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportAckResentPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")

        returnMessageInitiator = self.client.receiveMessage(
            "ExecutionReportFillResentPass")
        if returnMessageInitiator:
            self.assertEqual(
                returnMessageInitiator.getHeader().getField(35), "8")
        time.sleep(1)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FIXRobotUnitTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
