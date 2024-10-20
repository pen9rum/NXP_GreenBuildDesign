from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

@dataclass
class DesignData:
    designName: str
    length: float
    width: float
    rooms: Dict[str, int]
    windows: Dict[str, bool]
    specialRequest: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "designName": self.designName,
            "length": self.length,
            "width": self.width,
            "rooms": self.rooms,
            "windows": self.windows,
            "specialRequest": self.specialRequest
        }

@dataclass
class Location:
    temperature: float
    humidity: float
    sunlight: float

    def to_dict(self) -> dict:
        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "sunlight": self.sunlight
        }

@dataclass
class RoomEnvironmentRule:
    temperature: dict[str, float]
    humidity: dict[str, float]
    sunlight: dict[str, float]

@dataclass
class EnvironmentRules:
    livingRoom: RoomEnvironmentRule
    bedroom: RoomEnvironmentRule
    kitchen: RoomEnvironmentRule
    bathroom: RoomEnvironmentRule

@dataclass
class RoomDimension:
    length: float
    width: float
    x: float
    y: float

@dataclass
class RoomLayout:
    livingRoom: RoomDimension
    bedroom: List[RoomDimension]
    kitchen: RoomDimension
    bathroom: List[RoomDimension]

@dataclass
class EnergyEfficiencyScore:
    total_score: float
    temperature_score: float
    light_score: float
    humidity_score: float

@dataclass
class EnergyEfficiencyReport:
    energy_efficiency_grade: str
    total_score: float
    detailed_scores: dict[str, float]
    explanation: List[str]

@dataclass
class DesignConfiguration:
    name: str
    description: str
    advantages: dict[str, str]
    considerations: dict[str, str]
    room_layout: RoomLayout
    energy_efficiency_report: EnergyEfficiencyReport

@dataclass
class DesignResult:
    meta_info: dict[str, str]
    design_data: DesignData
    room_areas: dict[str, float]
    room_ratios: dict[str, float]
    locations: dict[str, Location]
    environmental_conditions: dict[str, str]
    room_environment_rules: EnvironmentRules
    configurations: List[DesignConfiguration]
    summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "meta_info": self.meta_info,
            "design_data": self.design_data.to_dict(),
            "room_areas": self.room_areas,
            "room_ratios": self.room_ratios,
            "locations": {k: v.to_dict() for k, v in self.locations.items()},
            "environmental_conditions": self.environmental_conditions,
            "room_environment_rules": {
                "livingRoom": vars(self.room_environment_rules.livingRoom),
                "bedroom": vars(self.room_environment_rules.bedroom),
                "kitchen": vars(self.room_environment_rules.kitchen),
                "bathroom": vars(self.room_environment_rules.bathroom)
            },
            "configurations": [
                {
                    "name": config.name,
                    "description": config.description,
                    "advantages": config.advantages,
                    "considerations": config.considerations,
                    "room_layout": {
                        "livingRoom": vars(config.room_layout.livingRoom),
                        "bedroom": [vars(room) for room in config.room_layout.bedroom],
                        "kitchen": vars(config.room_layout.kitchen),
                        "bathroom": [vars(room) for room in config.room_layout.bathroom]
                    },
                    "energy_efficiency_report": vars(config.energy_efficiency_report)
                } for config in self.configurations
            ],
            "summary": self.summary
        }