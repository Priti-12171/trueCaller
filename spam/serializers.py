from rest_framework import serializers
from spam.models import RegisteredUser,Contacts,ContactList



class ContactsSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model=Contacts,ContactList
    fields="__all__"