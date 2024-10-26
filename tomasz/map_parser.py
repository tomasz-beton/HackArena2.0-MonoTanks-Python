from hackathon_bot import *
import json
import numpy as np

class TomaszMap:
    def __init__(self, game_map):
        self.walls = []
        self.visible = []
        self.walls_arr = np.zeros((len(game_map.tiles), len(game_map.tiles[0])), dtype=int)
        self.visible_arr = np.zeros((len(game_map.tiles), len(game_map.tiles[0])), dtype=int)
        self.lasers = []
        self.bullets = []
        self.tanks = []
        self.mines = []
        self.items = []
        self.zones = {}
        
        self._extract_map_data(game_map)

    def _add_entity(self, entity, x, y):
        if isinstance(entity, Wall):
            self.walls.append((x, y))
            self.walls_arr[y, x] = 1
        elif isinstance(entity, Laser):
            self.lasers.append({'type': 'laser', 'pos': (x, y), 'ori': entity.orientation})
        elif isinstance(entity, DoubleBullet):
            self.bullets.append({'type': 'double_bullet', 'pos': (x, y), 'dir': entity.direction})
        elif isinstance(entity, Bullet):
            self.bullets.append({'type': 'bullet', 'pos': (x, y), 'dir': entity.direction})
        elif isinstance(entity, AgentTank):
            self.tanks.append({'type': 'agent_tank', 'pos': (x, y)})
        elif isinstance(entity, PlayerTank):
            self.tanks.append({'type': 'player_tank', 'pos': (x, y)})
        elif isinstance(entity, Mine):
            self.mines.append({'type': 'mine', 'pos': (x, y), 'exploded': entity.exploded})
        elif isinstance(entity, Item):
            self.items.append({'type': entity.type, 'pos': (x, y)})

    def _add_zone(self, zone, x, y, is_visible):
        idx = chr(zone.index)
        if idx not in self.zones:
            self.zones[idx] = {'idx': idx, 'pos': [(x, y)], 'vis_mask': [is_visible],'upper_left':  (x, y), 'lower_right':  (x, y)}

        self.zones[idx]["pos"].append((x, y))
        self.zones[idx]["vis_mask"].append(is_visible)
        self.zones[idx]["upper_left"] = (min(self.zones[idx]["upper_left"][0], x), min(self.zones[idx]["upper_left"][1], y))
        self.zones[idx]["lower_right"] = (max(self.zones[idx]["lower_right"][0], x), max(self.zones[idx]["lower_right"][1], y))

    def _extract_map_data(self, game_map):
        for x, row in enumerate(game_map.tiles):
            for y, tile in enumerate(row):
                if tile.is_visible:
                    self.visible.append((x, y))
                    self.visible_arr[x, y] = 1

                if tile.zone:
                    self._add_zone(tile.zone, x, y, is_visible=tile.is_visible)

                for entity in tile.entities:
                    self._add_entity(entity, x, y)

    def pretty_print(self):
        end = " "
        for x, row in enumerate(self.walls_arr):
            for y, wall in enumerate(row):
                if wall == 1:
                    print("■", end=end)
                else:
                    entity_symbol = self._get_entity_symbol(x, y)
                    print(entity_symbol, end=end)
            print()

    def __repr__(self):
        return (
            f"TomaszMap<walls={len(self.walls)},lasers={len(self.lasers)},"
            f"bullets={len(self.bullets)},tanks={len(self.tanks)},"
            f"mines={len(self.mines)},items={len(self.items)},zones={len(self.zones)}>"
        )
    
    def _get_entity_symbol(self, x, y):
        for laser in self.lasers:
            if laser['pos'] == (x, y):
                return "|" if laser['orientation'] is Orientation.HORIZONTAL else "-"

        for bullet in self.bullets:
            if bullet['pos'] == (x, y):
                return self._bullet_direction_symbol(bullet['dir'], bullet['type'] == 'double_bullet')

        for tank in self.tanks:
            if tank['pos'] == (x, y):
                return "A" if tank['type'] == 'agent_tank' else "P"

        for mine in self.mines:
            if mine['pos'] == (x, y):
                return "x" if mine['exploded'] else "X"

        for item in self.items:
            if item['pos'] == (x, y):
                return self._item_symbol(item['type'])

        for zone in self.zones.values():
            if (x, y) in zone['pos']:
                if zone['vis_mask'][zone['pos'].index((x, y))]:
                    return zone["idx"].upper()
                else:
                    return zone["idx"].lower()
        
        if x < 0 or y < 0 or x >= self.visible_arr.shape[0] or y >= self.visible_arr.shape[1]:
            print(f"Out of bounds: {x}, {y}")
            return "⛝"
        
        if self.visible_arr[x, y] == 1:
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