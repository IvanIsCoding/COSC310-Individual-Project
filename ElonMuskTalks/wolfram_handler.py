import os
import wolframalpha
import logging
import azure.functions as func


def handle_wolfram(query_result):
    """Returns the image with the answer from Wolfram"""
    logging.info(f"DEBUG: Wolfram")


    try:
        query_text = query_result["queryText"]

        app_id = os.getenv("WOLFRAM_APP_ID")
        client = wolframalpha.Client(app_id)

        res = client.query(query_text)

        imgUri = None

        # Search for image
        for pod in res.pods:
            for subpod in pod.subpods:
                if "img" in subpod:
                    # Found image in response from Wolfram, stop
                    imgUri = subpod["img"]["@src"]
                    break
            
            if imgUri is not None:
                break

        return {
        "fulfillmentMessages": [
            {"card": {"title": "Elon Did the Math","imageUri": imgUri,}}
            ]
        }

    except Exception as e:

        return {
            "fulfillmentMessages": [
                {"text": {"text": ["My engineers are working on this right now - thanks for talking to Elon Musk Bot"]}}
            ]
        }
