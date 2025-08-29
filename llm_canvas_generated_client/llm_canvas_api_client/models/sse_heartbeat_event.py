from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SSEHeartbeatEvent")


@_attrs_define
class SSEHeartbeatEvent:
    """SSE heartbeat event to keep connections alive.

    Attributes:
        type_ (Literal['heartbeat']):
        timestamp (float):
    """

    type_: Literal["heartbeat"]
    timestamp: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        timestamp = self.timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "timestamp": timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = cast(Literal["heartbeat"], d.pop("type"))
        if type_ != "heartbeat":
            raise ValueError(f"type must match const 'heartbeat', got '{type_}'")

        timestamp = d.pop("timestamp")

        sse_heartbeat_event = cls(
            type_=type_,
            timestamp=timestamp,
        )

        sse_heartbeat_event.additional_properties = d
        return sse_heartbeat_event

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
