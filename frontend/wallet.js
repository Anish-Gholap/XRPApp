// wallet.js
const { Wallet }   = require("xrpl")
const { sign, verify }     = require("ripple-keypairs")

// 1. Rehydrate your wallet
const wallet = Wallet.fromSeed("sEd73kkZgVYVR1rsDff5zWAZrXp6XTJ")

// 2. Get the hex‐encoded challenge from your backend
//    e.g. "7981574830a1d1ffe708c05fdcb5e7d3"
const challenge = "3ba6627fcc6fb12885f00a9f6fc58fc1"

// 3. Convert the UTF-8 challenge into a hex string
const messageHex = Buffer.from(challenge, "utf8").toString("hex")

// 4. Sign the hex‐encoded message with your private key
//    → this returns a hex‐encoded signature
const signatureHex = sign(messageHex, wallet.privateKey)  
console.log("Message (hex):", messageHex)
console.log("Signature (hex):", signatureHex)
console.log("Public Key:", wallet.publicKey)

// 5. (Optional) If your backend expects Base64, re-encode:
const signatureB64 = Buffer.from(signatureHex, "hex").toString("base64")
console.log("Signature (base64):", signatureB64)

const res = verify(
  messageHex, // the original message
  signatureHex, // the signature
  wallet.publicKey // the public key from the wallet
)

console.log("Signature valid:", res) // true if the signature is valid