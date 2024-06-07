import pyad
from pyad import adquery
from password_generator import PasswordGenerator
import pyad.adquery
import pyad.aduser

def change_pwd(msg_text):

    q = pyad.adquery.ADQuery()
    q.execute_query(attributes=['distinguishedname', 'mobile', 'cn'], where_clause="sAMAccountName='rahuranjan3455'".format(msg_text))  
    x = bool(q.get_results())
    if(str(x) == 'True'):
        for row in q.get_results():
            cn = row['distiguishedname']

    aduser = pyad.aduser.ADUser.from_cn(cn)
    pwo = PasswordGenerator()
    pwd = 'Tt' + pwo.generate()
    pyad.aduser.set_password(aduser, pwd)
    return (pwd)
    