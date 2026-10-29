"""
That a surface with a degenerate spot draws no black where it has one.

A surface's normals come from the directions it runs in from each point of its grid. Where
those directions are zero, as at the pole of a sphere, the normal is worked out from the
neighboring rows and columns instead, see grid_tangent in surface_mesh.wgsl. A sphere of three
rows has its first and last rows at the same meridian, so across them the middle row gets
nowhere, and a normal which comes out not a number draws black. Plain and textured surfaces
share that path, so both are drawn.

Nothing about the picture can be checked without a reference, so: render the two spheres,
and count the pixels where a sphere is drawn which are near black. A sphere which drew
nothing at all fails too, so that a framing which misses them cannot pass.

    python tests/surface_normals.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image


WORK = Path("/tmp/manimgl-surface-normals")
# A pixel whose channels all stay under this is black. Nothing lit comes out that dark: the
# least bright texel here is 128 in blue, and shading takes at most two fifths of it away
BLACK = 20
# How many pixels a sphere has to cover for it to count as drawn
MIN_DRAWN = 200

SCENE = '''
from manimlib import *


class DegenerateSpheres(ThreeDScene):
    """Spheres of three by three points, see surface_normals.py"""

    def construct(self):
        self.frame.set_euler_angles(theta=55 * DEGREES, phi=70 * DEGREES)
        self.frame.scale(0.5)
        textured = TexturedSurface(
            Sphere(radius=1.0, resolution=(3, 3)), "TEXTURE_PATH"
        )
        plain = Sphere(radius=1.0, resolution=(3, 3)).set_color(BLUE)
        textured.shift(LEFT * 1.5)
        plain.shift(RIGHT * 1.5)
        self.add(textured, plain)
        self.wait(0.1)
'''


def render() -> np.ndarray:
    subprocess.run(
        ["manimgl", str(WORK / "scenes.py"), "DegenerateSpheres", "-w", "-s", "-l",
         "--config_file", str(WORK / "empty.yml"), "--video_dir", str(WORK)],
        check=True, capture_output=True, text=True,
    )
    image = Image.open(WORK / "DegenerateSpheres.png").convert("RGB")
    return np.asarray(image, dtype=int)


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    texture = WORK / "texture.png"
    y, x = np.mgrid[0:256, 0:512]
    stripes = ((x // 32 + y // 32) % 2) * 127 + 128
    Image.fromarray(np.stack([x // 2, y, stripes], axis=-1).astype(np.uint8)).save(texture)
    (WORK / "scenes.py").write_text(SCENE.replace("TEXTURE_PATH", str(texture)))
    (WORK / "empty.yml").write_text("")

    image = render()
    background = image[0, 0]
    drawn = np.abs(image - background).max(axis=2) > BLACK
    half = image.shape[1] // 2
    failures = []

    for side, covered in (("textured", drawn[:, :half].sum()), ("plain", drawn[:, half:].sum())):
        print(f"  {side} sphere of 3x3 points covers {covered} pixels")
        if covered < MIN_DRAWN:
            failures.append(f"the {side} sphere covers only {covered} pixels, so it was not drawn")

    dark = int((drawn & (image.max(axis=2) < BLACK)).sum())
    print(f"  near black pixels where the spheres are drawn: {dark}")
    if dark:
        failures.append(
            f"{dark} pixels of a sphere with a degenerate spot are black, where its normals "
            f"could not be worked out"
        )

    for failure in failures:
        print(f"  FAIL: {failure}")
    if not failures:
        print("  spheres with degenerate spots are drawn without black")
    return 1 if failures else 0


sys.exit(main())
