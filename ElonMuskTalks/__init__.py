import logging
import azure.functions as func
import json

from .intent_handlers import *

import random

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        request_json = req.get_json()
        logging.info(f"DEBUG: {request_json}")
    except:
        return func.HttpResponse("First try-except failed")
    
    intent_dictionary = {
        "What Company Does Intent": handle_what_company_intent,
        "Work at SpaceX Intent - custom": handle_WorkatSpaceXIntent_followup,
        "Crypto Advice Intent": handle_crypto_advice_intent,
        "What is Crypto Intent": handle_what_is_crypto_intent,
        "Billionaire Tax Intent": handle_billionaire_tax_intent,
        "Daily Routine Intent": handle_daily_routine_intent,
        "Neuralink Applications Intent - custom": handle_NeuralinkAppIntent_followup,
        "Fight Putin Intent": handle_fight_putin_intent,
        "Stand With Ukraine Intent": handle_stand_with_ukraine_intent,
    }

    try:
        query_result = request_json["queryResult"]
        user_intent = query_result["intent"]["displayName"]

        if user_intent in intent_dictionary:
            answer_list = intent_dictionary[user_intent](query_result)
        else:
            answer_list = ["My engineers are working on this right now - thanks for talking to Elon Musk Bot"]
    except:
        answer_list = ["My engineers are working on this right now - thanks for talking to Elon Musk Bot"]

    answer = {
      "fulfillmentMessages": [
        {"text": {"text": answer_list}}
      ]
    }

    return func.HttpResponse(json.dumps(answer))
