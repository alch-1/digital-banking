import functions

def loginCustomer():

   OTP = '999999',

   PIN = '877324',

   serviceName = 'loginCustomer',

   userID = '01332738'



   headerObj = {

                    'Header': {

                    'serviceName': serviceName,

                    'userID': userID,

                    'PIN': PIN,

                    'OTP': OTP

                    }

                }



   final_url="{0}?Header={1}".format(url(),json.dumps(headerObj))

   response = requests.post(final_url)



   serviceRespHeader = response.json()['Content']['ServiceResponse']['ServiceRespHeader']

   errorCode = serviceRespHeader['GlobalErrorID']



   if errorCode == '010000':

       LoginOTPAuthenticateResponseObj = response.json()['Content']['ServiceResponse']['Login_OTP_Authenticate-Response']

       print('CustomerID: {}'.format(LoginOTPAuthenticateResponseObj['CustomerID']))

       print('BankID: {}'.format(LoginOTPAuthenticateResponseObj['BankID']))



   elif errorCode == '010041':

       print("OTP has expired.\nYou will receiving a SMS")



   else:

       print(serviceRespHeader['ErrorText'])



loginCustomer()