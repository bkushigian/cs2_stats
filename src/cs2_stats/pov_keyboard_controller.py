from typing import List
from pynput.keyboard import Controller, Key
from argparse import ArgumentParser
import time


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "first_half_ticks",
        type=int,
        help="ticks in the first half. The base key to refocus on player will change when sides switch",
    )
    parser.add_argument(
        "pov_key",
        type=int,
        help="key to press during demo review to keep POV on player after respawn. Should be in 1, 2, ..., 9, 0",
    )
    parser.add_argument(
        "--start_delay",
        default=5.0,
        type=float,
        help="seconds to delay before starting",
    )
    parser.add_argument(
        "--key_press_frequency",
        default=1.0,
        type=float,
        help="frequency (in seconds) with which to press the key to refocus on player",
    )
    parser.add_argument(
        "--ticks_per_second", default=64, help="Number of ticks in a second"
    )
    parser.add_argument(
        "--start_recording", default=None, action="Key to start recording"
    )
    parser.add_argument(
        "--stop_recording", default=None, action="Key to stop recording"
    )
    args = parser.parse_args()
    first_half_time = args.first_half_ticks / args.ticks_per_second
    run(args.pov_key, first_half_time, args.key_press_frequency, args.start_delay)


def run(
    pov_key: int,
    side_switch_times: float | List[float],
    key_press_frequency=1.0,
    delay: float = 5.0,
):

    if pov_key < 0 or pov_key > 9:
        raise RuntimeError(f"Illegal pov_key {pov_key}: must be in [0..9]")

    print("Start delay...")
    time.sleep(delay)
    print("Starting pov key")
    t0 = time.time()
    kb = Controller()
    t = time.time()

    key = str(pov_key)

    while t - t0 < side_switch_times:
        t = time.time()
        kb.press(key)
        kb.release(key)
        print(f"[1st Half] Pressed key {key} at demo time {t - t0:3.1f}s")
        time.sleep(key_press_frequency)

    key = str((pov_key + 5) % 10)

    while True:
        t = time.time()
        kb.press(key)
        kb.release(key)
        print(
            f"[2nd Half] Pressed key {key} at demo time {t - t0:3.1f}s    (Ctrl+C To Quit)"
        )
        time.sleep(key_press_frequency)


if __name__ == "__main__":
    main()
