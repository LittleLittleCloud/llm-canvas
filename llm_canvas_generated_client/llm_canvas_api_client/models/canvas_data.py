from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.canvas_data_nodes import CanvasDataNodes


T = TypeVar("T", bound="CanvasData")


@_attrs_define
class CanvasData:
    """Complete canvas data structure.

    Attributes:
        title (Union[None, str]):
        last_updated (Union[None, float]):
        description (Union[None, str]):
        canvas_id (str):
        created_at (float):
        nodes (CanvasDataNodes):
    """

    title: Union[None, str]
    last_updated: Union[None, float]
    description: Union[None, str]
    canvas_id: str
    created_at: float
    nodes: "CanvasDataNodes"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title: Union[None, str]
        title = self.title

        last_updated: Union[None, float]
        last_updated = self.last_updated

        description: Union[None, str]
        description = self.description

        canvas_id = self.canvas_id

        created_at = self.created_at

        nodes = self.nodes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "last_updated": last_updated,
                "description": description,
                "canvas_id": canvas_id,
                "created_at": created_at,
                "nodes": nodes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.canvas_data_nodes import CanvasDataNodes

        d = dict(src_dict)

        def _parse_title(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        title = _parse_title(d.pop("title"))

        def _parse_last_updated(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        last_updated = _parse_last_updated(d.pop("last_updated"))

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        canvas_id = d.pop("canvas_id")

        created_at = d.pop("created_at")

        nodes = CanvasDataNodes.from_dict(d.pop("nodes"))

        canvas_data = cls(
            title=title,
            last_updated=last_updated,
            description=description,
            canvas_id=canvas_id,
            created_at=created_at,
            nodes=nodes,
        )

        canvas_data.additional_properties = d
        return canvas_data

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
