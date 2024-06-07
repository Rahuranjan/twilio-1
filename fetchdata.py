import requests
import json
# headers = {'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=560064&date=07-02-2021"
urls = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=140&date=06-05-2021"
headers = {'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

data = requests.get(url)
print(data.text)

def get_data(pin, date):
    r = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+pin+"&date="+date+"")
    data  = r.json()
    check = r.text
    if 'Invalid Pincode' in check:
        return "Invalid Pincode"
    else:
        centers = data['centers']
        if(len(centers)>0):
            data_all =[]
            for center in centers:
                sessions = center["sessions"]
                for session in sessions:
                    data_all.append({"center_name": center["name"], "center_address": center["address"], "vaccine": session["vaccine"], "slots": session["slots"], "date": session["date"], "available_capacity": session["available_capacity"]})
            return data_all
        else:
            return ("No centers available")