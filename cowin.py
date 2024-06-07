from flask import request, Blueprint
from pymongo import MongoClient
from twilio.twiml.messaging_response import MessagingResponse
import json
from fetchdata import get_data

cowin = Blueprint('cowin', __name__)
                        

client = MongoClient('mongodb+srv://rahuranjan3455:0UPFaEeMReCadOEA@cluster0.nad1xtf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.get_database('cowin')
collection = db.get_collection('cowin')

@cowin.route('/cowin', methods=['POST', 'GET'])
def vaccine():
    num=request.form.get("From").replace("whatsapp:","")
    print(num)
    msg_text=request.form.get("Body")
    if "," in msg_text:
        pin = msg_text.split(",")[0]
        date = msg_text.split(",")[1]
        x=collection.find_one({"NUMBER":num})
        try:
            status=x["status"]
        except:
            pass

        if (bool(x)==False):
            collection.insert_one({"NUMBER":num,"status":"first"})
            msg=MessagingResponse()
            resp = msg.message("""Hello this is T2 from total technology, developed by gov. , to get covid vaccine availability related information please follow the below  
                    enter your pincode and date separated comma , for example if your pincode is 110045 and date you want for 15th may 2021,  then yourinput should be 110045,15-05-2021 """)
            return (str(msg))
        else:
            if(status == 'first'):
                data = get_data(pin, date)
                msg = MessagingResponse()

                if (data == "Invalid Pincode"):
                    resp = msg.message("Please enter valid Pincode")
                    return (str(msg))
                elif (data == "No centers available"):
                    resp = msg.message("No centers available for the given pincode and date, please try again with different pincode and date")
                    return (str(msg))
                else:
                    if(len(data) < 15):
                    
                        parse_data = json.dumps(data)
                        parse_data = parse_data.replace("{", "")
                        parse_data = parse_data.replace("}", "\n\n")
                        parse_data = parse_data.replace("[", "")
                        parse_data = parse_data.replace("]", "")
                        parse_data = parse_data.replace(",", "\n")
                        resp = msg.message(parse_data)
                        print(parse_data)
                        return (str(msg))
                    else:
                        resp1 = msg.message("please find the pdf for more information")
                        resp1.media("https://www.cowin.gov.in/")
                        return (str(msg))  
    
    else:
        msg=MessagingResponse()
        resp = msg.message("""Invalid input, developed by gov. , to get covid vaccine availability related information please follow the below  
                    enter your pincode and date separated comma , for example if your pincode is 110045 and date you want for 15th may 2021,  then yourinput should be 110045,15-05-2021 """)
        return (str(msg))
    print(num)
        