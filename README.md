# ⚛️ Iraq Quantum Lab (IQL) - 51 Qubit Simulator

**Developer:** Jaafar Abdulsalam  
**Stage:** 2nd Stage - Cybersecurity Engineering  
**Institution:** Al-Hikma University College  
**Supervisor:** Prof. Dr. Alaa Al-Hamami (Head of Dept.)

## 📝 Abstract
This project is an advanced research and software platform designed to simulate a **51-Qubit Quantum Computing** environment. It focuses on modeling Shor's and Grover's algorithms to study the impact of quantum threats on classical RSA encryption. The simulator operates under realistic physical conditions by integrating the **IBM Eagle 51Q Noise Model**.

## 🛠️ Technical Stack
* **Quantum Engine:** Pure Python State-Vector simulation using Linear Algebra & Complex Hilbert Space.
* **Shor's Algorithm:** Full implementation of **QFT (Quantum Fourier Transform)** and **Continued Fractions** for period finding.
* **Noise Simulation:** Modeling Decoherence (T1, T2) and Gate Errors based on real **IBM Eagle** calibration data.
* **Backend:** FastAPI (Python) for heavy matrix computations and probability distributions.
* **Frontend:** Interactive UI displaying wave-function collapse, counts, and entropy (H(X)).

## 🔬 Scientific Contribution
As a self-taught cybersecurity student, this project demonstrates:
1. **Hybrid Quantum Simulation:** Bridging the gap between classical logic and quantum interference.
2. **Post-Quantum Analysis:** Visualizing how the period $r$ is extracted through phase estimation.
3. **Hardware Constraints:** Proving how noise levels affect the accuracy of Shor's algorithm in real-world processors.

## 📚 Academic References
* **Shor, P. W. (1997).** Polynomial-Time Algorithms for Prime Factorization.
* **Nielsen, M. A., & Chuang, I. L. (2010).** Quantum Computation and Quantum Information.
* **IBM Quantum Processor Data:** Calibration logs for the Eagle 51Q processor.

## ⚖️ Rights & Licensing
This project is open-source under the **MIT License**. All rights reserved to the developer **Jaafar Abdulsalam - 2026**.

