from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_64_image_source_param import Base64ImageSourceParam
    from ..models.cache_control_ephemeral_param import CacheControlEphemeralParam
    from ..models.url_image_source_param import URLImageSourceParam


T = TypeVar("T", bound="ImageBlockParam")


@_attrs_define
class ImageBlockParam:
    """
    Attributes:
        source (Union['Base64ImageSourceParam', 'URLImageSourceParam']):
        type_ (Literal['image']):
        cache_control (Union['CacheControlEphemeralParam', None, Unset]):
    """

    source: Union["Base64ImageSourceParam", "URLImageSourceParam"]
    type_: Literal["image"]
    cache_control: Union["CacheControlEphemeralParam", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.base_64_image_source_param import Base64ImageSourceParam
        from ..models.cache_control_ephemeral_param import CacheControlEphemeralParam

        source: dict[str, Any]
        if isinstance(self.source, Base64ImageSourceParam):
            source = self.source.to_dict()
        else:
            source = self.source.to_dict()

        type_ = self.type_

        cache_control: Union[None, Unset, dict[str, Any]]
        if isinstance(self.cache_control, Unset):
            cache_control = UNSET
        elif isinstance(self.cache_control, CacheControlEphemeralParam):
            cache_control = self.cache_control.to_dict()
        else:
            cache_control = self.cache_control

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
                "type": type_,
            }
        )
        if cache_control is not UNSET:
            field_dict["cache_control"] = cache_control

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_64_image_source_param import Base64ImageSourceParam
        from ..models.cache_control_ephemeral_param import CacheControlEphemeralParam
        from ..models.url_image_source_param import URLImageSourceParam

        d = dict(src_dict)

        def _parse_source(data: object) -> Union["Base64ImageSourceParam", "URLImageSourceParam"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                source_type_0 = Base64ImageSourceParam.from_dict(data)

                return source_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            source_type_1 = URLImageSourceParam.from_dict(data)

            return source_type_1

        source = _parse_source(d.pop("source"))

        type_ = cast(Literal["image"], d.pop("type"))
        if type_ != "image":
            raise ValueError(f"type must match const 'image', got '{type_}'")

        def _parse_cache_control(data: object) -> Union["CacheControlEphemeralParam", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                cache_control_type_0 = CacheControlEphemeralParam.from_dict(data)

                return cache_control_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CacheControlEphemeralParam", None, Unset], data)

        cache_control = _parse_cache_control(d.pop("cache_control", UNSET))

        image_block_param = cls(
            source=source,
            type_=type_,
            cache_control=cache_control,
        )

        image_block_param.additional_properties = d
        return image_block_param

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
