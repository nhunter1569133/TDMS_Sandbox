from __future__ import annotations
from nptdms import TdmsFile, TdmsChannel

import numpy as np

###
### get_channels
###
def get_channels(
    tdms_file: TdmsFile
) -> list[tuple[str, str, TdmsChannel]]:
    """
    Arguments:
        tdms_file: The TDMS file object.

    Returns:
        A list of tuples containing group name, channel name, and channel object.
    """
    channels = []
    for group in tdms_file.groups():
        for channel in group.channels():
            channels.append((group.name, channel.name, channel))
    return channels
###
### ......................... get_channels ............................

### 
### find_channel
###
def find_channel(
    channels: list[tuple[str, str, TdmsChannel]], 
    channel_name: str, 
    role: str
) -> TdmsChannel:
    """
    Arguments:
        channels: List of tuples containing group name, channel name, and channel object.
        channel_name: Name of the channel to find.
        role: Role of the channel (used in error messages).

    Returns:
        The channel object corresponding to the specified channel name.
    """
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
###
### .............................. find_channel ....................................


###
### select_sample_range
###
def select_sample_range(
    signal: np.ndarray, 
    start_sample: int, 
    end_sample: int
) -> tuple[np.ndarray, np.ndarray]:
    if start_sample < 1:
        raise ValueError("Sample numbers start at 1.")
    if start_sample > end_sample:
        raise ValueError("The first sample number must not exceed the last.")
    if end_sample > len(signal):
        raise ValueError(f"The last sample number cannot exceed {len(signal)}.")

    sample_numbers = np.arange(start_sample, end_sample + 1)
    return sample_numbers, signal[start_sample - 1 : end_sample]
###
### .............................. select_sample_range ....................................