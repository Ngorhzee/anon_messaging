from shared.serializers import Serializer
from shared.serializers.resolvers import RELATED_QUERYSET_RESOLVER


class RoomSerialiser(Serializer):
    name = Serializer.field()
    id = Serializer.field()
    messages = Serializer.extended("MessageSerializer", many=True, resolver=RELATED_QUERYSET_RESOLVER)
    date_created = Serializer.field()

class MessageSerializer(Serializer):
    id = Serializer.field()
    content = Serializer.field()
    device_id = Serializer.field()
    date_created = Serializer.field()
    
