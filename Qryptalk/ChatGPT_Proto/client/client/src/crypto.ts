import * as oqs from "oqs"; // OQS.js
// AES encryption using Web Crypto API

export async function generateKyberKeys() {
  const alg = new oqs.KeyEncapsulation("Kyber512");
  return { publicKey: alg.generate_keypair().publicKey, privateKey: alg };
}

export async function encapsulate(publicKey: Uint8Array) {
  const alg = new oqs.KeyEncapsulation("Kyber512");
  const { ciphertext, shared_secret } = alg.encapsulate(publicKey);
  return { ciphertext, shared_secret };
}

export async function decapsulate(alg: any, ciphertext: Uint8Array) {
  return alg.decapsulate(ciphertext);
}

export async function encryptMessage(key: Uint8Array, message: string) {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const algo = { name: "AES-GCM", iv };
  const cryptoKey = await crypto.subtle.importKey("raw", key, algo, false, ["encrypt"]);
  const enc = new TextEncoder().encode(message);
  const ciphertext = await crypto.subtle.encrypt(algo, cryptoKey, enc);
  return { iv, ciphertext };
}

export async function decryptMessage(key: Uint8Array, iv: Uint8Array, ciphertext: ArrayBuffer) {
  const algo = { name: "AES-GCM", iv };
  const cryptoKey = await crypto.subtle.importKey("raw", key, algo, false, ["decrypt"]);
  const decrypted = await crypto.subtle.decrypt(algo, cryptoKey, ciphertext);
  return new TextDecoder().decode(decrypted);
}
