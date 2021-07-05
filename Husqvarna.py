
DIRECTIONS_LIST = [(0, 1), (1, 0), (0, -1), (-1, 0)]

DIRECTIONS = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0)
}

ACTIONS = ['A', 'G', 'D']


class Mower:
    def do_action(self):
        coord = 0 if self.direction[0] else 1
        step = self.direction[0] if self.direction[0] else self.direction[1]
        if self.position[coord] + step <= self.lawn_size[coord]:
            self.position[coord] += step

    def turn_left(self):
        direction_index = DIRECTIONS_LIST.index(self.direction)
        self.direction = DIRECTIONS_LIST[(direction_index - 1) % len(DIRECTIONS_LIST)]

    def turn_right(self):
        direction_index = DIRECTIONS_LIST.index(self.direction)
        self.direction = DIRECTIONS_LIST[(direction_index + 1) % len(DIRECTIONS_LIST)]

    def decrypt_position(self, message):
        x = int(message.split(" ")[0][0])
        y = int(message.split(" ")[0][0])
        direction = DIRECTIONS[message.split(" ")[1][0]]

        return [x, y], direction

    def to_string(self, position, direction):
        position = "".join([str(i) for i in position])
        direction = [k for k, v in DIRECTIONS.items() if v == direction][0]
        return f"===> {position} {direction}"

    def __init__(self, positon_message, lawn_size):
        self.position = self.decrypt_position(positon_message)[0]
        self.direction = self.decrypt_position(positon_message)[1]
        self.lawn_size = (int(lawn_size[:len(lawn_size)//2]), int(lawn_size[len(lawn_size)//2:]))
        self.actions = {
            "A": self.do_action,
            "G": self.turn_left,
            "D": self.turn_right,
        }

    def mow(self, seq):
        for step in seq:
            self.actions[step]()
        return self.to_string(self.position, self.direction)


def parse_and_launch_file():
    try:
        with open("mower_steps.txt", "r") as mower_file:
            message = ""
            seq_mowing = ""
            up_right_coord = ""
            steps = mower_file.readlines()
            for line in steps:
                line = line.strip()
                if any(direction in line for direction in list(DIRECTIONS.keys())):
                    message = line
                elif any(action in line for action in ACTIONS):
                    seq_mowing = line
                elif line.isdigit():
                    up_right_coord = line

                if message and seq_mowing and up_right_coord:
                    print(message)
                    print(seq_mowing)
                    mower = Mower(message, up_right_coord)
                    final_position = mower.mow(seq_mowing)
                    print(final_position)
                    message = ""
                    seq_mowing = ""
                    print("******************")
    except OSError:
        raise ("File not Found !")


if __name__ == '__main__':
    parse_and_launch_file()