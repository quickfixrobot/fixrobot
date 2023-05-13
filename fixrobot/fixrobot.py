"""
fixrobot is software to write testcases and test FIXEngine using FIX Protocol.
fixrobot can act as intitiator/client and acceptor/exchange.
fixrobot can send and receive FIX messages and will compare the actual messages with the expected messages.
The testcase can be run as python unittests or pytest plugins
"""
__author__ = "Anand P. Subramanian (quickfixrobot@gmail.com)"
__date__ = "23 July 2016 - Till Date"
__copyright__ = "fixrobot  Copyright (C) 2016  Anand P. Subramanian."
__license__ = "1.0"
__version__ = "License: GGPLv3+ GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>."
__credits__ = "Anand P. Subramanian"
__URL__ = "https://github.com/quickfixrobot/FIXRobot/"

# from __future__ import
# absolute_import,division,print_function,unicode_literals
import sys
import os
import string
import time
import configparser
from datetime import datetime
import copy
import logging
from collections import deque
import quickfix as fix
import quickfixt11 as fixt11
import quickfix40 as fix40
import quickfix41 as fix41
import quickfix42 as fix42
import quickfix43 as fix43
import quickfix44 as fix44
import quickfix50 as fix50
import quickfix50sp1 as fix50sp1
import quickfix50sp2 as fix50sp2

logFormat = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
logging.basicConfig(filename="fixrobot.log",
                    format=logFormat, level=logging.DEBUG)
messageIdDict = dict()


