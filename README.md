# Proof of Reserves Tutorial (USDT-only)

This tutorial explains how to verify your individual liabilities in a Proof-of-Reserves system where only **USDT assets** are involved. It uses the **Merkle Tree** to ensure transparency and security while allowing users to independently verify their inclusion.

---
## Background

Proof-of-Reserves leverages the **Merkle Tree**, a cryptographic data structure, to prove that users' USDT balances are accounted for in the platform's reserves. This ensures that every user's assets are included without exposing sensitive information.

---
## Verification Process
### Step 1: Generate the Merkle Leaf
To verify your inclusion in the **Merkle Tree**, follow these steps:
1. Hash your **User ID (UID)**.
2. Combine the hashed UID with your USDT balance.
3. Hash the resulting string to generate your Merkle Leaf.

---
#### Example: How to Build Your Merkle Leaf

##### Input:
1. **User ID**: User12345
2. **USDT Balance**: 100.25890

##### Steps:
1. **Hash Your UID**: Use SHA256 to hash the UID:
    ```
    Input: User12345
    Output (Hashed UID): 6e7fb5f60d505b9480ad515a14b63194fa8bc3883acb3d9fbe3f9010690fcb0c
    ```
3. **Format the USDT Balance**: Format your USDT balance according to these rules:
    - No scientific notation.
    - Remove trailing zeros.
    - 0 is formatted as `0.0`.
    - Values between 0 and 1 must start with `0.`.
3. Example:
    ```
    USDT Balance: 100.25890 → Formatted: 100.2589
    ```
4. **Combine Hashed UID and Balance**: Combine the hashed UID and formatted balance in the following format:
    ```
    {Hashed UID},USDT:{Balance}
    ```
5. Example:
    ```
    6e7fb5f60d505b9480ad515a14b63194fa8bc3883acb3d9fbe3f9010690fcb0c,USDT:100.2589
    ```
6. **Hash the Final String**: Hash the resulting string to get your Merkle Leaf:
    ```
    Input:
    6e7fb5f60d505b9480ad515a14b63194fa8bc3883acb3d9fbe3f9010690fcb0c,USDT:100.2589
    Output (Merkle Leaf): 3b44181df32e6fbad0273fd5bcaa8e273121d355a28933cd2b98a9e7c0bb3c7f
    ```
---
### Step 2: Verify Your Inclusion
#### Input Required:

1. **Your Merkle Path**:
  - A list of intermediate hash values provided by the platform, which allows you to traverse the Merkle Tree and calculate the root.
    ```
    Merkle Path:
    [
        "af12b34c...",
        "5d67e89f...",
        "c0ffee33..."
    ]
    ```
2. **Merkle Root**:
  - The final hash representing the entire tree, provided by the platform.
    ```
    Merkle Root: aabbccddeeff11223344556677889900aabbccddeeff11223344556677889900
    ```
3. **Your Merkle Leaf**:
  - Generated in **Step 1**.

#### Verify Using Python:
Write or use a Python script to traverse the Merkle Path and calculate the Merkle Root.

#### Command line tool to facilitate the verification
**Requirement**

Python 3.4 or above

#### Examples
- Generate the Hashed UID
> python por.py hash {uid}

- Generate the Merkle leaf
> python por.py hash {asset string}
e.g.
> python por.py hash abcdefg,USDT:20384

- Verify the inclusion of the Merkle leaf, compare the result with the Merkle root
> python por.py verify {Merkle leaf} {Merkle path}
