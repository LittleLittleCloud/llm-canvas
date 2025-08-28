from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.sse_message_deleted_event_data import SSEMessageDeletedEventData


T = TypeVar("T", bound="SSEMessageDeletedEvent")


@_attrs_define
class SSEMessageDeletedEvent:
    """SSE event data for message deletion.

    Attributes:
        type_ (Literal['message_deleted']):
        timestamp (float):
        canvas_id (str):
        data (SSEMessageDeletedEventData): Data payload for message deleted events.
    """

    type_: Literal["message_deleted"]
    timestamp: float
    canvas_id: str
    data: "SSEMessageDeletedEventData"
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
        from ..models.sse_message_deleted_event_data import SSEMessageDeletedEventData

        d = dict(src_dict)
        type_ = cast(Literal["message_deleted"], d.pop("type"))
        if type_ != "message_deleted":
            raise ValueError(f"type must match const 'message_deleted', got '{type_}'")

        timestamp = d.pop("timestamp")

        canvas_id = d.pop("canvas_id")

        data = SSEMessageDeletedEventData.from_dict(d.pop("data"))

        sse_message_deleted_event = cls(
            type_=type_,
            timestamp=timestamp,
            canvas_id=canvas_id,
            data=data,
        )

        sse_message_deleted_event.additional_properties = d
        return sse_message_deleted_event

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
