from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cache_control_ephemeral_param import CacheControlEphemeralParam
    from ..models.citation_char_location_param import CitationCharLocationParam
    from ..models.citation_content_block_location_param import CitationContentBlockLocationParam
    from ..models.citation_page_location_param import CitationPageLocationParam
    from ..models.citation_search_result_location_param import CitationSearchResultLocationParam
    from ..models.citation_web_search_result_location_param import CitationWebSearchResultLocationParam


T = TypeVar("T", bound="TextBlockParam")


@_attrs_define
class TextBlockParam:
    """
    Attributes:
        text (str):
        type_ (Literal['text']):
        cache_control (Union['CacheControlEphemeralParam', None, Unset]):
        citations (Union[None, Unset, list[Union['CitationCharLocationParam', 'CitationContentBlockLocationParam',
            'CitationPageLocationParam', 'CitationSearchResultLocationParam', 'CitationWebSearchResultLocationParam']]]):
    """

    text: str
    type_: Literal["text"]
    cache_control: Union["CacheControlEphemeralParam", None, Unset] = UNSET
    citations: Union[
        None,
        Unset,
        list[
            Union[
                "CitationCharLocationParam",
                "CitationContentBlockLocationParam",
                "CitationPageLocationParam",
                "CitationSearchResultLocationParam",
                "CitationWebSearchResultLocationParam",
            ]
        ],
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.cache_control_ephemeral_param import CacheControlEphemeralParam
        from ..models.citation_char_location_param import CitationCharLocationParam
        from ..models.citation_content_block_location_param import CitationContentBlockLocationParam
        from ..models.citation_page_location_param import CitationPageLocationParam
        from ..models.citation_web_search_result_location_param import CitationWebSearchResultLocationParam

        text = self.text

        type_ = self.type_

        cache_control: Union[None, Unset, dict[str, Any]]
        if isinstance(self.cache_control, Unset):
            cache_control = UNSET
        elif isinstance(self.cache_control, CacheControlEphemeralParam):
            cache_control = self.cache_control.to_dict()
        else:
            cache_control = self.cache_control

        citations: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.citations, Unset):
            citations = UNSET
        elif isinstance(self.citations, list):
            citations = []
            for citations_type_0_item_data in self.citations:
                citations_type_0_item: dict[str, Any]
                if isinstance(citations_type_0_item_data, CitationCharLocationParam):
                    citations_type_0_item = citations_type_0_item_data.to_dict()
                elif isinstance(citations_type_0_item_data, CitationPageLocationParam):
                    citations_type_0_item = citations_type_0_item_data.to_dict()
                elif isinstance(citations_type_0_item_data, CitationContentBlockLocationParam):
                    citations_type_0_item = citations_type_0_item_data.to_dict()
                elif isinstance(citations_type_0_item_data, CitationWebSearchResultLocationParam):
                    citations_type_0_item = citations_type_0_item_data.to_dict()
                else:
                    citations_type_0_item = citations_type_0_item_data.to_dict()

                citations.append(citations_type_0_item)

        else:
            citations = self.citations

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
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
        from ..models.citation_char_location_param import CitationCharLocationParam
        from ..models.citation_content_block_location_param import CitationContentBlockLocationParam
        from ..models.citation_page_location_param import CitationPageLocationParam
        from ..models.citation_search_result_location_param import CitationSearchResultLocationParam
        from ..models.citation_web_search_result_location_param import CitationWebSearchResultLocationParam

        d = dict(src_dict)
        text = d.pop("text")

        type_ = cast(Literal["text"], d.pop("type"))
        if type_ != "text":
            raise ValueError(f"type must match const 'text', got '{type_}'")

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

        def _parse_citations(
            data: object,
        ) -> Union[
            None,
            Unset,
            list[
                Union[
                    "CitationCharLocationParam",
                    "CitationContentBlockLocationParam",
                    "CitationPageLocationParam",
                    "CitationSearchResultLocationParam",
                    "CitationWebSearchResultLocationParam",
                ]
            ],
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                citations_type_0 = []
                _citations_type_0 = data
                for citations_type_0_item_data in _citations_type_0:

                    def _parse_citations_type_0_item(
                        data: object,
                    ) -> Union[
                        "CitationCharLocationParam",
                        "CitationContentBlockLocationParam",
                        "CitationPageLocationParam",
                        "CitationSearchResultLocationParam",
                        "CitationWebSearchResultLocationParam",
                    ]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            citations_type_0_item_type_0 = CitationCharLocationParam.from_dict(data)

                            return citations_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            citations_type_0_item_type_1 = CitationPageLocationParam.from_dict(data)

                            return citations_type_0_item_type_1
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            citations_type_0_item_type_2 = CitationContentBlockLocationParam.from_dict(data)

                            return citations_type_0_item_type_2
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            citations_type_0_item_type_3 = CitationWebSearchResultLocationParam.from_dict(data)

                            return citations_type_0_item_type_3
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        citations_type_0_item_type_4 = CitationSearchResultLocationParam.from_dict(data)

                        return citations_type_0_item_type_4

                    citations_type_0_item = _parse_citations_type_0_item(citations_type_0_item_data)

                    citations_type_0.append(citations_type_0_item)

                return citations_type_0
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    Unset,
                    list[
                        Union[
                            "CitationCharLocationParam",
                            "CitationContentBlockLocationParam",
                            "CitationPageLocationParam",
                            "CitationSearchResultLocationParam",
                            "CitationWebSearchResultLocationParam",
                        ]
                    ],
                ],
                data,
            )

        citations = _parse_citations(d.pop("citations", UNSET))

        text_block_param = cls(
            text=text,
            type_=type_,
            cache_control=cache_control,
            citations=citations,
        )

        text_block_param.additional_properties = d
        return text_block_param

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
