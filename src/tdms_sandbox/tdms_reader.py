from pathlib import Path
import matplotlib.pyplot as plt
from nptdms import TdmsFile
from tdms_sandbox.tdms_functions import find_channel, select_sample_range



def main() -> None:
    file_path = Path(input("TDMS file path: ").strip().strip('"'))
    if not file_path.is_file():
        raise FileNotFoundError(f"TDMS file not found: {file_path}")

    tdms = TdmsFile.read(str(file_path))
    groups = tdms.groups()
    print("\nChannels in file:")
    all_channels = get_channels(tdms)
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