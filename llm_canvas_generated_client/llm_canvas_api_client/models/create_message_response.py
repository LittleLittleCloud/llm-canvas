from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateMessageResponse")


@_attrs_define
class CreateMessageResponse:
    """Response type for POST /api/v1/canvas/{canvas_id}/messages

    Attributes:
        message_id (str):
        canvas_id (str):
        message (str):
    """

    message_id: str
    canvas_id: str
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message_id = self.message_id

        canvas_id = self.canvas_id

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message_id": message_id,
                "canvas_id": canvas_id,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message_id = d.pop("message_id")

        canvas_id = d.pop("canvas_id")

        message = d.pop("message")

        create_message_response = cls(
            message_id=message_id,
            canvas_id=canvas_id,
            message=message,
        )

        create_message_response.additional_properties = d
        return create_message_response

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
