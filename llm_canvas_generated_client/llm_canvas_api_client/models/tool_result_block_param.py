from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cache_control_ephemeral_param import CacheControlEphemeralParam
    from ..models.image_block_param import ImageBlockParam
    from ..models.search_result_block_param import SearchResultBlockParam
    from ..models.text_block_param import TextBlockParam


T = TypeVar("T", bound="ToolResultBlockParam")


@_attrs_define
class ToolResultBlockParam:
    """
    Attributes:
        tool_use_id (str):
        type_ (Literal['tool_result']):
        cache_control (Union['CacheControlEphemeralParam', None, Unset]):
        content (Union[Unset, list[Union['ImageBlockParam', 'SearchResultBlockParam', 'TextBlockParam']], str]):
        is_error (Union[Unset, bool]):
    """

    tool_use_id: str
    type_: Literal["tool_result"]
    cache_control: Union["CacheControlEphemeralParam", None, Unset] = UNSET
    content: Union[Unset, list[Union["ImageBlockParam", "SearchResultBlockParam", "TextBlockParam"]], str] = UNSET
    is_error: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.cache_control_ephemeral_param import CacheControlEphemeralParam
        from ..models.image_block_param import ImageBlockParam
        from ..models.text_block_param import TextBlockParam

        tool_use_id = self.tool_use_id

        type_ = self.type_

        cache_control: Union[None, Unset, dict[str, Any]]
        if isinstance(self.cache_control, Unset):
            cache_control = UNSET
        elif isinstance(self.cache_control, CacheControlEphemeralParam):
            cache_control = self.cache_control.to_dict()
        else:
            cache_control = self.cache_control

        content: Union[Unset, list[dict[str, Any]], str]
        if isinstance(self.content, Unset):
            content = UNSET
        elif isinstance(self.content, list):
            content = []
            for content_type_1_item_data in self.content:
                content_type_1_item: dict[str, Any]
                if isinstance(content_type_1_item_data, TextBlockParam):
                    content_type_1_item = content_type_1_item_data.to_dict()
                elif isinstance(content_type_1_item_data, ImageBlockParam):
                    content_type_1_item = content_type_1_item_data.to_dict()
                else:
                    content_type_1_item = content_type_1_item_data.to_dict()

                content.append(content_type_1_item)

        else:
            content = self.content

        is_error = self.is_error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tool_use_id": tool_use_id,
                "type": type_,
            }
        )
        if cache_control is not UNSET:
            field_dict["cache_control"] = cache_control
        if content is not UNSET:
            field_dict["content"] = content
        if is_error is not UNSET:
            field_dict["is_error"] = is_error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cache_control_ephemeral_param import CacheControlEphemeralParam
        from ..models.image_block_param import ImageBlockParam
        from ..models.search_result_block_param import SearchResultBlockParam
        from ..models.text_block_param import TextBlockParam

        d = dict(src_dict)
        tool_use_id = d.pop("tool_use_id")

        type_ = cast(Literal["tool_result"], d.pop("type"))
        if type_ != "tool_result":
            raise ValueError(f"type must match const 'tool_result', got '{type_}'")

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

        def _parse_content(
            data: object,
        ) -> Union[Unset, list[Union["ImageBlockParam", "SearchResultBlockParam", "TextBlockParam"]], str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_type_1 = []
                _content_type_1 = data
                for content_type_1_item_data in _content_type_1:

                    def _parse_content_type_1_item(
                        data: object,
                    ) -> Union["ImageBlockParam", "SearchResultBlockParam", "TextBlockParam"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            content_type_1_item_type_0 = TextBlockParam.from_dict(data)

                            return content_type_1_item_type_0
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            content_type_1_item_type_1 = ImageBlockParam.from_dict(data)

                            return content_type_1_item_type_1
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        content_type_1_item_type_2 = SearchResultBlockParam.from_dict(data)

                        return content_type_1_item_type_2

                    content_type_1_item = _parse_content_type_1_item(content_type_1_item_data)

                    content_type_1.append(content_type_1_item)

                return content_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[Unset, list[Union["ImageBlockParam", "SearchResultBlockParam", "TextBlockParam"]], str], data
            )

        content = _parse_content(d.pop("content", UNSET))

        is_error = d.pop("is_error", UNSET)

        tool_result_block_param = cls(
            tool_use_id=tool_use_id,
            type_=type_,
            cache_control=cache_control,
            content=content,
            is_error=is_error,
        )

        tool_result_block_param.additional_properties = d
        return tool_result_block_param

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
