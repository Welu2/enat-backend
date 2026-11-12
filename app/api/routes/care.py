from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response

from app.db.pagination import PAGE_RESPONSE
from app.dependencies import get_current_user_id
from app.models.care import (
    CareAccepted,
    CareAcceptRequest,
    CareConnection,
    CareInviteRequest,
    CareInviteResponse,
)
from app.services import care_access

router = APIRouter(tags=["care"], dependencies=[Depends(get_current_user_id)])


@router.post(
    "/users/me/care-connections", response_model=CareInviteResponse, status_code=201
)
def invite(payload: CareInviteRequest):
    return care_access.invite(payload)


@router.get(
    "/users/me/care-connections",
    response_model=list[CareConnection],
    responses=PAGE_RESPONSE,
)
def connections(
    response: Response,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    cursor: Annotated[str | None, Query(max_length=256)] = None,
):
    rows, next_cursor = care_access.connections(limit, cursor)
    if next_cursor:
        response.headers["X-Next-Cursor"] = next_cursor
    return rows


@router.delete("/users/me/care-connections/{connection_id}", status_code=204)
def revoke(connection_id: UUID) -> Response:
    care_access.revoke(connection_id)
    return Response(status_code=204)


@router.post("/care-connections/accept", response_model=CareAccepted)
def accept(payload: CareAcceptRequest):
    return care_access.accept(payload.token)
