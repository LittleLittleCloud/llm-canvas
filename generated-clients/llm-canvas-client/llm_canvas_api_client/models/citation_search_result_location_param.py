from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CitationSearchResultLocationParam")


@_attrs_define
class CitationSearchResultLocationParam:
    """
    Attributes:
        cited_text (str):
        end_block_index (int):
        search_result_index (int):
        source (str):
        start_block_index (int):
        title (Union[None, str]):
        type_ (Literal['search_result_location']):
    """

    cited_text: str
    end_block_index: int
    search_result_index: int
    source: str
    start_block_index: int
    title: Union[None, str]
    type_: Literal["search_result_location"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cited_text = self.cited_text

        end_block_index = self.end_block_index

        search_result_index = self.search_result_index

        source = self.source

        start_block_index = self.start_block_index

        title: Union[None, str]
        title = self.title

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cited_text": cited_text,
                "end_block_index": end_block_index,
                "search_result_index": search_result_index,
                "source": source,
                "start_block_index": start_block_index,
                "title": title,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cited_text = d.pop("cited_text")

        end_block_index = d.pop("end_block_index")

        search_result_index = d.pop("search_result_index")

        source = d.pop("source")

        start_block_index = d.pop("start_block_index")

        def _parse_title(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        title = _parse_title(d.pop("title"))

        type_ = cast(Literal["search_result_location"], d.pop("type"))
        if type_ != "search_result_location":
            raise ValueError(f"type must match const 'search_result_location', got '{type_}'")

        citation_search_result_location_param = cls(
            cited_text=cited_text,
            end_block_index=end_block_index,
            search_result_index=search_result_index,
            source=source,
            start_block_index=start_block_index,
            title=title,
            type_=type_,
        )

        citation_search_result_location_param.additional_properties = d
        return citation_search_result_location_param

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
