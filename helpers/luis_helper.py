from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

# from booking_details import BookingDetails


class Intent(Enum):
    EmployeeCode = "Employee-code"
    Roster = "Roster"
    FlightBookings = "Flight-Bookings"
    Stay = "Stay"
    Transportation = "Transportation"
    NONE_INTENT = "None"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> tuple[Intent, object]:
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )

            if intent == Intent.EmployeeCode.value:
                # result = BookingDetails()

                # We need to get the result from the LUIS JSON which at every level returns an array.
                empId = recognizer_result.entities.get("$instance", {}).get(
                    "Employee-id", []
                )
                if len(empId) > 0:
                    result = empId[0]["text"].capitalize()
                else:
                    result = "Invalid employee id"

            if intent == Intent.Roster.value:
                rosterB = recognizer_result.intents.get("$instance", {}).get(
                    "Roster_e", []
                )
                if len(rosterB) > 0:
                    result = rosterB[0]["text"].capitalize()
                else:
                    result = "Invalid Query"

            if intent == Intent.FlightBookings.value:
                flightB = recognizer_result.intents.get("$instance", {}).get(
                    "Flight-Bookings", []
                )
                if len(flightB) > 0:
                    result = flightB[0]["text"].capitalize()
                else:
                    result = "Invalid Query"
                
            if intent == Intent.Stay.value:
                stayB = recognizer_result.intents.get("$instance", {}).get(
                    "Stay", []
                )
                if len(stayB) > 0:
                    result = stayB[0]["text"].capitalize()
                else:
                    result = "Invalid Query"
            
            if intent == Intent.Transportation.value:
                transportationB = recognizer_result.intents.get("$instance", {}).get(
                    "Transporataion", []
                )
                if len(transportationB) > 0:
                    result = transportationB[0]["text"].capitalize()
                else:
                    result = "Invalid Query"

            if intent == Intent.NONE_INTENT.value:
                noneB = recognizer_result.intents.get("$instance", {}).get(
                    "None", []
                )
                if len(noneB) > 0:
                    result = noneB[0]["text"].capitalize()
                else:
                    result = "Invalid Query"



                # This value will be a TIMEX. And we are only interested in a Date so grab the first result and drop
                # the Time part. TIMEX is a format that represents DateTime expressions that include some ambiguity.
                # e.g. missing a Year.
                # date_entities = recognizer_result.entities.get("datetime", [])
                # if date_entities:
                #     timex = date_entities[0]["timex"]

                #     if timex:
                #         datetime = timex[0].split("T")[0]

                #         result.travel_date = datetime

                # else:
                #     result.travel_date = None

        except Exception as exception:
            print(exception)

        return intent, result
