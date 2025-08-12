from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.canvas_summary import CanvasSummary


T = TypeVar("T", bound="CanvasListResponse")


@_attrs_define
class CanvasListResponse:
    """Response type for GET /api/v1/canvas/list

    Attributes:
        canvases (list['CanvasSummary']):
    """

    canvases: list["CanvasSummary"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        canvases = []
        for canvases_item_data in self.canvases:
            canvases_item = canvases_item_data.to_dict()
            canvases.append(canvases_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "canvases": canvases,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.canvas_summary import CanvasSummary

        d = dict(src_dict)
        canvases = []
        _canvases = d.pop("canvases")
        for canvases_item_data in _canvases:
            canvases_item = CanvasSummary.from_dict(canvases_item_data)

            canvases.append(canvases_item)

        canvas_list_response = cls(
            canvases=canvases,
        )

        canvas_list_response.additional_properties = d
        return canvas_list_response

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
