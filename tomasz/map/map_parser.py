from hackathon_bot import *
import json
import numpy as np
from typing import Tuple

class TomaszZone:
    def __init__(self, game_zone):
        self.index = game_zone.index
        self.pos = game_zone.x, game_zone.y
        self.width = game_zone.width
        self.height = game_zone.height
        self.status = game_zone.status
        self.pos = []

    def add_pos(self, x, y):
        self.pos.append((x, y))

    def to_dict(self):
        return {
            'idx': self.index,
            'pos': self.pos,
            'width': self.width,
            'height': self.height,
            'status': self.status,
            'pos': self.pos
        }
    
class TomaszAgent:
    def __init__(self, entity: AgentTank, position: Tuple[int, int]):
        self.entity = entity
        self.position = position

class TomaszMap:
    def __init__(self, game_state: GameState):
        game_map = game_state.map
        self.game_state = game_state
        self.size = (len(game_map.tiles), len(game_map.tiles[0]))
        self.agent = None
        self.initialized = False

        self.walls_arr = np.zeros(self.size, dtype=int)
        self.visible_arr = np.zeros(self.size, dtype=int)
        self.walls = []
        self.visible = []
        self.lasers = []
        self.bullets = []
        self.tanks = []
        self.mines = []
        self.items = []
        self.zones = {}

        self.entities_grid = np.zeros(self.size, dtype=object)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.entities_grid[i, j] = []
        
        self._extract_map_data(game_map)

    def iter_entities(self):
        for ent in [*self.lasers, *self.bullets, *self.tanks, *self.mines, *self.items]:
            yield ent

    def _add_entity(self, entity, x, y):
        if isinstance(entity, Wall):
            entity_dict = {'type': 'wall', 'pos': (x, y)}
            self.walls.append(entity_dict)
            self.walls_arr[x, y] = 1
        elif isinstance(entity, Laser):
            entity_dict = {'type': 'laser', 'pos': (x, y), 'ori': entity.orientation}
            self.lasers.append(entity_dict)
        elif isinstance(entity, DoubleBullet):
            entity_dict = {'type': 'double_bullet', 'pos': (x, y), 'dir': entity.direction}
            self.bullets.append(entity_dict)
        elif isinstance(entity, Bullet):
            entity_dict = {'type': 'bullet', 'pos': (x, y), 'dir': entity.direction}
            self.bullets.append(entity_dict)
        elif isinstance(entity, AgentTank,):
            entity_dict = {'type': 'agent_tank', 'pos': (x, y), 'dir': entity.direction, 'turret_dir': entity.turret.direction}
            self.agent = TomaszAgent(entity, (y, x))
            self.tanks.append(entity_dict)
        elif isinstance(entity, PlayerTank):
            entity_dict = {'type': 'player_tank', 'pos': (x, y), 'dir': entity.direction, 'turret_dir': entity.turret.direction}
            self.tanks.append(entity_dict)
        elif isinstance(entity, Mine):
            entity_dict = {'type': 'mine', 'pos': (x, y), 'exploded': entity.exploded}
            self.mines.append(entity_dict)
        elif isinstance(entity, Item):
            item_type = {
                SecondaryItemType.DOUBLE_BULLET: 'item_double_bullet',
                SecondaryItemType.LASER: 'item_laser',
                SecondaryItemType.MINE: 'item_mine',
                SecondaryItemType.RADAR: 'item_radar'
            }.get(entity.type, "item_unknown")
            entity_dict = {'type': item_type, 'pos': (x, y)}
            self.items.append(entity_dict)
        
        self.entities_grid[x, y] = [entity_dict]


    def _extract_map_data(self, game_map: Map):
        for zone in game_map.zones:
            idx = chr(zone.index)
            self.zones[idx] = TomaszZone(zone)

        for x, row in enumerate(game_map.tiles):
            for y, tile in enumerate(row):
                if tile.zone:
                    zone = self.zones[chr(tile.zone.index)]
                    zone.add_pos(x, y)

                if tile.is_visible:
                    self.visible.append((x, y))
                    self.visible_arr[x, y] = 1

                for entity in tile.entities:
                    self._add_entity(entity, x, y)

        self.initialized = True

    def _char_map(self):
        char_map = np.full(self.entities_grid.shape, " ", dtype=str)
        for idx, zone in self.zones.items():
            for x, y in zone.pos:
                char_map[x, y] = idx.lower()
        
        char_map = np.where(self.walls_arr == 1, "■", char_map)

        for x in range(self.entities_grid.shape[0]):
            for y in range(self.entities_grid.shape[1]):
                entities = self.entities_grid[x, y]
                if len(entities) > 0:
                    entity = entities[0]  # TODO !
                    entity_symbol = self._get_entity_symbol(entity)
                    char_map[x, y] = entity_symbol
                elif self.visible_arr[x, y] == 1:
                    char_map[x, y] = "⬞"

        return char_map

    def pretty_print(self):
        char_map = self._char_map()
        char_map = np.pad(char_map, pad_width=1, mode='constant', constant_values="◻️")
        map_string = "\n".join(" ".join(row) for row in char_map)
        print(map_string, end="\n\n")

    def __repr__(self):
        return (
            "TomaszMap<"
            f"size={self.size},"
            f"agent_position={self.agent.position},"
            f"lasers={len(self.lasers)},"
            f"bullets={len(self.bullets)},"
            f"tanks={len(self.tanks)},"
            f"mines={len(self.mines)},"
            f"items={len(self.items)},"
            f"zones={len(self.zones)},"
            ">"
        )
    
    def _get_entity_symbol(self, entity_dict: dict):
        entity_type = entity_dict['type']
        
        if entity_type == 'wall':
            return "■"
        elif entity_type == 'laser':
            return "|" if entity_dict['ori'] is Orientation.HORIZONTAL else "-"
        elif entity_type == 'double_bullet' or entity_type == 'bullet':
            return self._bullet_direction_symbol(entity_dict['dir'], entity_type == 'double_bullet')
        elif entity_type == 'agent_tank':
            return "✪"
        elif entity_type == 'player_tank':
            return "◯"
        elif entity_type == 'mine':
            return "x" if entity_dict['exploded'] else "X"
        elif entity_type in ["item_double_bullet", "item_laser", "item_mine", "item_radar"]:
            return self._item_symbol(entity_type)

        return "?"

    def _bullet_direction_symbol(self, direction, is_double):
        if is_double:
            return {
                Direction.UP: "⇈",
                Direction.RIGHT: "⇉",
                Direction.DOWN: "⇊",
                Direction.LEFT: "⇇"
            }.get(direction, "?")
        else:
            return {
                Direction.UP: "↑",
                Direction.RIGHT: "→",
                Direction.DOWN: "↓",
                Direction.LEFT: "←"
            }.get(direction, "?")

    def _item_symbol(self, item_type: str):
        return {
            "item_double_bullet": "D",
            "item_laser": "L",
            "item_mine": "M",
            "item_radar": "R"
        }.get(item_type, "?")

    def to_json(self) -> str:
        data = {
            'walls': self.walls,  # Convert NumPy array to list for JSON serialization
            'visible': self.visible,
            'lasers': self.lasers,
            'bullets': self.bullets,
            'tanks': self.tanks,
            'mines': self.mines,
            'items': self.items,
            'zones': self.zones
        }
        return json.dumps(data)
    