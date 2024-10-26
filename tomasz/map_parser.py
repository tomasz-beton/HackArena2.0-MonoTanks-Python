from hackathon_bot import *
import numpy as np
from typing import List, Dict
import json

import json
import numpy as np
import json
import numpy as np

class TomaszMap:
    def __init__(self, game_map):
        # Extract data and store it in the instance
        self.walls = np.zeros((len(game_map.tiles), len(game_map.tiles[0])), dtype=int)
        self.visible = np.zeros((len(game_map.tiles), len(game_map.tiles[0])), dtype=int)
        self.lasers = []
        self.bullets = []
        self.tanks = []
        self.mines = []
        self.items = []
        self.zones = []
        
        self._extract_map_data(game_map)

    def _extract_map_data(self, game_map):
        for y, row in enumerate(game_map.tiles):
            for x, tile in enumerate(row):
                entity = tile.entities[0] if tile.entities else None

                if tile.is_visible:
                    self.visible[y, x] = 1

                # Walls
                if isinstance(entity, Wall):
                    self.walls[y, x] = 1
                
                
                # Lasers with orientation
                elif isinstance(entity, Laser):
                    self.lasers.append({
                        'type': 'laser',
                        'position': (x, y),
                        'orientation': entity.orientation
                    })
                
                # Bullets with direction
                elif isinstance(entity, DoubleBullet):
                    self.bullets.append({
                        'type': 'double_bullet',
                        'position': (x, y),
                        'direction': entity.direction
                    })
                elif isinstance(entity, Bullet):
                    self.bullets.append({
                        'type': 'bullet',
                        'position': (x, y),
                        'direction': entity.direction
                    })
                
                # Tanks (AgentTank or PlayerTank)
                elif isinstance(entity, AgentTank):
                    self.tanks.append({
                        'type': 'agent_tank',
                        'position': (x, y)
                    })
                elif isinstance(entity, PlayerTank):
                    self.tanks.append({
                        'type': 'player_tank',
                        'position': (x, y)
                    })
                
                # Mines with explosion status
                elif isinstance(entity, Mine):
                    self.mines.append({
                        'type': 'mine',
                        'position': (x, y),
                        'exploded': entity.exploded
                    })
                
                # Items with type
                elif isinstance(entity, Item):
                    self.items.append({
                        'type': entity.type,
                        'position': (x, y)
                    })
                
                # Zones with visibility
                elif tile.zone:
                    self.zones.append({
                        'index': tile.zone.index,
                        'position': (x, y),
                        'visible': tile.is_visible
                    })

    def pretty_print(self):
        end = " "
        for y, row in enumerate(self.walls):
            for x, wall in enumerate(row):
                if wall == 1:
                    print("■", end=end)
                else:
                    # Check for other entities based on position
                    entity_symbol = self._get_entity_symbol(x, y)
                    print(entity_symbol, end=end)
            print()

    def _get_entity_symbol(self, x, y):
        for laser in self.lasers:
            if laser['position'] == (x, y):
                return "|" if laser['orientation'] is Orientation.HORIZONTAL else "-"

        for bullet in self.bullets:
            if bullet['position'] == (x, y):
                return self._bullet_direction_symbol(bullet['direction'], bullet['type'] == 'double_bullet')

        for tank in self.tanks:
            if tank['position'] == (x, y):
                return "A" if tank['type'] == 'agent_tank' else "P"

        for mine in self.mines:
            if mine['position'] == (x, y):
                return "x" if mine['exploded'] else "X"

        for item in self.items:
            if item['position'] == (x, y):
                return self._item_symbol(item['type'])

        for zone in self.zones:
            if zone['position'] == (x, y):
                index = chr(zone['index'])
                return index.upper() if zone['visible'] else index.lower()
            
        if self.visible[y, x] == 1:
            return "⬞"

        return " "  # Default symbol for empty tiles

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

    def _item_symbol(self, item_type):
        return {
            SecondaryItemType.DOUBLE_BULLET: "D",
            SecondaryItemType.LASER: "L",
            SecondaryItemType.MINE: "M",
            SecondaryItemType.RADAR: "R"
        }.get(item_type, "?")

    def to_json(self) -> str:
        # Prepare data as dictionary for JSON serialization
        data = {
            'walls': self.walls.tolist(),  # Convert NumPy array to list for JSON serialization
            'lasers': self.lasers,
            'bullets': self.bullets,
            'tanks': self.tanks,
            'mines': self.mines,
            'items': self.items,
            'zones': self.zones
        }
        return json.dumps(data, indent=4)