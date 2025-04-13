"""
A test script to plot demos
"""

from awpy import Demo
import polars as pl
from awpy.plot import plot, gif, PLOT_SETTINGS
from sys import argv
from tqdm import tqdm

TICKS_PER_SECOND=64

def demo_gif(path, frames_per_second=10, round_num=1):
    """
    There are two values we care about
    - frames_per_second: how often do we plot to the gif
    - ticks_per_sec
    """
    frame_duration = 1/frames_per_second
    # Warning: this may be imprecise
    ticks_per_frame = int(frame_duration * TICKS_PER_SECOND)
    dem = Demo(path, verbose=False)
    dem.parse(player_props=["health", "armor_value", "pitch", "yaw"])

    map_name = dem.header.get('map_name')
    frames = []


    for tick in tqdm(dem.ticks.filter(pl.col("round_num") == round_num)["tick"].unique().to_list()[::ticks_per_frame]):
        frame_df = dem.ticks.filter(pl.col("tick") == tick)
        frame_df = frame_df[
            ["X", "Y", "Z", "health", "armor", "pitch", "yaw", "side", "name"]
        ]

        points = []
        point_settings = []

        for row in frame_df.iter_rows(named=True):
            points.append((row["X"], row["Y"], row["Z"]))

            # Determine team and corresponding settings
            settings = PLOT_SETTINGS[row["side"]].copy()

            # Add additional settings
            settings.update(
                {
                    "hp": row["health"],
                    "armor": row["armor"],
                    "direction": (row["pitch"], row["yaw"]),
                    "label": row["name"],
                }
            )

            point_settings.append(settings)

        frames.append({"points": points, "point_settings": point_settings})
    gif(map_name, frames, "plot.gif", duration=frame_duration)

def main():
    print("demo path", argv[1])
    demo_gif(argv[1])

if __name__ == "__main__":
    main()
