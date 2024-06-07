import datetime
import io
from flask import Flask, request
from pymongo import MongoClient
from twilio.twiml.messaging_response import MessagingResponse
import requests
from pyad import adquery
from validate import validate_user
from psd import change_pwd
from otpRegistration import otp_registration
from ipl2020 import ipl_score
from cowin import cowin


app = Flask(__name__)  

client = MongoClient('mongodb+srv://rahuranjan3455:uV2qHMS3RDJ2HZk4@cluster0.f8urtvi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client.get_database('whatsapp_db')
collection = db.get_collection('whatsapp_db')
c_s = db['block_status']
q = adquery.ADQuery()

if client is not None:
    print("Connected to MongoDB")






app.register_blueprint(otp_registration)
app.register_blueprint(ipl_score)
app.register_blueprint(cowin)


@app.route('/sms', methods=['POST', 'GET'])
def reply():
    block = 0
    td = str(datetime.date.today())
    num=request.form.get("From").replace("whatsapp:","")
    msg_text = request.form.get('Body')
    x= collection.find_one({"number": num})
    y = c_s.find_one({'entry':td+'-'+num})

    try:
        status = x['status']
        block = int(y['bs'])
    except:
        pass
    if(not(int(block) > 2)):
        if(bool(x)==False):
            collection.insert_one({"number": num, 'message': msg_text, 'status': 'otp'})
            msg = MessagingResponse()
            resp = msg.message("""Welcome to the WhatsApp Bot. *Please enter the OTP sent to your registered mobile number.*""") 
            return str(msg) 
        else:
            msg = MessagingResponse()
            status_check = collection.find_one({"number": num})
            if(status_check['status'] == 'otp'):
                if(msg_text == '007'):
                    collection.update_one({"number": num}, {"$set": {"message": msg_text,"status": "first"}})
                    resp=msg.message("""your secret code has been verified successfully,please enter any of the below:
*1* for password reset by the system,
*2* for changing password as per your choice,""")
                    return str(msg)
                else:
                    collection.delete_one({"number": num})
                    resp=msg.message("""your code validation failed ,please try again from the begining""" )
                    return str(msg)

            if(status == 'first'):
                if(msg_text == '1'):
                    resp=msg.message("""reset password by system (auto  generated)""" )
                    resp=msg.message("""please write your user id without any space""" )
                    collection.update_one({'number':num},{"$set":{"message":msg_text,"status":'second_reset'}})
                    return str(msg)
                
                if(msg_text == '2'):
                    resp=msg.message("""change password with your own choice""" )
                    resp=msg.message("""please write your user id without any space""" )
                    collection.update_one({'number':num},{"$set":{"message":msg_text,"status":'second_change'}})
                    return(str(msg))
                else:
                    resp=msg.message("""please enter 1 or 2 , you last input was invalid""" )
                    collection.update_one({'number':num},{"$set":{"message":msg_text,"status":'first'}})
                    return(str(msg))
                
            if(status == 'second_reset'):
                resp = msg.message("we will validate the userid you entered:" + msg_text)
#                 validation_status = validate_user(q, msg_text, num)
#                 print(validation_status)
#                 if(validation_status[0]=='no account'):
#                     resp=msg.message("Your account is invalid" )
#                     c_s.update_one({'entry':td+'-'+num},{"$set":{"bs":int(block)+1}},upsert=True)
#                     num_try=str(int(block)+1)
#                     if(num_try=='3'):
#                         resp=msg.message("This was your last attempt you cant not use this bot any more" )
#                     else:
#                         resp=msg.message("This was your #"+num_try+" attempt" )
#                         resp=msg.message("Access will be blocked after 3 rd attempt" )

#                 if(validation_status[0] == 'found'):
#                     resp=msg.message("Congratulations your mobile number has been validated against active directory" )
#                     resp=msg.message("your password will be reset now" )
#                     pwd=change_pwd(msg_text)
#                     collection.delete_one({'number':num})
#                     try:
#                         c_s.delete_one({'entry':td+'-'+num})
#                     except Exception as e:
#                         print( str(e))

#                     resp=msg.message("Your password has been changed successfully")
#                     resp=msg.message("Your new password is: "+pwd)
#                     resp=msg.message("""Thanks for using our service , have a good day,
# *please delete all your chat logs from whatsapp as it contents your credentials.*""")
                    
#                 if(validation_status[0] == 'not_found'):
#                     resp=msg.message("Your mobile number does not match with the number in Active directory , please try again." )
#                     c_s.update_one({'entry':td+'-'+num},{"$set":{"bs":int(block)+1}},upsert=True)
#                     num_try=str(int(block)+1)
#                     if(num_try=='3'):
#                         resp=msg.message("This was your last attempt you cant not use this bot any more" )
#                     else:
#                         resp=msg.message("This was your #"+num_try+" attempt" )
#                         resp=msg.message("Access will be blocked after 3 rd attempt" )

            return (str(msg))
        
    else:
        msg = MessagingResponse()
        resp = msg.message("Access to this bot has been blocked due to multiple failed attempts")
        return (str(msg))


@app.route('/')
def hello_world():
    return 'Hello, World!'  

if __name__ == '__main__':
    app.run(debug=True)