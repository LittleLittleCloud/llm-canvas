from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.base_64_image_source_param_media_type import Base64ImageSourceParamMediaType

T = TypeVar("T", bound="Base64ImageSourceParam")


@_attrs_define
class Base64ImageSourceParam:
    """
    Attributes:
        data (str):
        media_type (Base64ImageSourceParamMediaType):
        type_ (Literal['base64']):
    """

    data: str
    media_type: Base64ImageSourceParamMediaType
    type_: Literal["base64"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: str
        data = self.data

        media_type = self.media_type.value

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "media_type": media_type,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_data(data: object) -> str:
            return cast(str, data)

        data = _parse_data(d.pop("data"))

        media_type = Base64ImageSourceParamMediaType(d.pop("media_type"))

        type_ = cast(Literal["base64"], d.pop("type"))
        if type_ != "base64":
            raise ValueError(f"type must match const 'base64', got '{type_}'")

        base_64_image_source_param = cls(
            data=data,
            media_type=media_type,
            type_=type_,
        )

        base_64_image_source_param.additional_properties = d
        return base_64_image_source_param

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
