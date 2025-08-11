from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CitationWebSearchResultLocationParam")


@_attrs_define
class CitationWebSearchResultLocationParam:
    """
    Attributes:
        cited_text (str):
        encrypted_index (str):
        title (Union[None, str]):
        type_ (Literal['web_search_result_location']):
        url (str):
    """

    cited_text: str
    encrypted_index: str
    title: Union[None, str]
    type_: Literal["web_search_result_location"]
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cited_text = self.cited_text

        encrypted_index = self.encrypted_index

        title: Union[None, str]
        title = self.title

        type_ = self.type_

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cited_text": cited_text,
                "encrypted_index": encrypted_index,
                "title": title,
                "type": type_,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cited_text = d.pop("cited_text")

        encrypted_index = d.pop("encrypted_index")

        def _parse_title(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        title = _parse_title(d.pop("title"))

        type_ = cast(Literal["web_search_result_location"], d.pop("type"))
        if type_ != "web_search_result_location":
            raise ValueError(f"type must match const 'web_search_result_location', got '{type_}'")

        url = d.pop("url")

        citation_web_search_result_location_param = cls(
            cited_text=cited_text,
            encrypted_index=encrypted_index,
            title=title,
            type_=type_,
            url=url,
        )

        citation_web_search_result_location_param.additional_properties = d
        return citation_web_search_result_location_param

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
