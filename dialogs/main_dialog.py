# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from asyncio.base_futures import _FINISHED
from unittest import result
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)

from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, TurnContext, ConversationState, CardFactory
from botbuilder.schema import InputHints, SuggestedActions, CardAction, ActionTypes

from booking_recognizer import BookingRecognizer
from helpers.luis_helper import LuisHelper, Intent


class MainDialog(ComponentDialog):
    def __init__(
        self, luis_recognizer: BookingRecognizer
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self._luis_recognizer = luis_recognizer

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.intro_step, self.act_step, self.act2_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )

            return await step_context.next(None)
        message_text = "Please enter your IGA Code!"
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Call LUIS and gather any potential booking details. (Note the TurnContext has the response to the prompt.)
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )

        if intent == Intent.EmployeeCode.value and luis_result:
            step_context.values["empId"] = luis_result
            emp_id = step_context.values["empId"]
            message_text = f"How may I assist you {emp_id}?"
            prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )
        else:
            return await step_context.replace_dialog(self.id)

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def act2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )
        prompt_message = None
        if intent == Intent.FlightBookings.value and luis_result:  
            step_context.values["flightb"] = luis_result
            flight_b = step_context.values["flightb"]     
            message_text = "Here is your Flight details..."
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
        
        elif intent == Intent.Stay.value and luis_result:  
            step_context.values["stayb"] = luis_result
            stay_b = step_context.values["stayb"]     
            message_text = "Here is your Hotel details..."
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)

        elif intent == Intent.Transportation.value and luis_result:  
            step_context.values["transportb"] = luis_result 
            transport_b = step_context.values["transportb"]     
            message_text = "Here is your Cab details..."
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)

        else:     
            message_text = "Please try something else!"
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.ignoring_input)
            return await step_context.replace_dialog(self.act_step)

        return await step_context.prompt(TextPrompt.__name__,PromptOptions(prompt=prompt_message))

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result is not None:
            result = step_context.result
            message_text = "Thanks for using this bot!"
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)            
        
        return await step_context.prompt(TextPrompt.__name__,PromptOptions(prompt=prompt_message))
        
        

        

    