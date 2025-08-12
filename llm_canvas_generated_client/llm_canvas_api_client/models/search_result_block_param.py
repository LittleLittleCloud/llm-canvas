from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cache_control_ephemeral_param import CacheControlEphemeralParam
    from ..models.citations_config_param import CitationsConfigParam
    from ..models.text_block_param import TextBlockParam


T = TypeVar("T", bound="SearchResultBlockParam")


@_attrs_define
class SearchResultBlockParam:
    """
    Attributes:
        content (list['TextBlockParam']):
        source (str):
        title (str):
        type_ (Literal['search_result']):
        cache_control (Union['CacheControlEphemeralParam', None, Unset]):
        citations (Union[Unset, CitationsConfigParam]):
    """

    content: list["TextBlockParam"]
    source: str
    title: str
    type_: Literal["search_result"]
    cache_control: Union["CacheControlEphemeralParam", None, Unset] = UNSET
    citations: Union[Unset, "CitationsConfigParam"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.cache_control_ephemeral_param import CacheControlEphemeralParam

        content = []
        for content_item_data in self.content:
            content_item = content_item_data.to_dict()
            content.append(content_item)

        source = self.source

        title = self.title

        type_ = self.type_

        cache_control: Union[None, Unset, dict[str, Any]]
        if isinstance(self.cache_control, Unset):
            cache_control = UNSET
        elif isinstance(self.cache_control, CacheControlEphemeralParam):
            cache_control = self.cache_control.to_dict()
        else:
            cache_control = self.cache_control

        citations: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.citations, Unset):
            citations = self.citations.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "source": source,
                "title": title,
                "type": type_,
            }
        )
        if cache_control is not UNSET:
            field_dict["cache_control"] = cache_control
        if citations is not UNSET:
            field_dict["citations"] = citations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cache_control_ephemeral_param import CacheControlEphemeralParam
        from ..models.citations_config_param import CitationsConfigParam
        from ..models.text_block_param import TextBlockParam

        d = dict(src_dict)
        content = []
        _content = d.pop("content")
        for content_item_data in _content:
            content_item = TextBlockParam.from_dict(content_item_data)

            content.append(content_item)

        source = d.pop("source")

        title = d.pop("title")

        type_ = cast(Literal["search_result"], d.pop("type"))
        if type_ != "search_result":
            raise ValueError(f"type must match const 'search_result', got '{type_}'")

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

        _citations = d.pop("citations", UNSET)
        citations: Union[Unset, CitationsConfigParam]
        if isinstance(_citations, Unset):
            citations = UNSET
        else:
            citations = CitationsConfigParam.from_dict(_citations)

        search_result_block_param = cls(
            content=content,
            source=source,
            title=title,
            type_=type_,
            cache_control=cache_control,
            citations=citations,
        )

        search_result_block_param.additional_properties = d
        return search_result_block_param

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
