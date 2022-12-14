# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
from datetime import datetime
import logging
import boto3
from boto3.dynamodb.conditions import Attr
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEFAULT_MAX_LIMIT = 5
topics_remapped = {"sports": "Sports and Recreation", "community service": "Community Service", "academic": "Academic/College"}

client = boto3.client('dynamodb')

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, to Clubbify!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?F"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class TopClubIntentHandler(AbstractRequestHandler):
    "Handler for Top Club Intent."
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("topclub")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # get the slots value numClubs from handler_input, top numClubs club
        numClubs = ask_utils.request_util.get_slot(handler_input, "numClubs").value
        if not numClubs:
            numClubs = DEFAULT_MAX_LIMIT
        else:
            numClubs = int(numClubs)
            
        data = client.scan(
            TableName='clubs',
            Limit=numClubs
        )

        speak_output = ""
        for club in data['Items']:
            speak_output += club['club_name']['S'] + ',\n'

        speak_output = speak_output[:len(speak_output)-2]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class DescribeClubIntentHandler(AbstractRequestHandler):
    "Handler for DescribeClub Intent."
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DescribeClub")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # get the slots value numClubs from handler_input, top numClubs club
        club_name = ask_utils.request_util.get_slot(handler_input, "club_name").value
        club_name = ' '.join([c.capitalize() for c in club_name.split()])
        data = client.query(
            TableName= 'clubs',
            KeyConditionExpression='club_name=:c',
            ExpressionAttributeValues={
                ':c': {'S': club_name},
            },
            ProjectionExpression='statement',
        )

        speak_output = ""
        club = data['Items'][0]
        speak_output += club['statement']['S']

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class EventsIntentHandler(AbstractRequestHandler):
    "Handler for Events Intent."
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("events")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # get the variables from handler_input
        # day (date)
        d = ask_utils.request_util.get_slot(handler_input, "day")
        # y (number of events)
        y = ask_utils.request_util.get_slot(handler_input, "y")
        # club name
        clubName = ask_utils.request_util.get_slot(handler_input, "club")
        # depending on how many variables are not null, filter the database to find the desired result using query
        t = ""
        if d.value:
            t += d.value
        if y.value:
            t += y.value
        if clubName.value:
            t += clubName.value
        speak_output = t

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class MyInterestsIntentHandler(AbstractRequestHandler):
    "Handler for My Interests Intent."
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("myinterests")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # get see if user interests are stored in the database
        # if so put it out
        speak_output = "myinterests basic test"
        # otherwise, say no interests are recorded

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class InputInterestsIntentHandler(AbstractRequestHandler):
    "Handler for Input Interests Intent."
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("inputinterests")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # get the user inputed interests from handler_input
        i = ask_utils.request_util.get_slot(handler_input, "interests")
        # if the user inputed interests
        if i.value:
            # pass the string to another method that filters it down
            # and store the filtered down list into an set
            # first get rid of all duplicates
            r = set(i.value.split())
            # store that set in the database with user id
            speak_output = " ".join(list(r))
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class DynamoTestIntentHandler(AbstractRequestHandler):
    """Handler for DynamoTest Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DynamoTest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = client.get_item(
            TableName='clubs',
            Key={
                'club_name': {
                    "S": "Give Kids a Smile",
                },
                'day': {
                    "N": "3",
                }
            },
        )
        dataStr = str(data)

        return (
            handler_input.response_builder
                .speak(dataStr)
                .ask(dataStr)
                .response
        )

class BeforeTimeIntentHandler(AbstractRequestHandler):
    "Handler for BeforeTime Intent."
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("BeforeTime")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # get the slots value x from handler_input, top x club
        s = ask_utils.request_util.get_slot(handler_input, "time")
        time = ''.join(s.value.split(':'))
        curday = datetime.now().weekday() + 1
        if curday == 7:
            curday = 0
        data = client.query(
            IndexName= 'day-time-index',
            TableName='clubs',
            KeyConditionExpression='#da=:d AND #ti<:t',
            ExpressionAttributeValues={
                ':d': {'N': str(curday)},
                ':t': {'N': time},
            },
            ExpressionAttributeNames={'#da': 'day', '#ti': 'time'},
            ProjectionExpression='club_name',
        )
        speak_output = ""
        for club in data['Items'][:5]:
            speak_output += club['club_name']['S'] + ',\n'

        speak_output = speak_output[:len(speak_output)-2]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class BeforeTimeTopicIntentHandler(AbstractRequestHandler):
    "Handler for BeforeTimeTopic Intent."
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("BeforeTimeTopic")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # get the slots value x from handler_input, top x club
        s = ask_utils.request_util.get_slot(handler_input, "time")
        time = ''.join(s.value.split(':'))
        input_topic = ask_utils.request_util.get_slot(handler_input, "topic").value

        curday = datetime.now().weekday() + 1
        if curday == 7:
            curday = 0
        data = client.query(
            IndexName= 'day-time-index',
            TableName='clubs',
            KeyConditionExpression='#da=:d AND #ti<:t',
            ExpressionAttributeValues={
                ':d': {'N': str(curday)},
                ':t': {'N': time},
                ':topic': {'S' : input_topic}
            },
            FilterExpression='contains(topics,:topic)',
            ExpressionAttributeNames={'#da': 'day', '#ti': 'time'},
            ProjectionExpression='club_name',
        )
        speak_output = ""
        for club in data['Items'][:5]:
            speak_output += club['club_name']['S'] + ',\n'

        speak_output = speak_output[:len(speak_output)-2]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class AfterTimeIntentHandler(AbstractRequestHandler):
    "Handler for AfterTime Intent."
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AfterTime")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # get the slots value x from handler_input, top x club
        s = ask_utils.request_util.get_slot(handler_input, "time")
        time = ''.join(s.value.split(':'))
        curday = datetime.now().weekday() + 1
        if curday == 7:
            curday = 0
        data = client.query(
            IndexName= 'day-time-index',
            TableName='clubs',
            KeyConditionExpression='#da=:d AND #ti>=:t',
            ExpressionAttributeValues={
                ':d': {'N': str(curday)},
                ':t': {'N': time},
            },
            ExpressionAttributeNames={'#da': 'day', '#ti': 'time'},
            ProjectionExpression='club_name',
        )
        speak_output = ""
        for club in data['Items'][:5]:
            speak_output += club['club_name']['S'] + ',\n'

        speak_output = speak_output[:len(speak_output)-2]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class AfterTimeTopicIntentHandler(AbstractRequestHandler):
    "Handler for AfterTimeTopic Intent."
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AfterTimeTopic")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # get the slots value x from handler_input, top x club
        s = ask_utils.request_util.get_slot(handler_input, "time")
        time = ''.join(s.value.split(':'))
        input_topic = ask_utils.request_util.get_slot(handler_input, "topic").value
        curday = datetime.now().weekday() + 1
        if curday == 7:
            curday = 0
        data = client.query(
            IndexName= 'day-time-index',
            TableName='clubs',
            KeyConditionExpression='#da=:d AND #ti>=:t',
            ExpressionAttributeValues={
                ':d': {'N': str(curday)},
                ':t': {'N': time},
                ':topic': {'S' : input_topic}
            },
            FilterExpression='contains(topics,:topic)',
            ExpressionAttributeNames={'#da': 'day', '#ti': 'time'},
            ProjectionExpression='club_name',
        )
        speak_output = ""
        for club in data['Items'][:5]:
            speak_output += club['club_name']['S'] + ',\n'

        speak_output = speak_output[:len(speak_output)-2]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class BetweenTimeIntentHandler(AbstractRequestHandler):
    "Handler for BetweenTime Intent."
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("BetweenTime")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # get the slots value x from handler_input, top x club
        s = ask_utils.request_util.get_slot(handler_input, "timeone")
        time1 = ''.join(s.value.split(':'))
        s = ask_utils.request_util.get_slot(handler_input, "timetwo")
        time2 = ''.join(s.value.split(':'))
        curday = datetime.now().weekday() + 1
        if curday == 7:
            curday = 0
        data = client.query(
            IndexName= 'day-time-index',
            TableName='clubs',
            KeyConditionExpression='#da=:d AND #ti BETWEEN :t1 AND :t2',
            ExpressionAttributeValues={
                ':d': {'N': str(curday)},
                ':t1': {'N': time1},
                ':t2': {'N': time2},
            },
            ExpressionAttributeNames={'#da': 'day', '#ti': 'time'},
            ProjectionExpression='club_name',
        )
        speak_output = ""
        for club in data['Items'][:5]:
            speak_output += club['club_name']['S'] + ',\n'

        speak_output = speak_output[:len(speak_output)-2]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class BetweenTimeTopicIntentHandler(AbstractRequestHandler):
    "Handler for BetweenTimeTopic Intent."
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("BetweenTimeTopic")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # get the slots value x from handler_input, top x club
        s = ask_utils.request_util.get_slot(handler_input, "timeone")
        time1 = ''.join(s.value.split(':'))
        s = ask_utils.request_util.get_slot(handler_input, "timetwo")
        time2 = ''.join(s.value.split(':'))
        input_topic = ask_utils.request_util.get_slot(handler_input, "topic").value
        curday = datetime.now().weekday() + 1
        if curday == 7:
            curday = 0
        data = client.query(
            IndexName= 'day-time-index',
            TableName='clubs',
            KeyConditionExpression='#da=:d AND #ti BETWEEN :t1 AND :t2',
            ExpressionAttributeValues={
                ':d': {'N': str(curday)},
                ':t1': {'N': time1},
                ':t2': {'N': time2},
                ':topic': {'S' : input_topic}
            },
            ExpressionAttributeNames={'#da': 'day', '#ti': 'time'},
            FilterExpression='contains(topics,:topic)',
            ProjectionExpression='club_name',
        )
        speak_output = ""
        for club in data['Items'][:5]:
            speak_output += club['club_name']['S'] + ',\n'

        speak_output = speak_output[:len(speak_output)-2]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class TopicIntentHandler(AbstractRequestHandler):
    """Handler for Topic Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TopicIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        input_topic = ask_utils.request_util.get_slot(handler_input, "topic").value

        # Remap product
        if input_topic.lower() in topics_remapped:
            input_topic = topics_remapped[input_topic.lower()]

        data = client.scan(
            TableName='clubs',
            FilterExpression='contains(topics,:topic)',
            ExpressionAttributeValues={':topic': {
                'S': input_topic
                }},
            ProjectionExpression='club_name',
        )
        speak_output = ""
        for club in data['Items'][:5]:
            speak_output += club['club_name']['S'] + ',\n'

        speak_output = speak_output[:len(speak_output)-2]
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

        # EventsToday
