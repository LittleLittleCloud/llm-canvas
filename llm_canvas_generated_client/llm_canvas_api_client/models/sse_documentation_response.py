from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.sse_canvas_created_event import SSECanvasCreatedEvent
    from ..models.sse_canvas_deleted_event import SSECanvasDeletedEvent
    from ..models.sse_canvas_updated_event import SSECanvasUpdatedEvent
    from ..models.sse_error_event import SSEErrorEvent
    from ..models.sse_heartbeat_event import SSEHeartbeatEvent
    from ..models.sse_message_committed_event import SSEMessageCommittedEvent
    from ..models.sse_message_deleted_event import SSEMessageDeletedEvent
    from ..models.sse_message_updated_event import SSEMessageUpdatedEvent


T = TypeVar("T", bound="SSEDocumentationResponse")


@_attrs_define
class SSEDocumentationResponse:
    """Response type for GET /api/v1/sse/documentation

    Attributes:
        events (list[Union['SSECanvasCreatedEvent', 'SSECanvasDeletedEvent', 'SSECanvasUpdatedEvent', 'SSEErrorEvent',
            'SSEHeartbeatEvent', 'SSEMessageCommittedEvent', 'SSEMessageDeletedEvent', 'SSEMessageUpdatedEvent']]):
    """

    events: list[
        Union[
            "SSECanvasCreatedEvent",
            "SSECanvasDeletedEvent",
            "SSECanvasUpdatedEvent",
            "SSEErrorEvent",
            "SSEHeartbeatEvent",
            "SSEMessageCommittedEvent",
            "SSEMessageDeletedEvent",
            "SSEMessageUpdatedEvent",
        ]
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.sse_canvas_created_event import SSECanvasCreatedEvent
        from ..models.sse_canvas_deleted_event import SSECanvasDeletedEvent
        from ..models.sse_canvas_updated_event import SSECanvasUpdatedEvent
        from ..models.sse_error_event import SSEErrorEvent
        from ..models.sse_heartbeat_event import SSEHeartbeatEvent
        from ..models.sse_message_committed_event import SSEMessageCommittedEvent
        from ..models.sse_message_updated_event import SSEMessageUpdatedEvent

        events = []
        for events_item_data in self.events:
            events_item: dict[str, Any]
            if isinstance(events_item_data, SSECanvasCreatedEvent):
                events_item = events_item_data.to_dict()
            elif isinstance(events_item_data, SSECanvasUpdatedEvent):
                events_item = events_item_data.to_dict()
            elif isinstance(events_item_data, SSECanvasDeletedEvent):
                events_item = events_item_data.to_dict()
            elif isinstance(events_item_data, SSEHeartbeatEvent):
                events_item = events_item_data.to_dict()
            elif isinstance(events_item_data, SSEErrorEvent):
                events_item = events_item_data.to_dict()
            elif isinstance(events_item_data, SSEMessageCommittedEvent):
                events_item = events_item_data.to_dict()
            elif isinstance(events_item_data, SSEMessageUpdatedEvent):
                events_item = events_item_data.to_dict()
            else:
                events_item = events_item_data.to_dict()

            events.append(events_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "events": events,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sse_canvas_created_event import SSECanvasCreatedEvent
        from ..models.sse_canvas_deleted_event import SSECanvasDeletedEvent
        from ..models.sse_canvas_updated_event import SSECanvasUpdatedEvent
        from ..models.sse_error_event import SSEErrorEvent
        from ..models.sse_heartbeat_event import SSEHeartbeatEvent
        from ..models.sse_message_committed_event import SSEMessageCommittedEvent
        from ..models.sse_message_deleted_event import SSEMessageDeletedEvent
        from ..models.sse_message_updated_event import SSEMessageUpdatedEvent

        d = dict(src_dict)
        events = []
        _events = d.pop("events")
        for events_item_data in _events:

            def _parse_events_item(
                data: object,
            ) -> Union[
                "SSECanvasCreatedEvent",
                "SSECanvasDeletedEvent",
                "SSECanvasUpdatedEvent",
                "SSEErrorEvent",
                "SSEHeartbeatEvent",
                "SSEMessageCommittedEvent",
                "SSEMessageDeletedEvent",
                "SSEMessageUpdatedEvent",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    events_item_type_0 = SSECanvasCreatedEvent.from_dict(data)

                    return events_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    events_item_type_1 = SSECanvasUpdatedEvent.from_dict(data)

                    return events_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    events_item_type_2 = SSECanvasDeletedEvent.from_dict(data)

                    return events_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    events_item_type_3 = SSEHeartbeatEvent.from_dict(data)

                    return events_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    events_item_type_4 = SSEErrorEvent.from_dict(data)

                    return events_item_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    events_item_type_5 = SSEMessageCommittedEvent.from_dict(data)

                    return events_item_type_5
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    events_item_type_6 = SSEMessageUpdatedEvent.from_dict(data)

                    return events_item_type_6
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                events_item_type_7 = SSEMessageDeletedEvent.from_dict(data)

                return events_item_type_7

            events_item = _parse_events_item(events_item_data)

            events.append(events_item)

        sse_documentation_response = cls(
            events=events,
        )

        sse_documentation_response.additional_properties = d
        return sse_documentation_response

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
