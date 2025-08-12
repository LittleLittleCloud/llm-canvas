from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CitationPageLocationParam")


@_attrs_define
class CitationPageLocationParam:
    """
    Attributes:
        cited_text (str):
        document_index (int):
        document_title (Union[None, str]):
        end_page_number (int):
        start_page_number (int):
        type_ (Literal['page_location']):
    """

    cited_text: str
    document_index: int
    document_title: Union[None, str]
    end_page_number: int
    start_page_number: int
    type_: Literal["page_location"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cited_text = self.cited_text

        document_index = self.document_index

        document_title: Union[None, str]
        document_title = self.document_title

        end_page_number = self.end_page_number

        start_page_number = self.start_page_number

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cited_text": cited_text,
                "document_index": document_index,
                "document_title": document_title,
                "end_page_number": end_page_number,
                "start_page_number": start_page_number,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cited_text = d.pop("cited_text")

        document_index = d.pop("document_index")

        def _parse_document_title(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        document_title = _parse_document_title(d.pop("document_title"))

        end_page_number = d.pop("end_page_number")

        start_page_number = d.pop("start_page_number")

        type_ = cast(Literal["page_location"], d.pop("type"))
        if type_ != "page_location":
            raise ValueError(f"type must match const 'page_location', got '{type_}'")

        citation_page_location_param = cls(
            cited_text=cited_text,
            document_index=document_index,
            document_title=document_title,
            end_page_number=end_page_number,
            start_page_number=start_page_number,
            type_=type_,
        )

        citation_page_location_param.additional_properties = d
        return citation_page_location_param

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
