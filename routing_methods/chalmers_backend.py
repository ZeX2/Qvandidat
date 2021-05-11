# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Chalmers device (20 qubit).
"""

from qiskit.providers.models import (GateConfig, QasmBackendConfiguration)
from qiskit.test.mock.fake_backend import FakeBackend
from qiskit.transpiler import CouplingMap


class FakeChalmers(FakeBackend):
    """A fake 20 qubit backend."""

    def __init__(self):
        """
          00 ↔ 01 ↔ 02 ↔ 03 ↔ 04
           ↕    ↕    ↕    ↕   ↕
          05 ↔ 06 ↔ 07 ↔ 08 ↔ 09
           ↕   ↕    ↕    ↕     ↕
          10 ↔ 11 ↔ 12 ↔ 13 ↔ 14
           ↕    ↕   ↕    ↕     ↕
          15 ↔ 16 ↔ 17 ↔ 18 ↔ 19
        """
        coupling = CouplingMap()   
        cmap = coupling.from_grid(4, 5).get_edges()

        configuration = QasmBackendConfiguration(
            backend_name='fake_chalmers',
            backend_version='0.0.0',
            n_qubits=20,
            basis_gates=['rx', 'rz','iswap','cz','id'],
            simulator=False,
            local=True,
            conditional=False,
            open_pulse=False,
            max_shots = 100000,
            memory=False,
            gates=[GateConfig(name='TODO', parameters=[], qasm_def='TODO')],
            coupling_map=cmap,
        )

        super().__init__(configuration)

    def properties(self):
        """Returns a snapshot of device properties as recorded on 03/05/21.
        """
        return None