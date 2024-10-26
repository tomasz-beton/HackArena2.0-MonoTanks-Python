from tomasz.map_parser import TomaszMap
import numpy as np


class TomaszMapWithHistory(TomaszMap):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticks_since_seen = np.full(self.size, np.inf, dtype=int)
        #self.max_ticks_since_seen = 10

    def update(self, new_map: TomaszMap):
        self._update_entities_lists(new_map)
        self._update_entities_grid(new_map)
        self._update_clenup()

    def _update_entities_lists(self, new_map: TomaszMap):
        # walls don't change
        self.zones = new_map.zones

        self.agent_position = new_map.agent
        self.visible = new_map.visible
        self.visible_arr = new_map.visible_arr

        self.lasers = new_map.lasers
        self.bullets = new_map.bullets
        self.tanks = new_map.tanks
        self.mines = new_map.mines
        self.items = new_map.items
    
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

                    if entity['type'] in ['bullet', 'laser', 'agent_tank', 'double_bullet']:
                        self.entities_grid[x, y] = []


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
