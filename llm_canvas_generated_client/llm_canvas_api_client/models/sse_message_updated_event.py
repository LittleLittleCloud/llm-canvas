from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.message_node import MessageNode


T = TypeVar("T", bound="SSEMessageUpdatedEvent")


@_attrs_define
class SSEMessageUpdatedEvent:
    """SSE event data for message updates.

    Attributes:
        type_ (Literal['message_updated']):
        timestamp (float):
        canvas_id (str):
        data (MessageNode): Node in the canvas conversation graph.
    """

    type_: Literal["message_updated"]
    timestamp: float
    canvas_id: str
    data: "MessageNode"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        timestamp = self.timestamp

        canvas_id = self.canvas_id

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "timestamp": timestamp,
                "canvas_id": canvas_id,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message_node import MessageNode

        d = dict(src_dict)
        type_ = cast(Literal["message_updated"], d.pop("type"))
        if type_ != "message_updated":
            raise ValueError(f"type must match const 'message_updated', got '{type_}'")

        timestamp = d.pop("timestamp")

        canvas_id = d.pop("canvas_id")

        data = MessageNode.from_dict(d.pop("data"))

        sse_message_updated_event = cls(
            type_=type_,
            timestamp=timestamp,
            canvas_id=canvas_id,
            data=data,
        )

        sse_message_updated_event.additional_properties = d
        return sse_message_updated_event

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
