import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "84308277-4399-4388-9027-e232d50f66f7")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_ID = os.environ.get("LuisAppId", "996f0114-349e-4be5-92e4-72a5ec648bb6")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "d92fa31268ef4f65971cb74ae70576c8")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "australiaeast.api.cognitive.microsoft.com")
