from tomasz.map import TomaszMap
import numpy as np

from tomasz.map.danger_map import get_danger, visualize_danger

import logging
log = logging.getLogger(__name__)
log.disabled = False


class TomaszMapWithHistory(TomaszMap):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticks_since_seen = np.full(self.size, np.inf, dtype=int)
        self.last_danger_map_change = 0
        #self.max_ticks_since_seen = 10
        self.danger = np.zeros(self.size)

        self.lasers = [{**laser, "ticks_since_seen": 0} for laser in self.lasers]
        self.bullets = [{**bullet, "ticks_since_seen": 0} for bullet in self.bullets]
        self.tanks = [{**tank, "ticks_since_seen": 0} for tank in self.tanks]
        self.mines = [{**mine, "ticks_since_seen": 0} for mine in self.mines]
        self.items = [{**item, "ticks_since_seen": 0} for item in self.items]
        
    def update(self, new_map: TomaszMap):
        self._update_entities_lists(new_map)
        self._update_entities_grid(new_map)
        self._update_clenup()
        self._update_danger()
        self.game_state = new_map.game_state

    def _update_entities_lists(self, new_map: TomaszMap):
        # walls don't change
        self.zones = new_map.zones
        self.agent = new_map.agent
        self.visible = new_map.visible
        self.visible_arr = new_map.visible_arr

        self.lasers = []
        self.bullets = []
        self.tanks = []
        self.mines = []
        self.items = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for ent in self.entities_grid[i, j]:
                    since_seen = int(self.ticks_since_seen[i, j])
                    if since_seen < 0:
                        since_seen = 31337
                        #ovefrflow fix
                    if ent['type'] == 'laser':
                        self.lasers.append({**ent, "ticks_since_seen": since_seen})
                    elif ent['type'] == 'bullet':
                        self.bullets.append({**ent, "ticks_since_seen": since_seen})
                    elif ent['type'] == 'tank':
                        self.tanks.append({**ent, "ticks_since_seen": since_seen})
                    elif ent['type'] == 'mine':
                        self.mines.append({**ent, "ticks_since_seen": since_seen})
                    elif ent['type'] == 'item':
                        self.items.append({**ent, "ticks_since_seen": since_seen})
    
    def _update_entities_grid(self, new_map: TomaszMap):
        # TODO bullets and lasers may need special handling
        self.ticks_since_seen += 1
        for (x, y) in new_map.visible:
            self.ticks_since_seen[x, y] = 0
            self.entities_grid[x, y] = []

        for entity in new_map.iter_entities():
            x, y = entity['pos']
            self.ticks_since_seen[x, y] = 0

            self.entities_grid[x, y] = [entity]

    def _update_clenup(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.ticks_since_seen[x, y] > 0 and len(self.entities_grid[x, y]) > 0:
                    entities = self.entities_grid[x, y]
                    entity = entities[0]

                    if entity['type'] in ['bullet', 'laser']:
                        # we dont want to remember bullets and lasers that are not visible
                        self.entities_grid[x, y] = []
                    if entity['type'] == 'tank' and entity['agent']:
                        # we dont want to remember our own previous position
                        self.entities_grid[x, y] = []

    def _update_danger(self):
        danger = get_danger(self)
        if np.any(self.danger - danger != 0): 
            log.info("Danger map has changed")
            # danger map has changed
            self.last_danger_map_change = 0
        else:
            self.last_danger_map_change += 1

        self.danger = danger
            
        return 

    def __repr__(self):
        return (
            "TomaszMapWithHistory<"
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
    
    def pretty_print(self):
        danger_map = get_danger(self)
        char_map = visualize_danger(danger_map)

        og_char_map = self._char_map()
        
        char_map = np.hstack((og_char_map, char_map))

        char_map = np.pad(char_map, pad_width=1, mode='constant', constant_values="◻️")
        map_string = "\n".join(" ".join(row) for row in char_map)
        print(map_string, end="\n\n")

