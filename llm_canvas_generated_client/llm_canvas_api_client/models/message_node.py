from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.message import Message
    from ..models.message_node_meta_type_0 import MessageNodeMetaType0


T = TypeVar("T", bound="MessageNode")


@_attrs_define
class MessageNode:
    """Node in the canvas conversation graph.

    Attributes:
        id (str):
        message (Message): Message structure for canvas conversations.
        parent_id (Union[None, str]):
        child_ids (list[str]):
        meta (Union['MessageNodeMetaType0', None]):
    """

    id: str
    message: "Message"
    parent_id: Union[None, str]
    child_ids: list[str]
    meta: Union["MessageNodeMetaType0", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.message_node_meta_type_0 import MessageNodeMetaType0

        id = self.id

        message = self.message.to_dict()

        parent_id: Union[None, str]
        parent_id = self.parent_id

        child_ids = self.child_ids

        meta: Union[None, dict[str, Any]]
        if isinstance(self.meta, MessageNodeMetaType0):
            meta = self.meta.to_dict()
        else:
            meta = self.meta

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "message": message,
                "parent_id": parent_id,
                "child_ids": child_ids,
                "meta": meta,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message import Message
        from ..models.message_node_meta_type_0 import MessageNodeMetaType0

        d = dict(src_dict)
        id = d.pop("id")

        message = Message.from_dict(d.pop("message"))

        def _parse_parent_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        parent_id = _parse_parent_id(d.pop("parent_id"))

        child_ids = cast(list[str], d.pop("child_ids"))

        def _parse_meta(data: object) -> Union["MessageNodeMetaType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                meta_type_0 = MessageNodeMetaType0.from_dict(data)

                return meta_type_0
            except:  # noqa: E722
                pass
            return cast(Union["MessageNodeMetaType0", None], data)

        meta = _parse_meta(d.pop("meta"))

        message_node = cls(
            id=id,
            message=message,
            parent_id=parent_id,
            child_ids=child_ids,
            meta=meta,
        )

        message_node.additional_properties = d
        return message_node

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
