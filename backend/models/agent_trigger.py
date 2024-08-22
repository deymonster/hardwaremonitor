from uuid import UUID
from typing import TYPE_CHECKING, Optional, Union
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseTableID
from enum import Enum

class TriggerConditionEnum(str, Enum):
    EQUAL = "equal"
    NOT_EQUAL = "not_equal"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"


class AgentTriggerBase(SQLModel):
    agent_uuid: UUID = Field(index=True, unique=True)
    data_field: str
    condition: Optional[TriggerConditionEnum] = Field(description="Conditions for trigger")
    threshold_str: str | None = Field(default=None)
    threshold_float: float | None =Field(default=None)


class AgentTrigger(AgentTriggerBase, BaseTableID, table=True):
    def check_condition(self, current_value: Union[str, int, float]) -> bool:
        """Checking condition"""
        if self.threshold_float is not None:
            if isinstance(current_value, (int, float)):
                if self.condition == TriggerConditionEnum.EQUAL:
                    return current_value == self.threshold_float
                elif self.condition == TriggerConditionEnum.NOT_EQUAL:
                    return current_value != self.threshold_float
                elif self.condition == TriggerConditionEnum.GREATER_THAN:
                    return current_value > self.threshold_float
                elif self.condition == TriggerConditionEnum.LESS_THAN:
                    return current_value < self.threshold_float
                return False

        if self.threshold_str is not None:
            if isinstance(current_value, str):
                if self.condition == TriggerConditionEnum.EQUAL:
                    return current_value == self.threshold_str
                elif self.condition == TriggerConditionEnum.NOT_EQUAL:
                    return current_value != self.threshold_str
                return False

        return False


