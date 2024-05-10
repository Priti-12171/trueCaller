
from rest_framework import viewsets
from spam.models import RegisteredUser,Contacts, ContactList
from spam.serializers import ContactsSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import jwt, datetime 
from rest_framework.views import exceptions



# Registration API
class Register(APIView):
  def post(self,request):
    if request.data.get("user") is None or request.data.get("phone_no") is None:
      return Response(
        {
          "Error":"Something went wrong"
        },
        status = status.HTTP_400_BAD_REQUEST
      )
    user=RegisteredUser(
      user=request.data["user"],
      phone_no=request.data["phone_no"],
      password=request.data["password"]
    )
    user.save()
    return Response(
      {
        "Message":"Successfully",
        "token": generateToken(user=user)
      }
    )
  
  
  ##Login API
class Login(APIView):
  def post(self,request):
    if request.data.get("user") is None or request.data.get("password") is None:
      return Response(
        {
          "error":"Invalid Credential"
        },
        status=status.HTTP_400_BAD_REQUEST
      )
    user = request.data.get("user")
    user = RegisteredUser.objects.filter(user=user).first()
    return Response(
        {
          "token": generateToken(user=user)
        },
        status=status.HTTP_200_OK
      )
  

 ### API for not registered user   
class Contact(APIView):
  def post(self,request):
    if request.data.get("name") is None or request.data.get("phone_no") is None:
      return Response(
        {
          "Error":"Something went wrong"
        },
        status = status.HTTP_400_BAD_REQUEST
      )
    user=Contacts(
      name=request.data["name"],
      phone_no=request.data["phone_no"],
      spam=request.data["spam"]
    )
    if user:
      user.save()
    return Response(
      {
        "Message":"Successfully"
      }
    )
  

#Spam Mark API
class SpamUpdation(APIView):
  def get(self,request):
    phone_no=request.data.get("phone_no") 
    if phone_no is None:
      return Response(
        {
          "Error":"phone_no is required"
        },
        status = status.HTTP_400_BAD_REQUEST
      )
    contacts=Contacts.objects.filter(phone_no=phone_no).update(spam=True)
    registeredUser=RegisteredUser.objects.filter(phone_no=phone_no).update(spam=True)
    if(contacts+registeredUser):
      return Response(
        {
          "message":"marked as spam"
        },
        status=status.HTTP_200_OK
      )
    else:
      return Response(
        {
          "error":"phone number does not exist"
        },
        status = status.HTTP_400_BAD_REQUEST
      )

		 
#user can search by name 
class SearchByName(APIView):
  def get(self,request):
    validateToken(request.headers.get("token"))
    
    user=request.data.get("user") 
    if user is None:
      return Response(
        {
          "Error":"user is required"
        },
        status = status.HTTP_400_BAD_REQUEST
      )
    registeredUser_start= RegisteredUser.objects.filter(user__startswith=user)
    registeredUser_contain = RegisteredUser.objects.filter(user__contains=user).exclude(user__startswith=user)
    contacts_start= Contacts.objects.filter(name__startswith=user)
    contacts_contain = Contacts.objects.filter(name__contains=user).exclude(name__startswith=user)
    

    response=[]
    for contact in registeredUser_start:
      response.append(
        {
        "user":contact.user,
        "phone_no":contact.phone_no,
        "spam":contact.spam,
        }
      )
      for contact in registeredUser_contain:
        response.append(
        {
        "user":contact.user,
        "phone_no":contact.phone_no,
        "spam":contact.spam,
        }
      )
      for contact in contacts_start:
         response.append(
        {
        "user":contact.name,
        "phone_no":contact.phone_no,
        "spam":contact.spam,
        }
      )
      for contact in contacts_contain:
         response.append(
        {
        "user":contact.name,
        "phone_no":contact.phone_no,
        "spam":contact.spam,
        }
      )
    
    return Response(
        {
          "Message":response
        },
        status = status.HTTP_400_BAD_REQUEST
      )
  

##user can search by number
class SearchByNumber(APIView):
  def get(self,request):
    validateToken(request.headers.get("token"))
    phone_no=request.data.get("phone_no") 
    if phone_no is None:
      return Response(
        {
          "Error":"phone_no is required"
        },
        status = status.HTTP_400_BAD_REQUEST
      )
    registeredUser=RegisteredUser.objects.filter(phone_no=phone_no)
    response=[]
    for contact in registeredUser:
      response.append(
        {
        "user":contact.user,
        "phone_no":contact.phone_no,
        "spam":contact.spam,
        }
      )
    else:
      contacts=Contacts.objects.filter(phone_no=phone_no)
    
      for contact in contacts:
        response.append(
          {
            "name":contact.name,
            "phone_no":contact.phone_no,
            "spam":contact.spam
          }
        )
      
      return Response(
          {
            "message":response
          },
          status= status.HTTP_200_OK
        )
        


##search result API
class SearchResult(APIView):
  def get(self,request):
      if request.data.get("phone_no") is None or request.data.get("userId") is None:
        return Response(
          {
          "Error":"phone_no is required"
          },
        status = status.HTTP_400_BAD_REQUEST
      )
      phone_no = request.data.get("phone_no")
      userId = request.data.get("userId")
      registeredUser=RegisteredUser.objects.filter(phone_no=phone_no)
      contactList = ContactList.objects.filter(phone_no=phone_no, userId=userId)
      
      if(registeredUser is not None):
          email = ""
          if len(contactList) > 0:
           print(registeredUser)
           email = registeredUser[0].email
          return Response(
          {
           "name": registeredUser[0].user,
           "email": email
          },
           status = status.HTTP_400_BAD_REQUEST
           )
      

  ## function to generate a token   
def generateToken(user):
    payload = {
      'id': user.user,
      'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
      'iat':  datetime.datetime.now()
    }
    return jwt.encode(payload, 'secret', algorithm='HS256')


##function to validate the token
def validateToken(token):
    if token is None:
      raise Exception("Sorry, no numbers below zero")
    try:
      payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except:
      raise Exception("Invalid token")
    user = RegisteredUser.objects.filter(user=payload['id']).first()
    if user is None:
      raise Exception("User not present")

    
      

  
  
    

 
    







