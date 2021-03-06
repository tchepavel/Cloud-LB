import copy
from VM import VM

class PM:
    def __init__(self, flavour=None):
        if flavour is None:
            self.traits = {
                "cpu": 4,
                "bw": 4,
                "ram": 4,
                "iops": 4
            }

            self.max_load = {
                "cpu": 0.9,
                "bw": 0.8,
                "ram": 0.9,
                "iops": 0.8
            }

            self.demand = {}
            for tr in self.traits:
                self.demand[tr] = 0

            self.vms = list()

    def check_vm(self, vm: VM):
        ok = True
        for tr in self.traits:
            if self.demand[tr] + vm.traits[tr] * vm.load[tr] > self.max_load[tr] * self.traits[tr]:
                ok = False
                break
        return ok

    def place_vm(self, vm: VM, idx: int):
        self.vms.append((copy.deepcopy(vm), idx))
        for tr in vm.traits:
            self.demand[tr] += vm.traits[tr] * vm.load[tr]

    def remove_vm(self, idx: int):
        i = 0
        while self.vms[i][1] != idx:
            i += 1
        vm, _ = self.vms.pop(i)

        for tr in self.traits:
            self.demand[tr] -= vm.traits[tr] * vm.load[tr]

    def update_vm(self, vm: VM, idx: int):
        curr_vm, ar_idx = self.vms[idx]
        for tr in vm.traits:
            self.demand[tr] -= curr_vm.traits[tr] * curr_vm.load[tr]

        for tr in vm.traits:
            self.demand[tr] += vm.traits[tr] * vm.load[tr]
        self.vms[idx] = (vm, ar_idx)

    def mean_load(self):
        sum_loads = 0
        for trait in self.traits:
            sum_loads += self.demand[trait] / (self.traits[trait] * self.max_load[trait])
        return sum_loads / len(self.traits)

    def max_relative_load(self):
        max_re_load = 0.
        for trait in self.traits:
            max_re_load = max(max_re_load, self.demand[trait] / (self.traits[trait] * self.max_load[trait]))
        return max_re_load

    def lol_load(self):
        return 0.5 * self.mean_load() + 0.5 * self.max_relative_load()

    def clear(self):
        for tr in self.traits:
            self.demand[tr] = 0
        self.vms = list()

    def is_overloaded(self):
        for tr in self.traits:
            if self.traits[tr] * self.max_load[tr] < self.demand[tr]:
                return True

        return False
