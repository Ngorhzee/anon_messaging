from rest_framework.request import Request
from rest_framework.response import Response
from shared.view_tools.paths import Api
from .models import ChatRoom,Messages
from shared.view_tools.exceptions import ApiException, ResourceNotFound
from .sr import MessageSerializer, RoomSerialiser
from shared.view_tools import body_tools
from uuid import UUID
import pydantic

api = Api()



@api.endpoint("createroom", method="POST")
def createRoom(request: Request):
    room = ChatRoom.objects.create()
    sr = RoomSerialiser(room,request)
    return Response(sr())

class ValidateMessageInput(pydantic.BaseModel):
    content: str
    device_id: UUID

@api.endpoint("getmessages/<code>", method="GET")
def getmessages(request: Request, code: str):
    try:
        UUID(code)
    except ValueError:
        raise ApiException("Invalid Chatroom code")
    try:
        room = ChatRoom.objects.get(id=code)
    
    except ChatRoom.DoesNotExist:
        raise ResourceNotFound("Chatroom does not exist")
    
    messages = room.messages.all() # type: ignore
    sr = [MessageSerializer(message, request)() for message in messages]
    return Response(sr)
    

@api.endpoint("postmessages/<code>", method="POST")
@body_tools.validate(ValidateMessageInput)
def postmessages(request: Request, code: str):
    data: ValidateMessageInput = body_tools.get_validated_body(request)
    try:
        UUID(code)
    except ValueError:
        raise ApiException("Invalid Chatroom code")
    try:
        room = ChatRoom.objects.get(id=code)
    
    except ChatRoom.DoesNotExist:
        raise ResourceNotFound("Chatroom does not exist")
    
    message = Messages.objects.create(chatroom=room, content=data.content, device_id=data.device_id),

    return Response()
        





