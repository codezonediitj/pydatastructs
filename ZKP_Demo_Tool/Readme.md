# 🔐 Zero-Knowledge Proof Interactive Tutorial (Graph-Based Simulation)

This project is a **visual and interactive educational tool** that demonstrates the fundamental principles of **Zero-Knowledge Proofs (ZKPs)** using graph-based simulations and commitment schemes. It is built entirely using **Python + PyQt5**, and is designed to engage both cryptography students and mentors with real-world analogies and intuitive illustrations.

Developed by **Susmita Chakrabarty** as part of a GSoC proposal under the PyDataStructs organization.

---

##  What It Teaches

This tutorial explains:

-  **Commitment Schemes**: Using SHA-256 to create secure, hidden commitments.
- 🔐 **Binding**: Commitments cannot be altered after submission.
-  **Hiding**: Commitments reveal no information until the reveal phase.
- **ZKP Challenge Rounds**: Verifier issues a challenge, prover reveals commitment.
- **Graph-Based Real-World Use Cases**: Transaction roles in banking systems, fraud detection, and more.

Each scene is part of a **narrative and interactive journey**, gradually introducing cryptographic guarantees in a way that is fun, memorable, and technically sound.

---

## 📁 Project Structure
```plaintext
ZKP_Demo_Tool/
├── assets/
│   └── scene1.png              #Optional illustration or background image
│
├── tutorial/
│   ├── tutorial_scene.py       #Scene 1 - Intro to commitment schemes
│   ├── scene2_commitment.py    # Scene 2 - ZKP using transaction graph
│   ├── scene3_bipartate.py     # Scene 3 - Bipartite graph simulation
│   └── run_all_scenes.py       # Launcher GUI for all scenes
│
└── README.md                   # Project documentation

```
## How to Run

### 1. Recommended: Start with the Launcher

```bash
cd /ZKP_DEMO_TOOL/tutorial
python run_all_scenes.py
```
## Designed For

- Cryptography students and researchers  
- Mentors reviewing GSoC/academic projects  
- Visual learners who prefer intuitive simulations  
- Anyone curious about ZKPs in real-world graphs  

---

## Future Directions

- Add auto-mode for repeated ZKP rounds with statistics  
- Export logs to PDF for classroom use  
- Sound or animation effects for fraud detection  
- Homomorphic commitments or multi-party extensions  

---

## Acknowledgments

This demo was designed to be engaging and intellectually rich while remaining accessible.  
Thanks to [Wikipedia - Commitment Scheme](https://en.wikipedia.org/wiki/Commitment_scheme), educational ZKP materials, and feedback from mentors and peers.

