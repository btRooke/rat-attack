from typing import ClassVar, Optional, Dict, Type, Set
from curses import window
from .gameobject import GameObject
from .camera import Camera
import logging

def is_visible(o: GameObject):
    assert WorldManager.screen
    pos_x, pos_y = o.get_pos()
    cam_x, cam_y = Camera.get_pos()
    viewport, _ = WorldManager.screen.getmaxyx()

    return abs(pos_x - cam_x) < viewport / 2 and abs(pos_y - cam_y) < viewport / 2

class WorldManager:
    objects: ClassVar[list[GameObject]] = []
    screen: ClassVar[Optional[window]] = None

    @staticmethod
    def add_object(obj: GameObject):
        WorldManager.objects.append(obj)

    @staticmethod
    def update():
        Camera.update()

        for obj in WorldManager.objects:
            obj.update()

    @staticmethod
    def draw():
        if not WorldManager.screen:
            raise Exception("not initialised the screen")

        WorldManager.screen.refresh()

        coord_dict: Dict[tuple[int, int], list[GameObject]] = dict()

        for obj in WorldManager.objects:
            x, y = obj.get_pos()
            objs = coord_dict.get((x, y), [])
            objs.append(obj)
            objs.sort(key=lambda o: -o.zindex())
            coord_dict[(x,y)] = objs

        for objs in coord_dict.values():
            for obj in objs:
                obj.draw()

    @staticmethod
    def init(screen: window):
        WorldManager.screen = screen

    @staticmethod
    def _get_impassable_objects(x: int, y:int) -> list[GameObject]:
        return list(filter(lambda o: o.get_pos() == (x, y) and o.impassable(),
                           WorldManager.objects))

    @staticmethod
    def get_objects(x: int, y: int) -> list[GameObject]:
        return list(filter(lambda o: o.get_pos() == (x, y),
                           WorldManager.objects))

    """
    Determine if the given square is 'placeable'. Meaning that
    an object can be put on the square or the player can move
    to the square.
    """
    @staticmethod
    def can_place(x: int, y: int) -> int:
        return len(WorldManager._get_impassable_objects(x, y)) == 0

    @staticmethod
    def clear_cell(x: int, y: int):
        """
        clear all objects in the given location that is not the player
        """
        assert WorldManager.screen
        objs = WorldManager.get_objects(x, y)
        # all terrain is at zindex 0
        objs = list(filter(lambda o: o.zindex() == 0, objs))

        for obj in objs:
            logging.debug(f"Removed object {len(objs)}")
            WorldManager.objects.remove(obj)

    @staticmethod
    def get_objects_of_type(types: Set[Type]) -> list[GameObject]:
        return list(filter(lambda o: type(o) in types, WorldManager.objects))

    @staticmethod
    def get_visible_objects() -> list[GameObject]:
        return list((o for o in WorldManager.objects if is_visible(o)))

    @staticmethod
    def get_out_of_sight_objects() -> list[GameObject]:
        return list((o for o in WorldManager.objects if not is_visible(o)))