def getId(inputStr):
    try:
        if hasattr(fix, inputStr):
            dateAndTime = str(
                (datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f"))[:-3])
            if inputStr in ["SendingTime", "OrigSendingTime", "OnBehalfOfSendingTime", "TransactTime"]:
                return dateAndTime
            if inputStr in messageIdDict.keys():
                messageIdDict[inputStr] = messageIdDict[inputStr] + 1
                return inputStr.upper() + "_" + str(messageIdDict[inputStr]) + "_" + dateAndTime
            else:
                messageIdDict[inputStr] = 1
                return inputStr.upper() + "_" + str(messageIdDict[inputStr]) + "_" + dateAndTime
        else:
            raise Exception
    except Exception as e:
        logging.debug("Exception!!!:%s, %s", e.args, sys.exc_info()[0])
        raise Exception


class FIXMessageEvaluator():
    def evalMsgType(self,  msgTypeString):
        try: 
            fullMsgTypeString = "fix.MsgType_" + msgTypeString
            return eval(fullMsgTypeString)
        except Exception as e:
            logging.debug("Exception!!!:%s, %s", e.args, sys.exc_info()[0])
            raise Exception

class FIXRobotProcessor(fix.Application):
    '''
        FIXRobotProcessor
    '''
    orderID = 0
    execID = 0
    incomingFIXRobotMessage = None
    sessID = None

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
     
    def onCreate(self, sessionID):
        '''
            This is a callback function from quickfix library which is called in the event of creation of a new fix connection.

                Args:
                    sessionID(SessionId): FIX connection session object.
                Returns:
                    None.
                Raises:
                    None.
        '''
        self.incomingFIXRobotAdminMessage = None
        self.incomingFIXRobotAppMessage = None
        self.outgoingFIXRobotAdminMessage = None
        self.outgoingFIXRobotAppMessage = None
        self.incomingFIXRobotAdminMessageDeque = deque()
        self.incomingFIXRobotAppMessageDeque = deque()
        self.outgoingFIXRobotAdminMessageDeque = deque()
        self.outgoingFIXRobotAppMessageDeque = deque()
        self.sessID = sessionID
        self.clOrdID = 0
        self.orderID = 0
        self.execID = 0
        self.testReqID = 0
        self.defaultMessageConfig = configparser.ConfigParser()
        self.defaultMessageConfig.read(os.path.join(
            os.environ["FIXROBOTPATH"], "env", "DEFAULTMESSAGES.ini"))
        return

    def onLogon(self, sessionID):
        '''
            This is a callback function from quickfix library which is called in the event of logon by the fix connection.

                Args:
                    sessionID(SessionId): FIX connection session object.
                Returns:
                    None.
                Raises:
                    None.
        '''     
        logging.debug("Successful Logon to session:%s", sessionID.toString())
        return

    def onLogout(self, sessionID):
        '''
            This is a callback function from quickfix library which is called in the event of logout by the fix connection.

                Args:
                    sessionID(SessionId): FIX connection session object.
                Returns:
                    None.
                Raises:
                    None.
        ''' 
        logging.debug("Successful Logout to session:%s", sessionID.toString())
        return

    def toAdmin(self, message, sessionID):
        '''
            This is a callback function from quickfix library which is called when an admin message is received.

                Args:
                    message(Message): Received admin FIX message object.
                    sessionID(SessionId): FIX connection session object.
                Returns:
                    None.
                Raises:
                    None.
        ''' 
        #self.outgoingFIXRobotAdminMessageDeque = deque() 
        if 'self.outgoingFIXRobotAdminMessageDeque' not in locals() or 'self.outgoingFIXRobotAdminMessageDeque' not in globals():
            self.outgoingFIXRobotAdminMessageDeque = deque()
        if len(self.outgoingFIXRobotAdminMessageDeque) > 0:
            self.outgoingFIXRobotAdminMessageDeque.clear()
        self.outgoingFIXRobotAdminMessage = fix.Message(message)
        self.outgoingFIXRobotAdminMessageDeque.append(
            self.outgoingFIXRobotAdminMessage)
        logging.debug("%s sent the following admin message: %s",
                      sessionID.toString(), self.outgoingFIXRobotAdminMessage.toString())

    def fromAdmin(self, message, sessionID):
        '''
            This is a callback function from quickfix library which is called when an admin message is sent.

                Args:
                    message(Message): Sent admin FIX message object.
                    sessionID(SessionId): FIX connection session object.
                Returns:
                    None.
                Raises:
                    None.
        ''' 
        #self.incomingFIXRobotAdminMessageDeque = deque()
        if 'self.incomingFIXRobotAdminMessageDeque' not in locals() or 'self.incomingFIXRobotAdminMessageDeque' not in globals():
            self.incomingFIXRobotAdminMessageDeque = deque()
        self.incomingFIXRobotAdminMessage = fix.Message(message)
        if len(self.incomingFIXRobotAdminMessageDeque) > 0:
            if(self.incomingFIXRobotAdminMessage.getHeader().isSetField(43)):
                if(self.incomingFIXRobotAdminMessage.getHeader().getField(43) != "Y"):
                    self.incomingFIXRobotAdminMessageDeque.clear()
            else:
                self.incomingFIXRobotAdminMessageDeque.clear()
        self.incomingFIXRobotAdminMessageDeque.append(
            self.incomingFIXRobotAdminMessage)
        logging.debug("%s received the following admin message: %s",
                      sessionID.toString(), self.incomingFIXRobotAdminMessage.toString())

    def toApp(self, message, sessionID):
        '''
            This is a callback function from quickfix library which is called when an application message is received.

                Args:
                    message(Message): Received application FIX message object.
                    sessionID(SessionId): FIX connection session object.
                Returns:
                    None.
                Raises:
                    None.
        ''' 
        #self.outgoingFIXRobotAppMessageDeque = deque()
        if len(self.outgoingFIXRobotAppMessageDeque) > 0:
            self.outgoingFIXRobotAppMessageDeque.clear()
        self.outgoingFIXRobotAppMessage = fix.Message(message)
        self.outgoingFIXRobotAppMessageDeque.append(
            self.outgoingFIXRobotAppMessage)
        logging.debug("%s sent the following app message: %s",
                      sessionID.toString(), self.outgoingFIXRobotAppMessage.toString())

    def fromApp(self, message, sessionID):
        '''
            This is a callback function from quickfix library which is called when an application message is sent.

                Args:
                    message(Message): Received application FIX message object.
                    sessionID(SessionId): FIX connection session object.
                Returns:
                    None.
                Raises:
                    None.
        '''
        #self.incomingFIXRobotAppMessageDeque = deque()
        self.incomingFIXRobotAppMessage = fix.Message(message)
        if len(self.incomingFIXRobotAppMessageDeque) > 0:
            if(self.incomingFIXRobotAppMessage.getHeader().isSetField(43)):
                if(self.incomingFIXRobotAppMessage.getHeader().getField(43) != "Y"):
                    self.incomingFIXRobotAppMessageDeque.clear()
            else:
                self.incomingFIXRobotAppMessageDeque.clear()
        self.incomingFIXRobotAppMessageDeque.append(
            self.incomingFIXRobotAppMessage)
        logging.debug("%s received the following app message: %s",
                      sessionID.toString(), self.incomingFIXRobotAppMessage.toString())

    def getExpectedSenderNum(self):
        '''
            This function is used to get the next out sequence number.

                Args:
                    None.
                Returns:
                    None.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        # self.session.setNextSenderMsgSeqNum(n)
        # self.session.getExpectedSenderNum()
        try:
            self.session = fix.Session.lookupSession(self.sessID)
            senderSeqNo = self.session.getExpectedSenderNum()
            logging.debug("Next sender msg sequence num: %s", str(senderSeqNo))
            return senderSeqNo
        except Exception as e:
            logging.debug("Failed getting sender msg sequence num by %s, %s, %s!!!",
                          self.sessID.toString(), e.args, sys.exc_info()[0])
            raise Exception

    def setNextSenderMsgSeqNum(self, senderSeqNo):
        '''
            This function is used to set the next out sequence number.

                Args:
                    senderSeqNo(int): Out sequence number to set.
                Returns:
                    None.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        # self.session.setNextSenderMsgSeqNum(n)
        # self.session.getExpectedSenderNum()
        try:
            self.session = fix.Session.lookupSession(self.sessID)
            self.session.setNextSenderMsgSeqNum(senderSeqNo)
            logging.debug(
                "Next sender msg sequence num set to: %s", str(senderSeqNo))
        except Exception as e:
            logging.debug("Failed setting sender msg sequence num by %s, %s, %s!!!",
                          self.sessID.toString(), e.args, sys.exc_info()[0])
            raise Exception

    def getExpectedTargetNum(self):
        '''
            This function is used to get the next in sequence number.

                Args:
                    None.
                Returns:
                    None.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        # self.session.setNextTargetMsgSeqNum(n)
        # self.session.getExpectedTargetNum()
        try:
            self.session = fix.Session.lookupSession(self.sessID)
            targetSeqNo = self.session.getExpectedTargetNum()
            logging.debug("Next target msg sequence num: %s", str(targetSeqNo))
            return targetSeqNo
        except Exception as e:
            logging.debug("Failed getting target message sequence num by %s, %s, %s!!!",
                          self.sessID.toString(), e.args, sys.exc_info()[0])
            raise Exception

    def setNextTargetMsgSeqNum(self, targetSeqNo):
        '''
            This function is used to set the next expected in sequence number.

                Args:
                    targetSeqNo(int): In sequence number to set.
                Returns:
                    None.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        # self.session.setNextTargetMsgSeqNum(n)
        # self.session.getExpectedSenderNum()
        try:
            self.session = fix.Session.lookupSession(self.sessID)
            self.session.setNextTargetMsgSeqNum(targetSeqNo)
            logging.debug(
                "Next target msg sequence num set to: %s", str(targetSeqNo))
        except Exception as e:
            logging.debug("Failed setting target msg sequence num by %s, %s, %s!!!",
                          self.sessID.toString(), e.args, sys.exc_info()[0])
            raise Exception

    def presetFIXRobotMessage(self, presetMessage):
        '''
            This function is used to set a preset message and can be used for a any future purpose.

                Args:
                    presetMessage(str): Preset a message string.
                Returns:
                    None.
                Raises:
                    None.
        '''
        self.presetMessage = presetMessage
        return
    def logDumpMessageStore(self):
        '''
            This function is used to dump a copy of messages into the logs.

            Args:
                None.
            Returns:
                None.
            Raises:
                Exception: Raises exception when error occours.
        '''
        try:
            for itemIndex in range(len(self.incomingFIXRobotAdminMessageDeque)):
                logging.debug("Logging Incoming %s Admin Message %s : %s", itemIndex,
                              self.sessID.toString(), self.incomingFIXRobotAdminMessageDeque[itemIndex].toString())
            for itemIndex in range(len(self.incomingFIXRobotAppMessageDeque)):
                logging.debug("Logging Incoming %s App Message %s : %s", itemIndex,
                              self.sessID.toString(), self.incomingFIXRobotAppMessageDeque[itemIndex].toString())
            for itemIndex in range(len(self.outgoingFIXRobotAdminMessageDeque)):
                logging.debug("Logging Outgoing %s Admin Message %s : %s", itemIndex,
                              self.sessID.toString(), self.outgoingFIXRobotAdminMessageDeque[itemIndex].toString())
            for itemIndex in range(len(self.outgoingFIXRobotAppMessageDeque)):
                logging.debug("Logging Outgoing %s App Message %s : %s", itemIndex,
                              self.sessID.toString(), self.outgoingFIXRobotAppMessageDeque[itemIndex].toString())
            logging.debug(
                "Log dumped incoming and outgoing %s Admin and App message store", self.sessID.toString())
        except Exception as e:
            logging.debug("Failed getting %s message dump!!!:%s, %s",
                          self.sessID.toString(), e.args, sys.exc_info()[0])
            raise Exception

    def clearMessageStore(self):
        '''
            This function is used to clear the message store.

                Args:
                    None.
                Returns:
                    None.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        try:
            for itemIndex in range(len(self.incomingFIXRobotAdminMessageDeque)):
                logging.debug("Clearing Incoming %s Admin Message %s : %s", itemIndex,
                              self.sessID.toString(), self.incomingFIXRobotAdminMessageDeque.popleft().toString())
            for itemIndex in range(len(self.incomingFIXRobotAppMessageDeque)):
                logging.debug("Clearing Incoming %s App Message %s : %s", itemIndex,
                              self.sessID.toString(), self.incomingFIXRobotAppMessageDeque.popleft().toString())
            for itemIndex in range(len(self.outgoingFIXRobotAdminMessageDeque)):
                logging.debug("Clearing Outgoing %s Admin Message %s : %s", itemIndex,
                              self.sessID.toString(), self.outgoingFIXRobotAdminMessageDeque.popleft().toString())
            for itemIndex in range(len(self.outgoingFIXRobotAppMessageDeque)):
                logging.debug("Clearing Outgoing %s App Message %s : %s", itemIndex,
                              self.sessID.toString(),  self.outgoingFIXRobotAppMessageDeque.popleft().toString())
            logging.debug(
                "Cleared incoming and outgoing %s Admin and App message store", self.sessID.toString())
        except Exception as e:
            logging.debug("Failed clearing %s message store!!!:%s, %s",
                          self.sessID.toString(), e.args, sys.exc_info()[0])
            raise Exception

    def setMessagePart(self, fixMessage, defaultApplVerID, incomingFIXRobotMessage, outgoingFIXRobotMessage, fixMessageString):
        '''
            This function is used to create a FIX message object to send from a FIX message template string and 
            using previous incoming and outgoing FIX messages.

                Args:
                    fixMessage(Message): FIX message object created by setting its tag values to send.
                    defaultApplVerID(str): Application version FIX4.2, FIX5.0 etc..
                    incomingFIXRobotMessage(Message): To use values from incoming message to create a new FIX message to send.
                    outgoingFIXRobotMessage(Message): To use values from outgoing message to create a new FIX message to send.
                    fixMessageString(str): FIX message template to create a new FIX message to send.
                Returns:
                    Message: Returns FIX message object.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        try:
            isGroupMessage = False
            groupCountDict = dict()
            if 'isHeaderField' in dir(fixMessage) and 'isTrailerField' in dir(fixMessage):
                isGroupMessage = False
            else:
                isGroupMessage = True
            fixTagList = fixMessageString.split("|")
            for fixTagValue in fixTagList:
                logging.debug("setMessagePart: %s", fixTagValue)
                if len(fixTagValue.strip()) > 0:
                    if(fixTagValue[0].strip() == '$'):
                        fixFunctionTag = fixTagValue
                        fixFunctionTag = fixFunctionTag.replace(' ', '').strip()[
                            1:-1]
                        fixFunctionTagSplit = fixFunctionTag.split("(")
                        fixFunction = fixFunctionTagSplit[0]
                        fixTagNameString = fixFunctionTagSplit[1].strip()
                        fixTagNameList = fixTagNameString.split(",")
                        fixTagName = fixTagNameList[0]
                        fixField = None
                        fixGroupField = None
                        fixGroupCount = None
                        if fixFunction == 'setField':
                            fixField = getattr(fix, fixTagName)()
                            if len(fixTagNameList) == 1:
                                if fixTagName in ["SendingTime", "OrigSendingTime", "OnBehalfOfSendingTime", "TransactTime"]:
                                    fixField = getattr(fix, fixTagName)()
                                    fixField.setString(getId(fixTagName))
                                else:
                                    fixField = getattr(fix, fixTagName)(
                                        getId(fixTagName))
                            elif len(fixTagNameList) == 3:
                                fixFieldSourceDirection = fixTagNameList[1]
                                fixFieldSource = getattr(
                                    fix, fixTagNameList[2])()
                                fixIntFieldSource = fixFieldSource.getField()
                                if fixFieldSourceDirection == 'IN' and incomingFIXRobotMessage is not None:
                                    sourceMessage = incomingFIXRobotMessage
                                elif fixFieldSourceDirection == 'OUT' and outgoingFIXRobotMessage is not None:
                                    sourceMessage = outgoingFIXRobotMessage
                                else:
                                    raise Exception
                                if sourceMessage.isHeaderField(fixIntFieldSource):
                                    returnStatus = sourceMessage.getHeader().getFieldIfSet(fixFieldSource)
                                elif sourceMessage.isTrailerField(fixIntFieldSource):
                                    returnStatus = sourceMessage.getTrailer().getFieldIfSet(fixFieldSource)
                                else:
                                    returnStatus = sourceMessage.getFieldIfSet(
                                        fixFieldSource)
                                if returnStatus is False:
                                    raise Exception
                                fixField.setString(fixFieldSource.getString())
                            else:
                                fixFieldSourceDirection = fixTagNameList[1]
                                fixFieldSource = getattr(
                                    fix, fixTagNameList[2])()
                                fixIntFieldSource = fixFieldSource.getField()
                                if fixFieldSourceDirection == 'IN' and incomingFIXRobotMessage:
                                    sourceMessage = incomingFIXRobotMessage
                                elif fixFieldSourceDirection == 'OUT' and outgoingFIXRobotMessage:
                                    sourceMessage = outgoingFIXRobotMessage
                                else:
                                    raise Exception
                                sourceMessageGroup = sourceMessage
                                groupPos = 0
                                fixMessageGroup = sourceMessage
                                for listIndex in range(3, len(fixTagNameList), 2):
                                    groupPos = int(fixTagNameList[listIndex])
                                    groupField = getattr(
                                        fix, fixTagNameList[listIndex + 1])()
                                    fixMessageGroup = fix.Group(
                                        groupField.getField(), 1)
                                    sourceMessageGroup = sourceMessageGroup.getGroup(
                                        groupPos, fixMessageGroup)
                                returnStatus = fixMessageGroup.getFieldIfSet(
                                    fixFieldSource)
                                if returnStatus is False:
                                    raise Exception
                                fixField.setString(fixFieldSource.getString())
                        elif fixFunction == 'addGroup':
                            fixMessageLineName = fixTagNameList[0]
                            if len(fixTagNameList) > 1:
                                fixTagName = fixTagNameList[1]
                                if fixTagName.isdigit():
                                    fixGroupField = fix.IntField(
                                        int(fixTagName))
                                else:
                                    fixGroupField = getattr(fix, fixTagName)()
                            else:
                                fixGroupField = None
                            logging.debug(
                                "DefaultMessageLineName: %s", fixMessageLineName)
                            defaultMessageLine = self.defaultMessageConfig.get(
                                defaultApplVerID, fixMessageLineName)
                            defaultMessageLineList = defaultMessageLine.split(
                                ",")
                            subMessageType = defaultMessageLineList[0]
                            fixMessageSubString = defaultMessageLineList[1]
                            logging.debug(
                                "DefaultMessageName: %s", subMessageType)
                            logging.debug("DefaultMessage: %s",
                                          fixMessageSubString)
                            fixMessageGroup = getattr(
                                fixMessage, subMessageType)()
                            if subMessageType not in groupCountDict:
                                groupCountDict[subMessageType] = 1
                            else:
                                groupCountDict[subMessageType] = groupCountDict[
                                    subMessageType] + 1
                            incomingFIXRobotMessageGroup = getattr(
                                fixMessage, subMessageType)()
                            outgoingFIXRobotMessageGroup = getattr(
                                fixMessage, subMessageType)()
                            if incomingFIXRobotMessage is not None:
                                if incomingFIXRobotMessage.hasGroup(groupCountDict[subMessageType], incomingFIXRobotMessageGroup):
                                    incomingFIXRobotMessage.getGroup(
                                        groupCountDict[subMessageType], incomingFIXRobotMessageGroup)
                            else:
                                incomingFIXRobotMessageGroup = None
                            if outgoingFIXRobotMessage is not None:
                                if outgoingFIXRobotMessage.hasGroup(groupCountDict[subMessageType], outgoingFIXRobotMessageGroup):
                                    outgoingFIXRobotMessage.getGroup(
                                        groupCountDict[subMessageType], outgoingFIXRobotMessageGroup)
                            else:
                                incomingFIXRobotMessageGroup = None
                            fixField = self.setMessagePart(
                                fixMessageGroup, defaultApplVerID, incomingFIXRobotMessageGroup, outgoingFIXRobotMessageGroup,
                                fixMessageSubString)
                            fixGroupCount = groupCountDict[subMessageType]
                        if isGroupMessage or fixFunction == 'addGroup':
                            if fixGroupField is not None:
                                fixGroupField.setString(str(fixGroupCount))
                                fixField.setField(fixGroupField)
                            getattr(fixMessage, fixFunction)(fixField)
                        elif fixFunction == 'setField':
                            fixIntField = fixField.getField()
                            if fixMessage.isHeaderField(fixIntField):
                                getattr(fixMessage.getHeader(),
                                        fixFunction)(fixField)
                            elif fixMessage.isTrailerField(fixIntField):
                                getattr(fixMessage.getTrailer(),
                                        fixFunction)(fixField)
                            else:
                                getattr(fixMessage, fixFunction)(fixField)
                    else:
                        fixTagValueSplit = fixTagValue.split("=")
                        fixIntTag = int(fixTagValueSplit[0])
                        fixIntTagValue = fixTagValueSplit[1]
                        if (not isGroupMessage):
                            if fixMessage.isHeaderField(fixIntTag):
                                if(not fixMessage.getHeader().isSetField(fixIntTag)):
                                    fixMessage.getHeader().setField(fix.StringField(fixIntTag, fixIntTagValue))
                            elif fixMessage.isTrailerField(fixIntTag):
                                if(not fixMessage.getTrailer().isSetField(fixIntTag)):
                                    fixMessage.getTrailer().setField(fix.StringField(fixIntTag, fixIntTagValue))
                            elif (not fixMessage.isSetField(fixIntTag)):
                                fixMessage.setField(fix.StringField(
                                    fixIntTag, fixIntTagValue))
                        else:
                            if (not fixMessage.isSetField(fixIntTag)):
                                fixMessage.setField(fix.StringField(
                                    fixIntTag, fixIntTagValue))
            return fixMessage
        except Exception as e:
            logging.debug("Exception!!!:%s, %s", e.args, sys.exc_info()[0])

    def checkMessagePart(self, fixMessage, defaultApplVerID, fixGroupNumField, fixVersionEvalString, expectedFIXRobotMessageName,
                         fixMessageString):
        '''
            This function is used to compare an actual FIX message against the expected FIX message.
            The tag value comparison results are written to the log file and returns the status of comparison.

                Args:
                    fixMessage(Message): Actual FIX message object to be compared.
                    defaultApplVerID(str): FIX Application version FIX4.2, FIX5.0 etc..
                    fixGroupNumField(Group): Nested group name inside a FIX message object.
                    fixVersionEvalString(str): FIX version FIX4.2, FIXT1.1 etc..
                    expectedFIXRobotMessageName(str): FIX message name.
                    fixMessageString(str): Expected FIX message in string template format
                Returns:
                    bool: Returns True if difference is found during comparison of actual and expected FIX messages and False otherwise.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        try:
            logging.debug("checkMessagePart DefaultMessage: %s",
                          fixMessageString)
            isGroupMessage = False
            differenceFound = False
            groupDict = dict()
            if 'isHeaderField' in dir(fixMessage) and 'isTrailerField' in dir(fixMessage):
                isGroupMessage = False
            else:
                isGroupMessage = True
            fixTagList = fixMessageString.split("|")
            for fixTagValue in fixTagList:
                logging.debug("checkMessagePart: %s", fixTagValue)
                if len(fixTagValue.strip()) > 0:
                    if(fixTagValue[0].strip() == '$'):
                        fixFunctionTag = fixTagValue
                        fixFunctionTag = fixFunctionTag.replace(' ', '').strip()[
                            1:-1]
                        fixFunctionTagSplit = fixFunctionTag.split("(")
                        fixFunction = fixFunctionTagSplit[0]
                        #fixTagName = fixFunctionTagSplit[1].strip().split(',')[0]
                        fixTagNameString = fixFunctionTagSplit[1].strip()
                        fixTagNameList = fixTagNameString.split(",")
                        fixTagName = fixTagNameList[0]
                        if fixFunction == 'setField':
                            fixField = getattr(fix, fixTagName)()
                            fixIntTag = fixField.getField()
                            if not isGroupMessage:
                                if fixMessage.isHeaderField(fixIntTag):
                                    if fixMessage.getHeader().getFieldIfSet(fixField):
                                        resultString = "FIXTag-" + \
                                            str(fixIntTag) + ": Present"
                                    else:
                                        resultString = "FIXTag-" + \
                                            str(fixIntTag) + ": Absent"
                                elif fixMessage.isTrailerField(fixIntTag):
                                    if fixMessage.getTrailer().getFieldIfSet(fixField):
                                        resultString = "FIXTag-" + \
                                            str(fixIntTag) + ": Present"
                                    else:
                                        resultString = "FIXTag-" + \
                                            str(fixIntTag) + ": Absent"
                                else:
                                    if fixMessage.getFieldIfSet(fixField):
                                        resultString = "FIXTag-" + \
                                            str(fixIntTag) + ": Present"
                                    else:
                                        resultString = "FIXTag-" + \
                                            str(fixIntTag) + ": Absent"
                            else:
                                if fixMessage.getFieldIfSet(fixField):
                                    resultString = "FIXTag-" + \
                                        str(fixIntTag) + ": Present"
                                else:
                                    resultString = "FIXTag-" + \
                                        str(fixIntTag) + ": Absent"
                            self.cmpResultList.append(resultString)
                        elif fixFunction == 'addGroup':
                            fixMessageLineName = fixTagNameList[0]
                            if len(fixTagNameList) == 2:
                                fixGroupNumFieldTag = fixTagNameList[1]
                            else:
                                fixGroupNumFieldTag = None
                            logging.debug("fixTagNameList:%s", fixTagNameList)
                            logging.debug("fixGroupNumFieldTag:%s",
                                          fixGroupNumFieldTag)
                            logging.debug(
                                "checkMessagePart DefaultMessageLineName: %s", fixTagName)
                            defaultMessageLine = self.defaultMessageConfig.get(
                                defaultApplVerID, fixTagName)
                            defaultMessageLineList = defaultMessageLine.split(
                                ",")
                            subMessageType = defaultMessageLineList[0]
                            fixMessageSubString = defaultMessageLineList[1]
                            if subMessageType in groupDict.keys():
                                groupDict[subMessageType] = groupDict[
                                    subMessageType] + 1
                            else:
                                groupDict[subMessageType] = 1
                            logging.debug(
                                "checkMessagePart DefaultMessageName: %s", subMessageType)
                            logging.debug(
                                "checkMessagePart DefaultMessage: %s", fixMessageSubString)
                            newfixVersionEvalString = fixVersionEvalString + "." + expectedFIXRobotMessageName
                            fixMessageGroup = getattr(
                                eval(newfixVersionEvalString), subMessageType)()
                            fixMessage.getGroup(
                                groupDict[subMessageType], fixMessageGroup)
                            #fixGroupNum = groupDict[subMessageType]
                            differenceFoundNew = self.checkMessagePart(
                                fixMessageGroup, defaultApplVerID, copy.copy(
                                    fixGroupNumFieldTag), newfixVersionEvalString, subMessageType,
                                fixMessageSubString)
                            differenceFound = differenceFound or differenceFoundNew
                    else:
                        fixTagValueSplit = fixTagValue.split("=")
                        expectingTag = int(fixTagValueSplit[0])
                        expectingValue = fixTagValueSplit[1]
                        if (not isGroupMessage):
                            if fixMessage.isHeaderField(expectingTag):
                                if(fixMessage.getHeader().isSetField(expectingTag)):
                                    receivedValue = fixMessage.getHeader().getField(expectingTag)
                                else:
                                    receivedValue = ""
                            elif fixMessage.isTrailerField(expectingTag):
                                if(fixMessage.getTrailer().isSetField(expectingTag)):
                                    receivedValue = fixMessage.getTrailer().getField(expectingTag)
                                else:
                                    receivedValue = ""
                            elif (fixMessage.isSetField(expectingTag)):
                                receivedValue = fixMessage.getField(
                                    expectingTag)
                            else:
                                receivedValue = ""
                        else:

                            if (fixMessage.isSetField(expectingTag)):
                                receivedValue = fixMessage.getField(
                                    expectingTag)
                            else:
                                receivedValue = ""
                            logging.debug("fixGroupNumField:%s",
                                          fixGroupNumField)
                            logging.debug("expectingTag:%s", str(expectingTag))
                            logging.debug("expectingValue:%s",
                                          str(expectingValue))
                            if fixGroupNumField is not None:
                                if not fixGroupNumField.isdigit():
                                    fixGroupNumField = getattr(
                                        fix, fixGroupNumField).getField()
                                if receivedValue and expectingTag == int(fixGroupNumField):
                                    expectingValue = receivedValue
                                    logging.debug(
                                        "Inside expecting %s and received %s ", expectingValue, receivedValue)

                        if not(receivedValue) or expectingValue != receivedValue:
                            resultString = "FIXTag-" + \
                                str(expectingTag) + ": Received " + receivedValue + \
                                " != " + expectingValue + " Expecting"
                            differenceFound = True
                        else:
                            resultString = "FIXTag-" + \
                                str(expectingTag) + ": Received " + receivedValue + \
                                " == " + expectingValue + " Expecting"
                        self.cmpResultList.append(resultString)
            logging.debug("Difference Found %s", str(differenceFound))
            return differenceFound
        except Exception as e:
            logging.debug("Exception!!! %s, %s", e.args, sys.exc_info()[0])

    def sendFIXRobotMessage(self, defaultAdminVerID, defaultApplVerID, *args):
        '''
            This function is used to send the FIX message.

                Args:
                    defaultAdminVerID(str): FIX admin version FIX4.2, FIXT1.1 etc..
                    defaultApplVerID(str): FIX application version FIX4.2, FIX5.0 etc..
                    *args(vargs): FIX message is a variable argument which is mentioned
                              either as a message template name in the message template dictionary
                              or as a message type name and message string.                                                         
                Returns:
                    Message: Returns fix message which is sent.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        try:
            fixAdminVersionEvalString = defaultAdminVerID.strip().replace('.', '').lower()
            fixVersionEvalString = defaultApplVerID.strip().replace('.', '').lower()
            fixAdminVersionEval = eval(fixAdminVersionEvalString)
            fixVersionEval = eval(fixVersionEvalString)
            if len(args) == 1:
                outMessageName = args[0]
                logging.debug("DefaultMessageLineName: %s", outMessageName)
                #beginString = str(self.sessID.getBeginString())
                #fixVersion = beginString.strip('\x01').split('=')[1]
                defaultMessageLine = self.defaultMessageConfig.get(
                    defaultApplVerID, outMessageName)
                defaultMessageLineList = defaultMessageLine.split(",", 1)
                outgoingFIXRobotMessageName = defaultMessageLineList[0]
                defaultMessage = defaultMessageLineList[1]
            elif len(args) == 2:
                outgoingFIXRobotMessageName = args[0]
                defaultMessage = args[1]
            else:
                logging.debug(
                    "sendFIXRobotMessage incorrect number of arguments %s", *args)
                raise Exception
            logging.debug("DefaultMessageName: %s",
                          outgoingFIXRobotMessageName)
            logging.debug("DefaultMessage: %s", defaultMessage)
            #fixMessage = fix42.Message()
            #fixMessage = getattr(fix42, outgoingFIXRobotMessageName)()
            if(outgoingFIXRobotMessageName in ["Heartbeat", "TestRequest", "ResendRequest", "Reject", "SequenceReset", "Logon", "Logout"]):
                fixMessage = getattr(
                    fixAdminVersionEval, outgoingFIXRobotMessageName)()
            else:
                fixMessage = getattr(
                    fixVersionEval, outgoingFIXRobotMessageName)()
            fixMsgEval = FIXMessageEvaluator()
            if fixMessage.isApp():
                if len(self.incomingFIXRobotAppMessageDeque) > 0:
                    incomingFIXRobotMessage = self.incomingFIXRobotAppMessageDeque.popleft()
                    self.incomingFIXRobotAppMessageDeque.append(
                        fix.Message(incomingFIXRobotMessage))
                else:
                    incomingFIXRobotMessage = None
                if len(self.outgoingFIXRobotAppMessageDeque) > 0:
                    outgoingFIXRobotMessage = self.outgoingFIXRobotAppMessageDeque.popleft()
                    self.outgoingFIXRobotAppMessageDeque.append(
                        fix.Message(outgoingFIXRobotMessage))
                else:
                    outgoingFIXRobotMessage = None
            elif fixMessage.isAdmin():
                if len(self.incomingFIXRobotAdminMessageDeque) > 0:
                    incomingFIXRobotMessage = self.incomingFIXRobotAdminMessageDeque.popleft()
                    self.incomingFIXRobotAdminMessageDeque.append(

                        fix.Message(incomingFIXRobotMessage))
                else:
                    incomingFIXRobotMessage = None
                if len(self.outgoingFIXRobotAdminMessageDeque) > 0:
                    outgoingFIXRobotMessage = self.outgoingFIXRobotAdminMessageDeque.popleft()
                    self.outgoingFIXRobotAdminMessageDeque.append(
                        fix.Message(outgoingFIXRobotMessage))
                else:
                    outgoingFIXRobotMessage = None
            if outgoingFIXRobotMessageName != None:
                fixMessage.getHeader().setField(fix.MsgType(fixMsgEval.evalMsgType(
                                                outgoingFIXRobotMessageName)))
                fixMessage = self.setMessagePart(fixMessage, defaultApplVerID, incomingFIXRobotMessage, outgoingFIXRobotMessage,
                                                 defaultMessage)
            else:
                raise Exception
            logging.debug("Sending %s app message: %s",
                          self.sessID.toString(), fixMessage.toString())
            # self.incomingFIXRobotAppMessageDeque.clear()
            # self.incomingFIXRobotAdminMessageDeque.clear()
            fix.Session.sendToTarget(fixMessage, self.sessID)
            logging.debug("Sent %s app message: %s",
                          self.sessID.toString(), fixMessage.toString())
            return fixMessage
        except Exception as e:
            logging.debug("Failed sending app message by %s!!!",
                          self.sessID.toString())
            logging.debug("Failed sending app message by %s, %s!!!",
                          e.args, sys.exc_info()[0])
            raise Exception

    def receiveFIXRobotMessage(self, defaultAdminVerID, defaultApplVerID, *args):
        '''
            This function is used to receive the FIX message.

                Args:
                    defaultAdminVerID(str): FIX admin version FIX4.2, FIXT1.1 etc..
                    defaultApplVerID(str): FIX application version FIX4.2, FIX5.0 etc..
                    *args(vargs): FIX message is a variable argument which is mentioned
                              either as a message template name in the message template dictionary
                              or as a message type name and message string.                                                         
                Returns:
                    Message: Returns fix message which is received.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        try:
            self.cmpResultList = list()
            fixAdminVersionEvalString = defaultAdminVerID.strip().replace('.', '').lower()
            fixVersionEvalString = defaultApplVerID.strip().replace('.', '').lower()
            fixAdminVersionEval = eval(fixAdminVersionEvalString)
            fixVersionEval = eval(fixVersionEvalString)
            beginString = str(self.sessID.getBeginString())
            if len(args) == 1:
                inMessageName = args[0]
                logging.debug("%s DefaultMessageLineName: %s",
                              self.sessID.toString(), inMessageName)
                defaultMessageLine = self.defaultMessageConfig.get(
                    defaultApplVerID, inMessageName)
                defaultMessageLineList = defaultMessageLine.split(",", 1)
                expectedFIXRobotMessageName = defaultMessageLineList[0]
                expectedFIXRobotMessageString = defaultMessageLineList[1]
            elif len(args) == 2:
                expectedFIXRobotMessageName = args[0]
                expectedFIXRobotMessageString = args[1]
            else:
                logging.debug(
                    "% Received message incorrect number of arguments %s", self.sessID.toString(), args)
                raise Exception
            logging.debug("%s DefaultMessageName: %s",
                          self.sessID.toString(), expectedFIXRobotMessageName)
            logging.debug("%s DefaultMessage: %s",
                          self.sessID.toString(), expectedFIXRobotMessageString)
            differenceFound = False
            fixMessage = fix.Message()
            fixMsgEval = FIXMessageEvaluator()
            if expectedFIXRobotMessageName != None:
                fixMessage.getHeader().setField(fix.MsgType(fixMsgEval.evalMsgType(
                                                expectedFIXRobotMessageName)))
            if fixMessage.isApp() is True:
                incomingFIXRobotMessage = self.incomingFIXRobotAppMessageDeque.popleft()
                self.incomingFIXRobotAppMessageDeque.append(
                    fix.Message(incomingFIXRobotMessage))
            elif fixMessage.isAdmin() is True:
                incomingFIXRobotMessage = self.incomingFIXRobotAdminMessageDeque.popleft()
                self.incomingFIXRobotAdminMessageDeque.append(
                    fix.Message(incomingFIXRobotMessage))
            if expectedFIXRobotMessageName is not None:
                expectingMessageType = fixMsgEval.evalMsgType(
                    expectedFIXRobotMessageName)
                msgType = fix.MsgType()
                incomingFIXRobotMessage.getHeader().getField(msgType)
                receivedMessageType = msgType.getValue()
                receivedMessageType = str(msgType)
                logging.debug("Received messageType: %s", receivedMessageType)
                receivedMessageType = msgType.getValue()
                if expectingMessageType != receivedMessageType:
                    resultString = "MessageType: Received " + receivedMessageType + \
                        " != " + expectingMessageType + " Expecting"
                    differenceFound = True
                else:
                    resultString = "MessageType: Received " + receivedMessageType + \
                        " == " + expectingMessageType + " Expecting"
                self.cmpResultList.append(resultString)
                if expectedFIXRobotMessageString != None:
                    incomingFIXRobotMessage = fix.Message(
                        incomingFIXRobotMessage)
                    differenceFoundNew = self.checkMessagePart(
                        incomingFIXRobotMessage, defaultApplVerID, None, fixVersionEvalString, expectedFIXRobotMessageName,
                        expectedFIXRobotMessageString)
                    differenceFound = differenceFound or differenceFoundNew
                else:
                    logging.debug(
                        "%s Expected MessageString is empty!!! %s", self.sessID.toString(), expectedFIXRobotMessageString)
                    raise Exception
            for item in self.cmpResultList:
                logging.debug(item)
            if differenceFound == True:
                logging.debug(
                    "Received message is not same as expected message")
                raise Exception
            else:
                logging.debug("Received message is same as expected message")
                return incomingFIXRobotMessage
        except Exception as e:
            logging.debug("%s Failed receiving app message by !!!%s, %s",
                          self.sessID.toString(), e.args, sys.exc_info()[0])
            raise Exception


class fixrobot():
    '''
        fixrobot class creates a FIX connection and/or then send and receive FIX messages
    '''
    def startFIXRobot(self, conn_name, instanceType):
        '''
            Starts a fix connection for a specified connection name and type of instance as initiator or acceptor.

                Args:
                    conn_name(str): FIX connection name.
                    instanceType(str): Type of the instance as initiator or acceptor.
                Returns:
                    bool: The return value. True for success, False otherwise
                Raises:
                    Exception: Raises exception when error occours.
        '''    
        try:
            # self.stdout_backup=sys.stdout
            # self.trash_file=open('file', 'w')
            # sys.stdout=self.trash_file
            config = configparser.ConfigParser()
            config.read(os.path.join(
                os.environ["FIXROBOTPATH"], "env", "connections.ini"))
            config_file = config.get("CONNECTIONS", conn_name)
            fixConnectionsFile = config.get("CONNECTIONS", conn_name)
            fixConnectionFileFullPath = str(os.path.join(
                os.environ["FIXROBOTPATH"], "env", fixConnectionsFile))
            settings = fix.SessionSettings(fixConnectionFileFullPath)
            dictionary = settings.get()
            id1 = fix.SessionID(dictionary.getString(fix.BEGINSTRING),
                                dictionary.getString(fix.SENDERCOMPID),
                                dictionary.getString(fix.TARGETCOMPID))
            self.defaultApplVerID = dictionary.getString(fix.BEGINSTRING)
            self.defaultAdminVerID = ""
            if self.defaultApplVerID == "FIXT.1.1":
                self.defaultAdminVerID = "FIXT.1.1"
                self.defaultApplVerID = dictionary.getString(
                    fix.DEFAULT_APPLVERID)
                dictionary.setString(fix.TRANSPORT_DATA_DICTIONARY, str(os.path.join(
                    os.environ["FIXROBOTPATH"], dictionary.getString(fix.TRANSPORT_DATA_DICTIONARY))))
                dictionary.setString(fix.APP_DATA_DICTIONARY, str(os.path.join(
                    os.environ["FIXROBOTPATH"], dictionary.getString(fix.APP_DATA_DICTIONARY))))
                dictionary.setString(fix.FILE_LOG_PATH, str(os.path.join(
                    os.environ["FIXROBOTPATH"], dictionary.getString(fix.FILE_LOG_PATH))))
                dictionary.setString(fix.FILE_STORE_PATH, str(os.path.join(
                    os.environ["FIXROBOTPATH"], dictionary.getString(fix.FILE_STORE_PATH))))
            else:
                self.defaultAdminVerID = self.defaultApplVerID
                dictionary.setString(fix.DATA_DICTIONARY, str(os.path.join(
                    os.environ["FIXROBOTPATH"], dictionary.getString(fix.DATA_DICTIONARY))))
                dictionary.setString(fix.FILE_LOG_PATH, str(os.path.join(
                    os.environ["FIXROBOTPATH"], dictionary.getString(fix.FILE_LOG_PATH))))
                dictionary.setString(fix.FILE_STORE_PATH, str(os.path.join(
                    os.environ["FIXROBOTPATH"], dictionary.getString(fix.FILE_STORE_PATH))))
            settings.set(id1, dictionary)

            storeFactory = fix.FileStoreFactory(settings)
            logFactory = fix.FileLogFactory(settings)
            # logFactory = fix.ScreenLogFactory(settings)
            if(instanceType == "INITIATOR"):
                self.application = FIXRobotProcessor()
                self.fixRobot = fix.SocketInitiator(self.application,
                                                    storeFactory,
                                                    settings,
                                                    logFactory)
                self.fixRobot.start()
                logging.debug("Initiator started")
                return True
            elif(instanceType == "ACCEPTOR"):
                self.application = FIXRobotProcessor()
                self.fixRobot = fix.SocketAcceptor(self.application,
                                                   storeFactory,
                                                   settings,
                                                   logFactory)
                self.fixRobot.start()
                logging.debug("Acceptor started")
                return True
            return False
        except Exception as e:
            logging.debug("Failed connecting initator!!!%s - %s",
                          e.args, sys.exc_info()[0])
            raise Exception

    def startInitiator(self, conn_name):
        '''
            Starts initiator for a given connection name.

                Args:
                    conn_name(str): FIX connection name.
                Returns:
                    bool: The return value. True for success, False otherwise
                Raises:
                    Exception: Raises exception when error occours.
        '''    
        try:
            returnValue = self.startFIXRobot(conn_name, "INITIATOR")
            return returnValue
        except Exception as e:
            logging.debug("Failed connecting initator!!!",
                          e.args, sys.exc_info()[0])
            raise Exception

    def startAcceptor(self, conn_name):
        '''
            Starts acceptor for a given connection name.

                Args:
                    conn_name(str): FIX connection name.
                Returns:
                    bool: The return value. True for success, False otherwise
                Raises:
                    Exception: Raises exception when error occours.
        ''' 
        try:
            returnValue = self.startFIXRobot(conn_name, "ACCEPTOR")
            return returnValue
        except Exception as e:
            logging.debug("Failed starting acceptor!!!:%s - %s",
                          e.args, sys.exc_info()[0])
            raise

    def sendMessage(self, *args):
        '''
            Send FIX message to the FIX connection.

                Args:
                    *args(vargs): FIX message is a variable argument which is mentioned
                                  either as a message template name in the message template dictionary
                                  or as a message type name and message string.
                Returns:
                    Message: Returns fix message which is received.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        try:
            if (len(args) == 1) or (len(args) == 2):
                fixMessage = self.application.sendFIXRobotMessage(
                    self.defaultAdminVerID, self.defaultApplVerID, *args)
            else:
                logging.debug(
                    "sendFIXRobotMessage incorrect number of arguments %s", *args)
                raise Exception
            return fixMessage
        except Exception as e:
            logging.debug("Failed sending fixrobot message!!!%s - %s",
                          e.args, sys.exc_info()[0])
            raise Exception

    def receiveMessage(self, *args):
        '''
            Receive FIX message from the FIX connection.

                Args:
                    *args(vargs): FIX message is a variable argument which is mentioned
                                  either as a message template name in the message template dictionary
                                  or as a message type name and message string.
                Returns:
                    Message: Returns fix message which is received.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        try:
            if (len(args) == 1) or (len(args) == 2):
                fixMessage = self.application.receiveFIXRobotMessage(
                    self.defaultAdminVerID, self.defaultApplVerID, *args)
            else:
                logging.debug(
                    "receiveFIXRobotMessage incorrect number of arguments %s", *args)
                raise Exception
            return fixMessage
        except Exception as e:
            logging.debug("Failed receiving fixrobot message or Difference found!!!%s - %s",
                          e.args, sys.exc_info()[0])
            raise Exception

    def getExpectedSenderNum(self):
        '''
            This function is used to get the next out sequence number.

                Args:
                    None.
                Returns:
                    None.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        try:
            senderSeqNo = self.application.getExpectedSenderNum()
            return senderSeqNo
        except Exception as e:
            logging.debug("Failed receiving sender sequence number!!!",
                          e.args, sys.exc_info()[0])
            raise Exception

    def setNextSenderMsgSeqNum(self, senderSeqNo):
        '''
            This function is used to set the next out sequence number.

                Args:
                    senderSeqNo(int): Out sequence number to set.
                Returns:
                    None.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        try:
            self.application.setNextSenderMsgSeqNum(senderSeqNo)
            return True
        except Exception as e:
            logging.debug("Failed setting sender sequence number!!!",
                          e.args, sys.exc_info()[0])
            raise Exception

    def getExpectedTargetNum(self):
        '''
            This function is used to get the next in sequence number.

                Args:
                    None.
                Returns:
                    None.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        try:
            targetSeqNo = self.application.getExpectedTargetNum()
            return targetSeqNo
        except Exception as e:
            logging.debug("Failed receiving target sequence number!!!",
                          e.args, sys.exc_info()[0])
            raise Exception

    def setNextTargetMsgSeqNum(self, targetSeqNo):
        '''
            This function is used to set the next expected in sequence number.

                Args:
                    targetSeqNo(int): In sequence number to set.
                Returns:
                    None.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        try:
            self.application.setNextTargetMsgSeqNum(targetSeqNo)
            return True
        except Exception as e:
            logging.debug("Failed setting target sequence number!!!",
                          e.args, sys.exc_info()[0])
            raise Exception

    def logDumpMessageStore(self):
        '''
            This function is used to dump a copy of messages into the logs.

                Args:
                    None.
                Returns:
                    None.
                Raises:
                    Exception: Raises exception when error occours.

        '''
        try:
            self.application.logDumpMessageStore()
            return True
        except Exception as e:
            logging.debug("Failed log dump message store!!!",
                          e.args, sys.exc_info()[0])
            raise Exception

    def clearMessageStore(self):
        '''
            This function is used to clear the message store.

                Args:
                    None.
                Returns:
                    None.
                Raises:
                    Exception: Raises exception when error occours.
        '''
        try:
            self.application.clearMessageStore()
            return True
        except Exception as e:
            logging.debug("Failed clearing message store!!!",
                          e.args, sys.exc_info()[0])
            raise Exception

    def stopInitiator(self):
        '''
            Stops initiator for a given connection name.

                Args:
                    None.
                Returns:
                    None.
                Raises:
                    Exception: Raises exception when error occours.
        '''  
        try:
            self.fixRobot.stop()
            logging.debug("Initiator stopped")
            return True
        except Exception as e:
            logging.debug("Failed disconnecting initiator!!!",
                          e.args, sys.exc_info()[0])
            raise Exception

    def stopAcceptor(self):
        '''
            Stops acceptor for a given connection name.

                Args:
                    None.
                Returns:
                    None.
                Raises:
                    Exception: Raises exception when error occours.
        '''  
        try:
            self.fixRobot.stop()
            logging.debug("Acceptor stopped")
            return True
        except Exception as e:
            logging.debug("Failed disconnecting acceptor!!!:%s, %s",
                          e.args, sys.exc_info()[0])
            raise

if __name__ == "__main__":
    try:
        print("Author: Written by Anand P. Subramanian.")
        print("Copyright: fixrobot  Copyright (C) 2016  Anand P. Subramanian.")
        print("License: GGPLv3+ GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.")
        print("Reporting bugs: https://github.com/quickfixrobot/FIXRobot/issues")
        print("Usage: import fixrobot")
    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
