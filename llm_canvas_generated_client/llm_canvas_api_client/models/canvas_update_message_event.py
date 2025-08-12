from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.message_node import MessageNode


T = TypeVar("T", bound="CanvasUpdateMessageEvent")


@_attrs_define
class CanvasUpdateMessageEvent:
    """Event data for canvas message updates.

    Attributes:
        event_type (Literal['update_message']):
        canvas_id (str):
        timestamp (float):
        data (MessageNode): Node in the canvas conversation graph.
    """

    event_type: Literal["update_message"]
    canvas_id: str
    timestamp: float
    data: "MessageNode"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        event_type = self.event_type

        canvas_id = self.canvas_id

        timestamp = self.timestamp

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_type": event_type,
                "canvas_id": canvas_id,
                "timestamp": timestamp,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message_node import MessageNode

        d = dict(src_dict)
        event_type = cast(Literal["update_message"], d.pop("event_type"))
        if event_type != "update_message":
            raise ValueError(f"event_type must match const 'update_message', got '{event_type}'")

        canvas_id = d.pop("canvas_id")

        timestamp = d.pop("timestamp")

        data = MessageNode.from_dict(d.pop("data"))

        canvas_update_message_event = cls(
            event_type=event_type,
            canvas_id=canvas_id,
            timestamp=timestamp,
            data=data,
        )

        canvas_update_message_event.additional_properties = d
        return canvas_update_message_event

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
