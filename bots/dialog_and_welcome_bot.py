# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import os.path

from typing import List
from botbuilder.core import (
    ConversationState,
    MessageFactory,
    UserState,
    TurnContext,
)
from botbuilder.dialogs import Dialog
from botbuilder.schema import Attachment, ChannelAccount
from helpers.dialog_helper import DialogHelper

from .dialog_bot import DialogBot
from booking_recognizer import BookingRecognizer


class DialogAndWelcomeBot(DialogBot):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        luis_recognizer: BookingRecognizer
    ):
        super(DialogAndWelcomeBot, self).__init__(
            conversation_state, user_state, luis_recognizer
        )

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Please enter your IGA Code!")
