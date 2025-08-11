from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.canvas_summary_meta import CanvasSummaryMeta


T = TypeVar("T", bound="CanvasSummary")


@_attrs_define
class CanvasSummary:
    """Summary information about a canvas.

    Attributes:
        canvas_id (str):
        created_at (float):
        root_ids (list[str]):
        node_count (int):
        title (Union[None, str]):
        description (Union[None, str]):
        meta (CanvasSummaryMeta):
    """

    canvas_id: str
    created_at: float
    root_ids: list[str]
    node_count: int
    title: Union[None, str]
    description: Union[None, str]
    meta: "CanvasSummaryMeta"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        canvas_id = self.canvas_id

        created_at = self.created_at

        root_ids = self.root_ids

        node_count = self.node_count

        title: Union[None, str]
        title = self.title

        description: Union[None, str]
        description = self.description

        meta = self.meta.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "canvas_id": canvas_id,
                "created_at": created_at,
                "root_ids": root_ids,
                "node_count": node_count,
                "title": title,
                "description": description,
                "meta": meta,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.canvas_summary_meta import CanvasSummaryMeta

        d = dict(src_dict)
        canvas_id = d.pop("canvas_id")

        created_at = d.pop("created_at")

        root_ids = cast(list[str], d.pop("root_ids"))

        node_count = d.pop("node_count")

        def _parse_title(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        title = _parse_title(d.pop("title"))

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        meta = CanvasSummaryMeta.from_dict(d.pop("meta"))

        canvas_summary = cls(
            canvas_id=canvas_id,
            created_at=created_at,
            root_ids=root_ids,
            node_count=node_count,
            title=title,
            description=description,
            meta=meta,
        )

        canvas_summary.additional_properties = d
        return canvas_summary

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
