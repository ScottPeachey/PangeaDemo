import math
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any, Union
from PIL import Image, ImageDraw
import logging

logger = logging.getLogger()


@dataclass
class Point:
    x: float
    y: float
    z: float

    def __add__(self, other: Union["Point", int, float]) -> "Point":
        if type(other) == int or type(other) == float:
            point = Point(self.x + other, self.y + other, self.z + other)
        elif type(other) == Point:
            point = Point(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError(f"unsupported operand type(s) for +: '{type(self)}' and '{type(other)}'")
        return point

    def __sub__(self, other: Union["Point", int, float]) -> "Point":
        if type(other) == int or type(other) == float:
            point = Point(self.x - other, self.y - other, self.z - other)
        elif type(other) == Point:
            point = Point(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError(f"unsupported operand type(s) for -: '{type(self)}' and '{type(other)}'")
        return point

    def __mul__(self, other: Union[int, float]):
        if type(other) != int and type(other) != float:
            raise TypeError(f"unsupported operand type(s) for *: '{type(self)}' and '{type(other)}'")
        return Point(self.x * other, self.y * other, self.z * other)

    def __str__(self):
        return f"Point({self.x}, {self.y}, {self.z})"

    def rotate_z(self, angle: Union[int, float]) -> "Point":
        """Rotate points around the z axis by angle in radians"""
        return Point(
            self.x * math.cos(angle) - self.x * math.sin(angle),
            self.y * math.sin(angle) + self.y * math.cos(angle),  # this line was causing the error
            self.z,
        )

    def norm(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def list(self) -> List[Union[int, float]]:
        return [self.x, self.y, self.z]


def world_to_camera(point: "Point", camera: Dict[str, Any]) -> "Point":
    """Transforms a point to coordinates with the camera at the origin and the x-axis perpendicular to the image
    axis towards the focus."""

    # TODO: there appears to be a bug in this implementation / error found in rotate_z()
    pos = camera["pos"]
    f = camera["f"]
    theta = math.atan2(pos.y, -pos.x)
    point_in_cam_coords = (point - pos).rotate_z(theta)
    x = point_in_cam_coords.x
    y = point_in_cam_coords.y
    z = point_in_cam_coords.z
    scale = x / f
    camera_point = Point(scale * z, scale * y, scale)
    return camera_point


def render_points(
    points: List["Point"],
    view: Dict[str, float],
    fit_params: Dict[str, "Point"] = None,
    dims: Tuple[int, int] = (320, 320),
) -> Image.Image:
    """Creates an image of the points and the fitted plane from the view of the camera at a position given in view.
    The view dictionary defines the position of the camera in the x,y plane by an angle in radians and a distance
    that, the camera points towards the origin."""

    img = Image.new("RGB", dims)
    img_draw = ImageDraw.Draw(img)
    rotation = view["rotation"]
    distance = view["distance"]
    camera_position = Point(distance * math.cos(rotation), distance * math.sin(rotation), 0)
    camera = {"pos": camera_position, "f": view["focal_length"] / 1000}  # pos - camera position, f - focal length in m
    if fit_params:
        # TODO: implement colouring of the image using the distance to the plane. Also add in transparency for points
        #  behind the plan and opacity for points in front of the plane
        pass
    for point in points:
        # TODO: sort points along camera axis to get display ordering correct when drawing
        point_in_image = world_to_camera(point, camera)
        size = 100 / point_in_image.z
        logger.debug(f"World {point}: size {size} at {point_in_image}")
        y = point_in_image.x + dims[0] // 2
        x = point_in_image.y + dims[1] // 2
        img_draw.ellipse((x - size, y - size, x + size, y + size), fill=(250, 0, 0), outline=(0, 255, 0))
    return img


def fit_points(points: List[Tuple[float, float, float]]) -> Dict[str, Union[float, "Point"]]:
    """Takes a  list of input points and calculates the plane of best fit."""
    # TODO: implementation to return plane defined by normal and distance from origin along the normal
    distance = 0.0
    normal = Point(1, 0, 0)
    normal = normal * (1 / normal.norm())
    return {"distance": distance, "normal": normal}


if __name__ == "__main__":
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    req_data = {
        "points": [
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (-1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, -1.0, 0.0),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, -1.0),
        ],
        "params": {"rotation": 0, "distance": 2.0, "focal_length": 50.0},
    }
    points_in = [Point(*p) for p in req_data["points"]]
    img_out = render_points(points_in, req_data["params"])
    # TODO: should show up as:
    #
    #        o
    #
    #    o   0   o
    #
    #        o

    img_out.show()


