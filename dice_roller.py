from random import randint


def roll_d20(with_advantage: bool=False) -> int:
    return randint(1,20) if not with_advantage else max([randint(1,20), randint(1, 20])

def roll_xdy(dice_str: str, individual_results: bool=False) -> int:
    dice_str = dice_str.lower()
    nums = [int(val) for val in dice_str.split('d')]
    result = [0] * nums[0]
    for i in range(nums[0]):
        result[i] = randint(1, nums[1])

    return sum(result) if not individual_results else result

