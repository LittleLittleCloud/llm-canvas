from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_canvas_response import DeleteCanvasResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    canvas_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/api/v1/canvas/{canvas_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DeleteCanvasResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = DeleteCanvasResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DeleteCanvasResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    canvas_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[DeleteCanvasResponse, HTTPValidationError]]:
    """Delete Canvas

     Delete a canvas by ID.
    Args:
        canvas_id: Canvas UUID to delete
    Returns:
        DeleteCanvasResponse with success message
    Raises:
        HTTPException: 404 if canvas not found

    Args:
        canvas_id (str): Canvas UUID to delete

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteCanvasResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        canvas_id=canvas_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    canvas_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[DeleteCanvasResponse, HTTPValidationError]]:
    """Delete Canvas

     Delete a canvas by ID.
    Args:
        canvas_id: Canvas UUID to delete
    Returns:
        DeleteCanvasResponse with success message
    Raises:
        HTTPException: 404 if canvas not found

    Args:
        canvas_id (str): Canvas UUID to delete

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteCanvasResponse, HTTPValidationError]
    """

    return sync_detailed(
        canvas_id=canvas_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    canvas_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[DeleteCanvasResponse, HTTPValidationError]]:
    """Delete Canvas

     Delete a canvas by ID.
    Args:
        canvas_id: Canvas UUID to delete
    Returns:
        DeleteCanvasResponse with success message
    Raises:
        HTTPException: 404 if canvas not found

    Args:
        canvas_id (str): Canvas UUID to delete

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteCanvasResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        canvas_id=canvas_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    canvas_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[DeleteCanvasResponse, HTTPValidationError]]:
    """Delete Canvas

     Delete a canvas by ID.
    Args:
        canvas_id: Canvas UUID to delete
    Returns:
        DeleteCanvasResponse with success message
    Raises:
        HTTPException: 404 if canvas not found

    Args:
        canvas_id (str): Canvas UUID to delete

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteCanvasResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            canvas_id=canvas_id,
            client=client,
        )
    ).parsed
