from ast import arg
from urllib import response
from urllib.request import urlopen
from webbrowser import get
from botbuilder.core import ActivityHandler, ConversationState, UserState, TurnContext, MessageFactory
from botbuilder.dialogs import Dialog
from helpers.dialog_helper import DialogHelper
from helpers.luis_helper import LuisHelper, Intent
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions
from booking_recognizer import BookingRecognizer
from helpers.luis_helper import LuisHelper, Intent
from unittest import case

# url = "https://api.spacexdata.com/v4/capsules"
# f = urlopen(url)
# myfile = f.read()


# url = 'https://www.w3schools.com/python/demopage.php'
# myobj = {'Employee id': 'emp_id'}

# myfile = requests.post(url, json = myobj)

class DialogBot(ActivityHandler):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        luis_recognizer: BookingRecognizer
    ):

        if conversation_state is None:
            raise Exception(
                "[DialogBot]: Missing parameter. conversation_state is required"
            )
        if user_state is None:
            raise Exception("[DialogBot]: Missing parameter. user_state is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        self._luis_recognizer = luis_recognizer

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have occurred during the turn.
        await self.conversation_state.save_changes(turn_context, False)
        await self.user_state.save_changes(turn_context, False)


    async def on_message_activity(self, turn_context: TurnContext):
        await self.on_list_select(turn_context)
        return await self._send_suggested_actions(turn_context)

    async def on_list_select(self, turn_context: TurnContext):
        if turn_context.activity.text.lower() == "flight details":
            # call flight details api
            await turn_context.send_activity("Flight details found!")

        elif turn_context.activity.text.lower() == "transport details":
            # call transport details api
            await turn_context.send_activity("Transport details found!")

        elif turn_context.activity.text.lower() == "hotel details":
            # call hotel details api
            await turn_context.send_activity("Hotel details found!")

        elif turn_context.activity.text.lower() == "roster details":
            # call hotel details api
            await turn_context.send_activity("Roster details found!")

        else:
            # call LUIS
            await self.call_luis(turn_context)

    async def call_luis(self, turn_context: TurnContext):
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, turn_context
        )

        if intent == Intent.EmployeeCode.value and luis_result:
            #turn_context.values["empId"] = luis_result
            emp_id = luis_result
            await turn_context.send_activity(f"Hello {emp_id}")

        elif intent == Intent.Roster.value and luis_result:  
            roster_b = intent
            await turn_context.send_activity("Here is your Roster details...")

        elif intent == Intent.FlightBookings.value and luis_result:  
            flight_b = intent
            await turn_context.send_activity("Here is your flight details...")
        
        elif intent == Intent.Stay.value and luis_result:  
            stay_b = intent
            await turn_context.send_activity("Here is your Hotel details...")

        elif intent == Intent.Transportation.value and luis_result:  
            transport_b = intent
            await turn_context.send_activity("Here is your Cab details...")
        else:     
            await turn_context.send_activity("Can't understand what you are trying to say...")
       
    
    async def _send_suggested_actions(self, turn_context: TurnContext):
        reply = MessageFactory.text("Please select from the below options")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Flight Details",
                    type=ActionTypes.im_back,
                    value="Flight Details",
                ),
                CardAction(
                    title="Transport Details",
                    type=ActionTypes.im_back,
                    value="Transport Details",
                ),
                CardAction(
                    title="Hotel Details",
                    type=ActionTypes.im_back,
                    value="Hotel Details",
                ),
                CardAction(
                    title="Roster Details",
                    type=ActionTypes.im_back,
                    value="Roster Details",
                ),
            ]
        )

        return await turn_context.send_activity(reply)