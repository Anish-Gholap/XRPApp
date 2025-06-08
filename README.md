# XRP MyGrant Microloans App

**🚀 150-Character Summary**  
> **Offers** a transparent credit scoring, peer-to-peer lending, and remittance platform to **support** underserved migrant workers in Singapore **solve** financial exclusion **with** XRPL-based on-chain credit scoring and decentralized identity (DID)

---

## 📝 Full Description

Migrant workers are a crucial pillar of accelerating economies in Southeast Asia today but remain financially underserved. About 70% do not have access to financial services that match their needs. Traditional financial services and products are tied to nationality-based indicators and limited by national borders. Poor financial literacy and predatory lenders further trap workers in cycles of debt.

To address these structural issues that perpetuate inequitable financial dependence, our dApp leverages the XRP Ledger to empower low-wage migrant workers in Southeast Asia with a platform for:

- **Trackable and Immutable loan history**: On successful posting of a loan request, an nft of the loan listing will be created where only the lender can burn the nft after fulfillment.
- **Transparent Remittances**: Send XRP cross-border at minimal cost and high speed.  
- **P2P Microloans**: Offer collateralized or uncollateralized loans directly on XRPL.  
- **On-Chain Credit Scoring**: Evaluate creditworthiness using immutable remittance history.



---

## ⚙️ Technical Explanation

### 1. Credit Scoring via Remittance History
- **Data Extraction**: Query user’s XRP wallet transaction history using the XRPL API (`account_tx`).  
- **Behavioral Scoring**: Analyze remittance patterns (frequency, volume, diverse destinations) with `xrpl-py` or `xrpl.js`.  
- **Risk Profiles**: Apply rule-based heuristics or simple ML models to generate a credit score; store off-chain (e.g., PostgreSQL) keyed by DID.

### 3. Privacy Layer with Zero-Knowledge Proofs
- **Verifiable Presentations**: Users consent to share ZKPs of their transaction record, revealing only the necessary attestations without exposing raw data.  
- **Trust Building**: Leverages blockchain-native behaviors rather than centralized data to democratize credit access.

### 4. Secure Authentication with Decentralized Identity (DID)
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

## NFT Loan Collateral System

The XRP Ledger also supports Non-Fungible Tokens (NFTs) which can be used as loan collateral. The API provides endpoints for NFT operations:

### NFT Operations

1. Mint NFT: Create a new NFT on the XRP Ledger
   - /api/xrp/loan/nft/mint
   - Requires wallet address, seed, and URI pointing to NFT metadata

2. Create Sell Offer: List an NFT for sale or as collateral
   - /api/xrp/loan/nft/sell
   - Can specify a destination (specific buyer/borrower)
   - Can set an expiration date (loan term)

3. Accept Sell Offer: Accept an NFT offer (claim collateral)
   - /api/xrp/loan/nft/accept
   - Used when a loan defaults and collateral is claimed

4. Burn NFT: Destroy an NFT (release collateral)
   - /api/xrp/loan/nft/burn
   - Can be used to release collateral when a loan is fully repaid

5. View NFTs: Get all NFTs owned by an account
   - /api/xrp/loan/nft/{address}

### NFT Loan Process

1. Collateral Setup:
   - Borrower mints an NFT or uses an existing one
   - NFT represents the collateral (e.g., property, vehicle title)
   
2. Loan Disbursement:
   - Borrower creates a sell offer for their NFT to the lender with an expiration matching the loan term
   - Lender funds the loan with issued currency
   
3. Loan Repayment:
   - If borrower repays in full, the sell offer expires or is cancelled
   - If borrower defaults, lender can accept the NFT sell offer to claim the collateral

This system provides a trustless mechanism for collateralized loans on the XRP Ledger.

---

## 📂 Project Links

- **Slides**: [Canva Presentation](https://www.canva.com/design/DAGpoyh7hAE/Tixfbu6zGVSUf1_7SDKuNA/edit?utm_content=DAGpoyh7hAE&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
- **Live Demo**: [Canva Slide with Video](https://www.canva.com/design/DAGpoyh7hAE/Tixfbu6zGVSUf1_7SDKuNA/edit?ui=eyJEIjp7IlQiOnsiQSI6IlBCNWRCU014dDUzaE5yZFcifX19)
- **GitHub Repo**: [Anish-Gholap/XRPApp](https://github.com/Anish-Gholap/XRPApp)
- **UI Screenshots**: [Google Drive with UI Screenshots]([url](https://drive.google.com/drive/folders/1NVOYAIutT-n1JAGy-WU06x_7FnT7J0re?usp=sharing)):https://drive.google.com/drive/folders/1NVOYAIutT-n1JAGy-WU06x_7FnT7J0re?usp=sharing
- **Block Explorer Link for Transactions from Our dApp on the XRP Ledger testnet**: https://testnet.xrpl.org/transactions/4D6D8A733342271AF83D20C7B6AD9DDD9348B8B1C22BCE5DBB4CE9FBBC0406DA
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

# XRP Lending System

## How XRP Ledger Loan System Works

This API implements a lending system on the XRP Ledger using issued currencies. The process involves several steps:

### Loan Funding Process

1. **DefaultRipple Flag Setup**: 
   - The issuer account is configured with the DefaultRipple flag enabled
   - This allows issued currencies to ripple (flow) through the issuer

2. **Trust Line Creation**:
   - Both lender and borrower establish trust lines to the issuer
   - Trust lines specify the maximum amount of the currency they're willing to hold

3. **Currency Issuance**:
   - The issuer creates the digital currency (e.g., "SGD")
   - Currency is issued to the lender's account

4. **Loan Payment**:
   - The lender sends the issued currency to the borrower
   - This transaction represents the loan disbursement
   - The XRP Ledger records this obligation in its distributed ledger

### Loan Repayment Process

1. **Repayment Transaction**:
   - The borrower sends the issued currency back to the lender
   - This typically includes principal plus interest
   - The transaction settles the debt obligation on the ledger

2. **Final Settlement**:
   - The loan obligation is settled on the ledger
   - Balances of both parties are updated accordingly

### Benefits of XRPL for Loans

- **Immutable Record**: All transactions are permanently recorded on the XRP Ledger
- **Transparency**: Loan terms and payments are publicly verifiable
- **Speed**: Transactions settle in 3-5 seconds
- **Low Cost**: Transaction fees are minimal (fraction of a cent)
- **Programmable**: Currency issuance can have restrictions or conditions

### API Endpoints

- `/fund-loan`: Handles the complete loan setup and funding process
- `/repay-loan`: Processes loan repayments from borrower to lender
- `/balance/{address}`: Check balances of any XRP address
- `/send-xrp`: Send native XRP between wallets
