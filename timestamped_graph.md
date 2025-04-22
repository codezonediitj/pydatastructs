# Timestamped Graph Snapshots

## Overview

The timestamped snapshot feature enables graphs to store their historical states automatically using real-time timestamps. This allows users to track the evolution of a graph over time, retrieve past states, and perform time-based analysis.

## Why This Feature Matters

- **Graph Evolution Tracking**: Enables users to analyze how a graph changes over time.
- **Anomaly Detection in Secure Networks**: Helps in detecting unusual patterns in cryptographic protocols and secure transactions.
- **Time-Series Graph Analysis**: Supports applications in secure financial transactions and privacy-preserving communications.
- **Cryptographic Security (Future Enhancement)**: Can be extended to sign snapshots using HMAC for integrity verification and encrypted storage.
- **Environment Variable-Based Secret Key**: Adds security by keeping cryptographic secrets out of the source code, reducing exposure to attacks.

## How It Works

### **Snapshot Storage & Security Enhancements**

- When `add_snapshot()` is called, a deep copy of the graph is saved with a unique timestamp.
- Each snapshot is **serialized and cryptographically signed** using an **HMAC signature**.
- The system stores the HMAC signature alongside the snapshot to verify its integrity before retrieval.

### **Why We Use an Environment Variable for the Secret Key**
To **prevent hardcoding secrets in the source code**, we store the **HMAC secret key in an environment variable** instead of defining it directly in the script. This offers:
1. **Better Security**: Secrets stored in environment variables are not exposed in source code repositories.
2. **Protection Against Attacks**: If an attacker gains access to the codebase, they **cannot retrieve the HMAC key** without environment access.
3. **Separation of Concerns**: The cryptographic key can be changed without modifying the code, making key rotation easier.

## **Security Best Practices**
To ensure maximum security when handling cryptographic keys, follow these best practices:

1. **Always set the HMAC key before running the program:**
   ```bash
   export HMAC_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

### **Retrieving Historical States**

- Users can retrieve past versions of the graph using `get_snapshot(timestamp)`, enabling time-based queries.
- If an invalid timestamp is requested, the system raises a clear error with available timestamps.

### **Listing Available Snapshots**

- The `list_snapshots()` method provides a sorted list of all saved timestamps.

## Usage Example

```python
from pydatastructs.graphs import Graph

graph = Graph(implementation='adjacency_list')

graph.add_edge("A", "B", weight=5)
graph.add_snapshot()  # Snapshot stored with real-time timestamp

graph.add_edge("B", "C", weight=7)
graph.add_snapshot()

# List stored snapshots
print(graph.list_snapshots())  # Output: [timestamp1, timestamp2]

# Retrieve a past graph state
old_graph = graph.get_snapshot(graph.list_snapshots()[0])
```

## Future Enhancements

- **Secure Graph Snapshots for Banking & Finance**: Implement HMAC or cryptographic signing to prevent unauthorized modifications in financial transaction networks.
- **Encrypted Graph Storage for Privacy-Critical Applications**: Apply homomorphic encryption or privacy-preserving encryption to protect sensitive data, such as medical records, customer transactions, or identity graphs.
- **Efficient Storage for Large-Scale Graphs**: Introduce optimized serialization techniques to store historical snapshots with minimal overhead, making it scalable for real-world enterprise applications.
- **Integrity Verification for Regulatory Compliance**: Ensure snapshots cannot be altered without detection by integrating cryptographic hash functions. This is crucial for auditing in banking, supply chain security, and legal record-keeping.
- **Regulatory Compliance and Auditing**: Extend integrity verification using Merkle trees for large-scale verification. Implement tamper-proof logging for financial transactions.
- **Efficient storage for large graphs**: Introduce optimized serialization techniques to minimize storage costs.

## Conclusion

This feature lays the groundwork for advanced **cryptographic** graph analytics, allowing users to analyze, secure, and retrieve historical graph states efficiently. As future enhancements are implemented, timestamped snapshots will serve as a core foundation for **secure graph-based computations, privacy-preserving transactions, and cryptographic security in graph structures.**

