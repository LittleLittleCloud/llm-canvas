from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.message_role import MessageRole

if TYPE_CHECKING:
    from ..models.image_block_param import ImageBlockParam
    from ..models.text_block_param import TextBlockParam
    from ..models.tool_result_block_param import ToolResultBlockParam
    from ..models.tool_use_block_param import ToolUseBlockParam


T = TypeVar("T", bound="Message")


@_attrs_define
class Message:
    """Message structure for canvas conversations.

    Attributes:
        content (Union[list[Union['ImageBlockParam', 'TextBlockParam', 'ToolResultBlockParam', 'ToolUseBlockParam']],
            str]):
        role (MessageRole):
    """

    content: Union[list[Union["ImageBlockParam", "TextBlockParam", "ToolResultBlockParam", "ToolUseBlockParam"]], str]
    role: MessageRole
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.text_block_param import TextBlockParam
        from ..models.tool_result_block_param import ToolResultBlockParam
        from ..models.tool_use_block_param import ToolUseBlockParam

        content: Union[list[dict[str, Any]], str]
        if isinstance(self.content, list):
            content = []
            for content_type_1_item_data in self.content:
                content_type_1_item: dict[str, Any]
                if isinstance(content_type_1_item_data, TextBlockParam):
                    content_type_1_item = content_type_1_item_data.to_dict()
                elif isinstance(content_type_1_item_data, ToolUseBlockParam):
                    content_type_1_item = content_type_1_item_data.to_dict()
                elif isinstance(content_type_1_item_data, ToolResultBlockParam):
                    content_type_1_item = content_type_1_item_data.to_dict()
                else:
                    content_type_1_item = content_type_1_item_data.to_dict()

                content.append(content_type_1_item)

        else:
            content = self.content

        role = self.role.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.image_block_param import ImageBlockParam
        from ..models.text_block_param import TextBlockParam
        from ..models.tool_result_block_param import ToolResultBlockParam
        from ..models.tool_use_block_param import ToolUseBlockParam

        d = dict(src_dict)

        def _parse_content(
            data: object,
        ) -> Union[list[Union["ImageBlockParam", "TextBlockParam", "ToolResultBlockParam", "ToolUseBlockParam"]], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_type_1 = []
                _content_type_1 = data
                for content_type_1_item_data in _content_type_1:

                    def _parse_content_type_1_item(
                        data: object,
                    ) -> Union["ImageBlockParam", "TextBlockParam", "ToolResultBlockParam", "ToolUseBlockParam"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            content_type_1_item_type_0 = TextBlockParam.from_dict(data)

                            return content_type_1_item_type_0
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            content_type_1_item_type_1 = ToolUseBlockParam.from_dict(data)

                            return content_type_1_item_type_1
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            content_type_1_item_type_2 = ToolResultBlockParam.from_dict(data)

                            return content_type_1_item_type_2
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        content_type_1_item_type_3 = ImageBlockParam.from_dict(data)

                        return content_type_1_item_type_3

                    content_type_1_item = _parse_content_type_1_item(content_type_1_item_data)

                    content_type_1.append(content_type_1_item)

                return content_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    list[Union["ImageBlockParam", "TextBlockParam", "ToolResultBlockParam", "ToolUseBlockParam"]], str
                ],
                data,
            )

        content = _parse_content(d.pop("content"))

        role = MessageRole(d.pop("role"))

        message = cls(
            content=content,
            role=role,
        )

        message.additional_properties = d
        return message

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
