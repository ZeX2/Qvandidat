# Roadmap

- [ ] Solve the Exact cover NP-problem presented in Pontus memo
  - [x] Using cirq
  - [x] Using qiskit
  - [ ] Generate data
    - [ ] using depolarization noise models with varying probabilities
    - [ ] using phase flip and phase damp noise models with varying probabilities
- [ ] Solve the equal size partition problem (mock problem)
  - [ ] Using cirq
  - [x] Using qiskit
  - [ ] Generate data
    - [ ] using depolarization noise models with varying probabilities
    - [ ] using phase flip and phase damp noise models with varying probabilities
- [ ] Present results and ask questions
- [ ] Compare the noise with and without `circuit-group's` custom gates
- [ ] Implement an interface for a classical optimizer


## Plan

* Fix the qiskit implementation of the Exact cover problem
  * I double checked the gate sequence and remove the noise but we still get the wrong energy landscape.
* Generate data for Exact cover
* Implement mock problem (steal most of the code from the problem group)
  * [some random blog post](https://jasonrudolph.com/blog/2009/02/25/git-tip-how-to-merge-specific-files-from-another-branch/); just do `git checkout branch_name paths`
* Generate data for the mock prblem
* Present results


## Notes

### Cirq is slow

Cirq is really slow when running with the depolarize gates compared. Removing the depolarizing gates makes it fast, but they are needed for our simulations. Qiskit has no problem to be simulated with noise (but it may not be applied?), but we should also add depolarizing gates to our qiskit circuit to see if it is the depolarizing gates that are slow in cirq or if qiskits noise model just is superior in terms of speed. 

As of now running Qiskit with 50x50 angles and 500 repetitions takes a couple of seconds while the cirq implementation runs forever (at 4/50 after more than 5mins...).

### Wanted features

* A single function to execute to add noise in cirq, as of now a noise gate is added manually after each normal gate (there are more fun things to do than adding gates by hand!). 
* Move stuff regarding Exact cover and the mock problem to separeate folders, try to factor out common methods (like the bruteforce plot and the cirq add noise feature above if implemented)

### When generating data

Change the probability p in an interval, eg. change `fidelity` from 0.5 to 1 with a stepsize of 0.01.

Measure difference in noise by comparing how much the energy landscape changed compared to simulations without noise.

Run QAOA and see if we still reach the same angles. Does the optimizer take the same path?

The approximation ratio Pontus used in his Matlab code as an measurement of error.


### Questions to ask

Are the simulations we've run sufficient? (once we've runned them)

Are there any other noise models we want to simulate?

How do we choose the probability p for phase flip and phase damp? (I guess we'll use the same proceedure as for the depolarizing gates for now)

 
