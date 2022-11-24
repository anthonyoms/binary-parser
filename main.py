# Script to read and parse binary file.
import json
import numpy as np

last_position = 0


def parse_binary_file(path: str):
    # Load file into memory
    with open(path, 'rb') as f:
        data = f.read()

    # File size
    file_size = len(data)

    def get_data_chunk(byte_amount: int):
        global last_position
        x = data[last_position:last_position + byte_amount]
        last_position = last_position + byte_amount
        return x

    # Get first 6 bytes
    magic_key = get_data_chunk(6)

    x = int.from_bytes(get_data_chunk(2), byteorder='little')
    y = int.from_bytes(get_data_chunk(2), byteorder='little')

    number_of_triggers_per_pixel = int.from_bytes(get_data_chunk(2), byteorder='little')
    number_of_frames = int.from_bytes(get_data_chunk(2), byteorder='little')
    description_length = int.from_bytes(get_data_chunk(2), byteorder='little')
    description = get_data_chunk(description_length - 1).decode('utf-8')
    pixel_data_pointer = int.from_bytes(get_data_chunk(x * y * number_of_frames * 8), byteorder='little')

    print(f'File size: {file_size}')
    print(f'Magic key: {magic_key}')
    print(f'X: {x}')
    print(f'Y: {y}')
    print(f'Number of triggers per pixel: {number_of_triggers_per_pixel}')
    print(f'Number of frames: {number_of_frames}')
    print(f'Description length: {description_length}')
    print(f'Description: {description}')

    triggers = []

    # Get Single trigger header data.
    while (last_position < file_size):
        trigger_number = int.from_bytes(get_data_chunk(4 + 1), byteorder='little')
        time_from_last_trigger = int.from_bytes(get_data_chunk(2), byteorder='little')
        number_of_pulses = int.from_bytes(get_data_chunk(2), byteorder='little')
        time_offset = int.from_bytes(get_data_chunk(2), byteorder='little')
        width = int.from_bytes(get_data_chunk(2), byteorder='little')
        peak_value = int.from_bytes(get_data_chunk(2), byteorder='little')

        triggers.append({
            'trigger_number': trigger_number,
            'time_from_last_trigger': time_from_last_trigger,
            'number_of_pulses': number_of_pulses,
            'time_offset': time_offset,
            'width': width,
            'peak_value': peak_value
        })

        # print(f'Trigger number: {trigger_number}')
        # print(f'Time from last trigger: {time_from_last_trigger}')
        # print(f'Number of pulses: {number_of_pulses}')
        # print(f'Time offset: {time_offset}')
        # print(f'Width: {width}')
        # print(f'Peak value: {peak_value}')
        #
        # print(f'Pointer position: {last_position}')

    #     Find trigger by trigger number with binary search
    print("=========================================")
    query_number = 138320
    trigger = next((x for x in triggers if x['trigger_number'] == query_number), None)
    if trigger is None:
        print(f"Trigger {query_number} not found")
    else:
        print(f" What is the Time Offset at trigger number 138320? {trigger['time_offset']}")

    # Find the most common time offset
    time_offsets = [x['time_offset'] for x in triggers]
    unique, counts = np.unique(time_offsets, return_counts=True)
    most_common_time_offset = unique[np.argmax(counts)]
    print(f" What is the most common Time Offset? {most_common_time_offset}")

    #     save json to file
    with open('triggers.json', 'w') as f:
        f.write(json.dumps(triggers))
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_binary_file('./data.bin')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/