import cirq
from exact_cover_pontus_probability import calculate_probability
from exact_cover_pontus_cost_function import cost_function
from cirq import Simulator

# TODO
#  noisy = circuit.with_noise(cirq.depolarize(p))
#  Implement with noise, reqarding dimension parameter d.


def expectation_value(gamma, beta, repetitions=50):

    q1 = cirq.LineQubit(1)
    q2 = cirq.LineQubit(2)

    rxg = cirq.rx(gamma)
    rzg = cirq.rz(gamma)
    rx2b = cirq.rx(2*beta)

    p1 = calculate_probability(0.99, 2)
    p2 = calculate_probability(0.99, 4)

    dn1 = cirq.depolarize(p1)
    dn2 = cirq.depolarize(p2)

    circuit = cirq.Circuit(
        cirq.H(q1),
        dn1(q1),
        rxg(q2),
        dn1(q2),
        cirq.CZ(q1, q2),
        dn2(q1),
        dn2(q2),
        rzg(q1),
        dn1(q1),
        cirq.H(q2),
        dn1(q2),
        rx2b(q1),
        dn1(q1),
        rx2b(q2),
        dn1(q2),
        cirq.measure(q1, q2),
    )

    simulator = Simulator()

    results = simulator.run(circuit, repetitions=repetitions)

    C = 0
    for result in results.measurements['1,2']:
        C += cost_function(result[0], result[1])

    return C/len(results.measurements['1,2'])


print(expectation_value(0, 0, 50))
