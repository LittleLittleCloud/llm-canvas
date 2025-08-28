from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.sse_canvas_deleted_event_data import SSECanvasDeletedEventData


T = TypeVar("T", bound="SSECanvasDeletedEvent")


@_attrs_define
class SSECanvasDeletedEvent:
    """SSE event data for canvas deletion.

    Attributes:
        type_ (Literal['canvas_deleted']):
        timestamp (float):
        data (SSECanvasDeletedEventData): Data payload for canvas deleted events.
    """

    type_: Literal["canvas_deleted"]
    timestamp: float
    data: "SSECanvasDeletedEventData"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        timestamp = self.timestamp

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "timestamp": timestamp,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sse_canvas_deleted_event_data import SSECanvasDeletedEventData

        d = dict(src_dict)
        type_ = cast(Literal["canvas_deleted"], d.pop("type"))
        if type_ != "canvas_deleted":
            raise ValueError(f"type must match const 'canvas_deleted', got '{type_}'")

        timestamp = d.pop("timestamp")

        data = SSECanvasDeletedEventData.from_dict(d.pop("data"))

        sse_canvas_deleted_event = cls(
            type_=type_,
            timestamp=timestamp,
            data=data,
        )

        sse_canvas_deleted_event.additional_properties = d
        return sse_canvas_deleted_event

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
