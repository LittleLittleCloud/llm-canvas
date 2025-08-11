from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.canvas_commit_message_event import CanvasCommitMessageEvent


T = TypeVar("T", bound="CommitMessageRequest")


@_attrs_define
class CommitMessageRequest:
    """
    Attributes:
        data (CanvasCommitMessageEvent): Event data for canvas message commits.
    """

    data: "CanvasCommitMessageEvent"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.canvas_commit_message_event import CanvasCommitMessageEvent

        d = dict(src_dict)
        data = CanvasCommitMessageEvent.from_dict(d.pop("data"))

        commit_message_request = cls(
            data=data,
        )

        commit_message_request.additional_properties = d
        return commit_message_request

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
