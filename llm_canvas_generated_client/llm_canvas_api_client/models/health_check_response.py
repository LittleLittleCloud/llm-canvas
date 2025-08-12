from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.health_check_response_server_type import HealthCheckResponseServerType

T = TypeVar("T", bound="HealthCheckResponse")


@_attrs_define
class HealthCheckResponse:
    """Response type for GET /api/v1/health

    Attributes:
        status (Literal['healthy']):
        server_type (HealthCheckResponseServerType):
        timestamp (Union[None, float]):
    """

    status: Literal["healthy"]
    server_type: HealthCheckResponseServerType
    timestamp: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        server_type = self.server_type.value

        timestamp: Union[None, float]
        timestamp = self.timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "server_type": server_type,
                "timestamp": timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = cast(Literal["healthy"], d.pop("status"))
        if status != "healthy":
            raise ValueError(f"status must match const 'healthy', got '{status}'")

        server_type = HealthCheckResponseServerType(d.pop("server_type"))

        def _parse_timestamp(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        timestamp = _parse_timestamp(d.pop("timestamp"))

        health_check_response = cls(
            status=status,
            server_type=server_type,
            timestamp=timestamp,
        )

        health_check_response.additional_properties = d
        return health_check_response

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
