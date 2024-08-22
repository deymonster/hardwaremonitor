from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from crud.base import CRUDBase
from models.agent_trigger import AgentTrigger
from schemas.trigger import ITriggerCreate,ITriggerUpdate
from uuid import UUID


class CRUDTrigger(CRUDBase[AgentTrigger, ITriggerCreate, ITriggerUpdate]):
    async def get_by_uuid(self,
                          uuid: UUID,
                          db_session: AsyncSession | None = None
                          ) -> AgentTrigger | None:
        session = db_session or self.db.session
        query = select(self.model).where(self.model.agent_uuid == uuid)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def check_condition(self,
                              *,
                              uuid: UUID,
                              current_value: Union[str, int, float],
                              db_session: AsyncSession | None = None) -> bool:
        """Check if the condition is met"""
        session = db_session or self.db.session
        trigger = await self.get_by_uuid(uuid, db_session=db_session)
        if trigger:
            return trigger.check_trigger(current_value)
        return False

    async def delete_by_uuid(self,
                             uuid: UUID,
                             db_session: AsyncSession | None = None) -> bool:
        """Delete the trigger by uuid"""
        session = db_session or self.db.session
        trigger = await self.get_by_uuid(uuid, db_session=db_session)
        if trigger:
            await session.delete(trigger)
            await session.commit()
            return True
        return False

trigger_crud = CRUDTrigger(AgentTrigger)


__all__ = [
    "trigger_crud",
]
