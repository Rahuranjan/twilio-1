from flask import request, Blueprint
from pymongo import MongoClient
from twilio.twiml.messaging_response import MessagingResponse
from pycricbuzz import Cricbuzz
import json

ipl_score = Blueprint('ipl_score', __name__)

client = MongoClient('mongodb+srv://rahuranjan3455:uV2qHMS3RDJ2HZk4@cluster0.f8urtvi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.get_database('IPL2020')
collection = db.get_collection('ipl2020')


@ipl_score.route('/ipl_score', methods=['POST', 'GET'])
def score():
    num=request.form.get("From").replace("whatsapp:","")
    print(num)
    msg_text=request.form.get("Body")
    x=collection.find_one({"NUMBER":num})
    try:
        status=x["status"]
    except:
        pass

    if (bool(x)==False):
        collection.insert_one({"NUMBER":num,"status":"first"})
        msg=MessagingResponse()
        resp=msg.message("""Hello & welcome ,myself *T2 FROM TOTAL TECHNOLOGY* ,a bot for knowing live score updates for ipl matches.
please read and select from the below options:
enter *1* to get live score for an ongoing match,
enter *2* to get sull score updates for an ongoing match,
enter *3* to get complete match information for an ongoing match.
""")
        return str(msg)
    
    else:
        if(status == 'first'):
            msg = MessagingResponse()
            if(msg_text == '1'):
                c = Cricbuzz()
                print(c)
                matches = c.matches()
                print(matches)
                match_data = []
                for match in matches :
                    if match["srs"]=="Indian Premier League 2020" and not(match["mchstate"]=="preview"):
                        match_data.append(match)
                    if(len(match_data) == 1):
                        match_id = match_data[0]["id"]
                    livescore = c.livescore(mid=match_id)
                    livescore = json.dumps(livescore)
                    return (str(msg))

            else:
                resp=msg.message("""Sorry you have entered invalid option.
please read and select from the below options:
enter *1* to get live score for an ongoing match,
enter *2* to get sull score updates for an ongoing match,
enter *3* to get complete match information for an ongoing match.
""")
                return (str(msg))

