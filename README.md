# XRP MyGrant Microloans App

**🚀 150-Character Summary**  
> **Offers** a transparent credit scoring, peer-to-peer lending, and remittance platform to **support** underserved migrant workers in Singapore **solve** financial exclusion **with** XRPL-based on-chain credit scoring and decentralized identity (DID)

---

## 📝 Full Description

Migrant workers are a crucial pillar of accelerating economies in Southeast Asia today but remain financially underserved. About 70% do not have access to financial services that match their needs. Traditional financial services and products are tied to nationality-based indicators and limited by national borders. Poor financial literacy and predatory lenders further trap workers in cycles of debt.

To address these structural issues that perpetuate inequitable financial dependence, our dApp leverages the XRP Ledger to empower low-wage migrant workers in Southeast Asia with a platform for:

- **Transparent Remittances**: Send XRP cross-border at minimal cost and high speed.  
- **P2P Microloans**: Offer collateralized or uncollateralized loans directly on XRPL.  
- **On-Chain Credit Scoring**: Evaluate creditworthiness using immutable remittance history.

---

## ⚙️ Technical Explanation

### 1. Credit Scoring via Remittance History
- **Data Extraction**: Query user’s XRP wallet transaction history using the XRPL API (`account_tx`).  
- **Behavioral Scoring**: Analyze remittance patterns (frequency, volume, diverse destinations) with `xrpl-py` or `xrpl.js`.  
- **Risk Profiles**: Apply rule-based heuristics or simple ML models to generate a credit score; store off-chain (e.g., PostgreSQL) keyed by DID.

### 2. Privacy Layer with Zero-Knowledge Proofs
- **Verifiable Presentations**: Users consent to share ZKPs of their transaction record, revealing only the necessary attestations without exposing raw data.  
- **Trust Building**: Leverages blockchain-native behaviors rather than centralized data to democratize credit access.

### 3. Secure Authentication with Decentralized Identity (DID)
- **DID Creation**: Anchor self-sovereign identities on XRPL using the XLS-40 `DIDSet` transaction.  
- **Challenge–Response Flow**:  
  1. Frontend requests a nonce from `/auth/request-challenge`.  
  2. User signs the nonce with their XRPL private key (via `xrpl.js` or wallet extension).  
  3. Backend resolves the DID Document on-chain, verifies the signature, then issues a JWT with the DID as `sub`.  
- **Passwordless**: Eliminates centralized KYC databases; users fully control and port their identity.

### 4. Microloan Origination on XRPL
- **Collateralized Loans**:  
  - Borrower locks collateral (XRP or token) via `EscrowCreate`.  
  - Lender disburses funds via native XRP or issued IOUs.  
  - Collateral is released on repayment via `EscrowFinish` or Hooks.

- **Uncollateralized Loans**:  
  - Establish trustline from lender to borrower’s account based on credit score.  
  - Lender issues IOU tokens directly on XRPL.  
  - Repayment tracked on-chain; Hooks trigger notifications or DID credential revocations on default.

- **Settlement & Repayment**:  
  Loans repaid in XRP or IOUs. Hooks enforce time-based conditions and automate default handling.

---

## 📂 Project Links

- **Slides**: [Canva Presentation](https://www.canva.com/design/DAGpoyh7hAE/Tixfbu6zGVSUf1_7SDKuNA/edit?utm_content=DAGpoyh7hAE&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
- **Live Demo**: [Canva Slide with Video](https://www.canva.com/design/DAGpoyh7hAE/Tixfbu6zGVSUf1_7SDKuNA/edit?ui=eyJEIjp7IlQiOnsiQSI6IlBCNWRCU014dDUzaE5yZFcifX19)
- **GitHub Repo**: [Anish-Gholap/XRPApp](https://github.com/Anish-Gholap/XRPApp)
- **UI Screenshots**: [Google Drive with UI Screenshots of Main Flows] (https://drive.google.com/drive/folders/1NVOYAIutT-n1JAGy-WU06x_7FnT7J0re?usp=sharing)
---

## 👥 Team & Contact

- **Yash Vershori** – yashvershori@gmail.com  
- **Anish Gholap** – anishgholap@gmail.com  
- **LP Low** – lowpt.a@gmail.com  
- **EY Ong** – eyong002@gmail.com

**Affiliations:** Nanyang Technological University (NTU), National University of Singapore, Sinaya Corp

**Twitter:** [@_audreee_](https://twitter.com/_audreee_), [@adnamawol](https://twitter.com/adnamawol)

---

## 🎯 Competition Tracks

- XRP Ledger Track  
- Exploration Track – Cross-chain & EVM Sidechain (Flowdesk)  
- Ripple Impact Social Impact Prize  
- EVM Sidechain Bounty  
- Multi-Purpose Tokens & DID & Credential  
- Best Cross-Chain App Leveraging Axelar Bridge (GMP)  
- Best Developer Tooling
