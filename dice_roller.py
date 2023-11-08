from random import randint


def roll_d20(with_advantage: bool=False, with_disadvantage: bool=False) -> int:
    if (not with_advantage and not with_disadvantage) or (with_advantage and with_disadvantage):
        return randint(1, 20)
    elif with_advantage:
        return max([randint(1,20), randint(1, 20)])
    else:
        return min([randint(1,20), randint(1, 20)])

def roll_xdy(dice_str: str, individual_results: bool=False) -> int:
    dice_str = dice_str.lower()
    nums = [int(val) for val in dice_str.split('d')]
    result = [0] * nums[0]
    for i in range(nums[0]):
        result[i] = randint(1, nums[1])

    return sum(result) if not individual_results else result

