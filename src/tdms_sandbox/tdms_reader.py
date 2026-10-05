from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from nptdms import TdmsFile


def find_channel(
    channels: list[tuple[str, str, object]], channel_name: str, role: str
) -> object:
    matches = [entry for entry in channels if entry[1] == channel_name]
    if not matches:
        available = ", ".join(sorted({entry[1] for entry in channels}))
        raise ValueError(
            f"No {role} channel named {channel_name!r}. Available channel names: "
            f"{available}"
        )
    if len(matches) > 1:
        locations = ", ".join(f"{group}/{name}" for group, name, _ in matches)
        raise ValueError(
            f"Channel name {channel_name!r} is ambiguous; matches: {locations}"
        )
    return matches[0][2]


def select_sample_range(
    signal: np.ndarray, start_sample: int, end_sample: int
) -> tuple[np.ndarray, np.ndarray]:
    if start_sample < 1:
        raise ValueError("Sample numbers start at 1.")
    if start_sample > end_sample:
        raise ValueError("The first sample number must not exceed the last.")
    if end_sample > len(signal):
        raise ValueError(f"The last sample number cannot exceed {len(signal)}.")

    sample_numbers = np.arange(start_sample, end_sample + 1)
    return sample_numbers, signal[start_sample - 1 : end_sample]


def main() -> None:
    file_path = Path(input("TDMS file path: ").strip().strip('"'))
    if not file_path.is_file():
        raise FileNotFoundError(f"TDMS file not found: {file_path}")

    tdms = TdmsFile.read(str(file_path))
    groups = tdms.groups()
    print("\nChannels in file:")
    all_channels = []
    for group in groups:
        for channel in group.channels():
            entry = (group.name, channel.name, channel)
            all_channels.append(entry)
            print(f"  {group.name}/{channel.name} ({len(channel)} samples)")

    signal_name = input("Signal channel name: ").strip()
    signal_channel = find_channel(all_channels, signal_name, "signal")

    signal = signal_channel[:]
    start_sample = int(input("First sample number (1-based): ").strip())
    end_sample = int(input("Last sample number (inclusive): ").strip())
    sample_numbers, selected_signal = select_sample_range(
        signal, start_sample, end_sample
    )

    figure, axis = plt.subplots()
    axis.plot(sample_numbers, selected_signal)
    axis.set_xlabel("Sample number")
    axis.set_ylabel(signal_channel.name)
    axis.set_title(f"{signal_channel.group_name}/{signal_channel.name}")
    figure.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()