class EventsTodayIntentHandler(AbstractRequestHandler):
    "Handler for EventsToday Intent."
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("EventsToday")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # get the slots value x from handler_input, top x club
        input_today = ask_utils.request_util.get_slot(handler_input, "today").value
        date = str(input_today)
        data = client.query(
            TableName='events',
            KeyConditionExpression='#d=:dateToday',
            ExpressionAttributeValues={
                ':dateToday': {'S': date},
            },
            ExpressionAttributeNames={'#d': 'date'},
        )
        speak_output = ""
        for club in data['Items'][:5]:
            timeInDigits = int(club['time']['N'])
            minutes = timeInDigits % 100
            hours = timeInDigits // 100
            timeOfDay = "am"
            if hours > 12:
                hours = hours - 12
                timeOfDay = "pm"
            
            if minutes < 10:
                minutes = "0" + str(minutes)

            timeStr = f'{hours}:{minutes}'
            
            speak_output += club['club']['S'] + ' meets at ' + timeStr + " " +timeOfDay + ',\n'
        
        speak_output = speak_output[:len(speak_output)-2]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
# added handlers
sb.add_request_handler(TopClubIntentHandler())
sb.add_request_handler(EventsIntentHandler())
sb.add_request_handler(MyInterestsIntentHandler())
sb.add_request_handler(InputInterestsIntentHandler())
sb.add_request_handler(DynamoTestIntentHandler())
sb.add_request_handler(BeforeTimeIntentHandler())
sb.add_request_handler(AfterTimeIntentHandler())
sb.add_request_handler(BetweenTimeIntentHandler())
sb.add_request_handler(TopicIntentHandler())
sb.add_request_handler(EventsTodayIntentHandler())
sb.add_request_handler(DescribeClubIntentHandler())
sb.add_request_handler(BeforeTimeTopicIntentHandler())
sb.add_request_handler(AfterTimeTopicIntentHandler())
sb.add_request_handler(BetweenTimeTopicIntentHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()