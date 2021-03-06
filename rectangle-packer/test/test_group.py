# MIT License
# 
# Copyright (c) 2017 Daniel Andersson
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Built-in
import random

# PyPI
import pytest

# Local
import minorminer._rpack as rpack


def test_flat():
    data = [3, 2, 1]
    # Todo: the order should not matter
    assert rpack.group(data, 3) == [[3], [2], [1]]


def test_nr_groups():
    with pytest.raises(ValueError):
        rpack.group([1], -1)
    with pytest.raises(ValueError):
        rpack.group([1], 0)
    data = list(range(1, 100))
    for nr_groups in range(1, 100):
        assert len(rpack.group(data, nr_groups)) == nr_groups


def test_empty_list():
    assert rpack.group([], 3) == [[], [], []]


def test_input_error():
    with pytest.raises(TypeError):
        rpack.group(None, 3)
    with pytest.raises(TypeError):
        rpack.group([1, 2, 3], None)
    with pytest.raises(TypeError):
        rpack.group(None, None)


def test_performance():
    groups = rpack.group(list(range(1_000)), 5)
    assert max(sum(g) for g in groups) == 99_900


def test_swap_complete():
    """Test that no further "swapping" will improve the result"""
    # Get random data
    data = [random.random() for _ in range(500)]
    nr_groups = random.randint(2, 15)
    # Figure out which group is the maximal-sum group
    groups = rpack.group(data, nr_groups)
    group_sums = [sum(g) for g in groups]
    max_duration = max(group_sums)
    group_id_max = group_sums.index(max_duration)
    max_group = groups[group_id_max]

    # For each element in max_group, try to swap element with other
    # elements in the other groups and check if the "max-group" can
    # be improved.
    for i in range(len(max_group)):
        for group_id, group in enumerate(groups):
            if group_id == group_id_max:
                # We don't want to swap within the same group
                continue
            for j in range(len(group)):
                # Swap
                group[j], max_group[i] = max_group[i], group[j]
                # Swap should not make any improvements
                group_sums = [sum(g) for g in groups]
                assert max(group_sums) >= max_duration
                # Undo swap
                group[j], max_group[i] = max_group[i], group[j]
