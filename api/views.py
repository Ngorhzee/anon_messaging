from rest_framework.request import Request
from rest_framework.response import Response
from shared.view_tools.paths import Api
from .models import ChatRoom,Messages
from shared.view_tools.exceptions import ApiException, ResourceNotFound
from .sr import MessageSerializer, RoomSerialiser
from shared.view_tools import body_tools
from uuid import UUID
import typing
import pydantic
from rest_framework import status

api = Api()



@api.endpoint("create-room", method="POST")
def createRoom(request: Request):
    body = typing.cast(dict, request.data)
    name = body.get("name")
    room = ChatRoom.objects.create(name=name)
    sr = RoomSerialiser(room,request)
    return Response(sr())

class ValidateMessageInput(pydantic.BaseModel):
    content: str
    device_id: UUID
    chatroom_id: UUID

@api.endpoint("get-messages/<code>", method="GET")
def getmessages(request: Request, code: str):
    query_param = typing.cast(dict, request.query_params)
    param_from = query_param.get("from")

    try:
        UUID(code)
    except ValueError:
        raise ApiException("Invalid Chatroom code")
    try:
        room = ChatRoom.objects.get(id=code)
    
    except ChatRoom.DoesNotExist:
        raise ResourceNotFound("Chatroom does not exist")
    if param_from is None:
       messages = room.messages.all() # type: ignore
    else: 
       messages = room.messages.filter(date_created__gte= param_from) # type: ignore

    sr = [MessageSerializer(message, request)() for message in messages]
    return Response(sr)

    

@api.endpoint("post-messages", method="POST")
@body_tools.validate(ValidateMessageInput)
def postmessages(request: Request,):
    data: ValidateMessageInput = body_tools.get_validated_body(request)
   
    try:
        room = ChatRoom.objects.get(id=data.chatroom_id)
    
    except ChatRoom.DoesNotExist:
        raise ResourceNotFound("Chatroom does not exist")
    
    message = Messages.objects.create(chatroom=room, content=data.content, device_id=data.device_id),

    return Response(status=status.HTTP_204_NO_CONTENT)
        





