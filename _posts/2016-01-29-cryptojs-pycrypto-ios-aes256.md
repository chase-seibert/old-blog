---
layout: post
title: Interoperable AES256 encryption between CryptoJS, PyCrypto and CryptoSwift
---

Even though AES256 is a standard, there are enough choices left to implementing libraries to make
cross platform encrypting and decrypting tricky. In particular, getting Javascript, Python and
Swift code that could all encrypt to the same ciphertext using the same plaintext and keys, and
then successfully decrypt back to the plaintext proved to be a multiple day adventure for three
engineers.

Thanks to [marcoslin](https://gist.github.com/marcoslin/8026990) for getting us started!

Also, thanks to my co-workers Chris Boyle and Yair Loeza, who assure me that they do not have
Twitter accounts worth linking to ;)

# CryptoJS

This library makes some implementation decisions that required diving into the source code to
even find out about.

- In the canonical usage `Crypto.AES.encrypt(plaintext, key, options)`, the second parameter is not actually
the AES key. It's the "passphrase", which is used to randomly generate `key`, `iv` AND `salt` values.
- However, if you pass a byte array instead of a string, it WILL use that value as the `key` directly.
- We also found it expedient to set an `iv` value explicitly via the third `options` parameter.
- The default AES mode and padding scheme are also defaulted differently than other libraries, but
can easily be over-ridden in the constructor. We chose zero byte padding knowing that it's simple and
that we would need to implement pad/unpad ourselves on the other platforms.
- Finally, we chose a serialization method of hex over the wire, to reduce the change that a character
encoding issue make our ciphertext invalid in transit.


```javascript
var Crypto = require('cryptojs');
Crypto = Crypto.Crypto;

var KEY = 'This is a key123';
var IV = 'This is an IV456';
var MODE = new Crypto.mode.CFB(Crypto.pad.ZeroPadding);

var plaintext = 'The answer is no';
var input_bytes = Crypto.charenc.UTF8.stringToBytes(plaintext);
var key = Crypto.charenc.UTF8.stringToBytes(KEY);
var options = {iv: Crypto.charenc.UTF8.stringToBytes(IV), asBytes: true, mode: MODE};
var encrypted = Crypto.AES.encrypt(input_bytes, key, options);
var encrypted_hex = Crypto.util.bytesToHex(encrypted);
console.log(encrypted_hex); // this is the value you send over the wire

output_bytes = Crypto.util.hexToBytes(encrypted_hex);
output_plaintext_bytes = Crypto.AES.decrypt(output_bytes, key, options);
output_plaintext = Crypto.charenc.UTF8.bytesToString(output_plaintext_bytes);
console.log(output_plaintext); // result: 'The answer is no'
```


# PyCrypto

We actually started with this implementation, but ended up having to tweak it more to be compatible
with what we were doing in CryptoJS. Nothing weird here, but we did need to set the mode correctly,
and we needed to implement the padding ourselves. PyCrypto does not require that plaintext be a
multiple of BLOCK_SIZE the way PyCrypto does, but we needed to ensure that it could encrypt and
decrypt to the same outputs as PyCrypto.


```python
import binascii
from Crypto.Cipher import AES


KEY = 'This is a key123'
IV = 'This is an IV456'
MODE = AES.MODE_CFB
BLOCK_SIZE = 16
SEGMENT_SIZE = 128


def encrypt(key, iv, plaintext):
    aes = AES.new(key, MODE, iv, segment_size=SEGMENT_SIZE)
    plaintext = _pad_string(plaintext)
    encrypted_text = aes.encrypt(plaintext)
    return binascii.b2a_hex(encrypted_text).rstrip()


def decrypt(key, iv, encrypted_text):
    aes = AES.new(key, MODE, iv, segment_size=SEGMENT_SIZE)
    encrypted_text_bytes = binascii.a2b_hex(encrypted_text)
    decrypted_text = aes.decrypt(encrypted_text_bytes)
    decrypted_text = _unpad_string(decrypted_text)
    return decrypted_text


def _pad_string(value):
    length = len(value)
    pad_size = BLOCK_SIZE - (length % BLOCK_SIZE)
    return value.ljust(length + pad_size, '\x00')


def _unpad_string(value):
    while value[-1] == '\x00':
        value = value[:-1]
    return value


if __name__ == '__main__':
    input_plaintext = 'The answer is no'
    encrypted_text = encrypt(KEY, IV, input_plaintext)
    decrypted_text = decrypt(KEY, IV, encrypted_text)
    assert decrypted_text == input_plaintext
```


# CryptoSwift

Only weird thing here is that we needed to implement our own conversion of a hex to NSData.


```swift
class AESHelper {


    var key: String
    var iv: String
    let BLOCK_SIZE = 16

    init (key: String, iv: String) {
        self.key = key
        self.iv = iv
    }

    func encrypt (stringToEncrypt: String) -> String {
        let messageData = stringToEncrypt.dataUsingEncoding(NSUTF8StringEncoding)
        let byteArray = pad(messageData!.arrayOfBytes())
        let encryptedBytes = try! AES(key: self.key, iv: self.iv, blockMode: .CFB).encrypt(byteArray, padding: .None)
        return encryptedBytes.toHexString()
    }

    func decrypt (var message: String) -> String {
        let messageData = message.dataFromHexadecimalString()
        let byteArray = messageData?.arrayOfBytes()
        let decryptedBytes: [UInt8] = try! AES(key: self.key, iv: self.iv, blockMode: .CFB).decrypt(byteArray!, padding: .None)
        let unpaddedBytes = unpad(decryptedBytes)
        var unencryptedString = NSString(bytes: unpaddedBytes, length: unpaddedBytes.count, encoding: NSUTF8StringEncoding)
        return String(unencryptedString)
    }

    private func pad(var value: [UInt8]) -> [UInt8] {
        let length: Int = value.count
        let padSize = BLOCK_SIZE - (length % BLOCK_SIZE)
        let padArray = [UInt8](count: padSize, repeatedValue: 0)
        value.appendContentsOf(padArray)
        return value
    }

    private func unpad(var value: [UInt8]) -> [UInt8] {
        for var index = value.count - 1; index >= 0; --index {
            if value[index] == 0 {
                value.removeAtIndex(index)
            } else  {
                break
            }
        }
        return value
    }

}

extension String {

    /// http://stackoverflow.com/questions/26501276/converting-hex-string-to-nsdata-in-swift
    ///
    /// Create NSData from hexadecimal string representation
    ///
    /// This takes a hexadecimal representation and creates a NSData object. Note, if the string has any spaces, those are removed. Also if the string started with a '<' or ended with a '>', those are removed, too. This does no validation of the string to ensure it's a valid hexadecimal string
    ///
    /// The use of `strtoul` inspired by Martin R at http://stackoverflow.com/a/26284562/1271826
    ///
    /// - returns: NSData represented by this hexadecimal string. Returns nil if string contains characters outside the 0-9 and a-f range.

    func dataFromHexadecimalString() -> NSData? {
        let trimmedString = self.stringByTrimmingCharactersInSet(NSCharacterSet(charactersInString: "<> ")).stringByReplacingOccurrencesOfString(" ", withString: "")

        // make sure the cleaned up string consists solely of hex digits, and that we have even number of them

        let regex = try! NSRegularExpression(pattern: "^[0-9a-f]*$", options: .CaseInsensitive)

        let found = regex.firstMatchInString(trimmedString, options: [], range: NSMakeRange(0, trimmedString.characters.count))
        if found == nil || found?.range.location == NSNotFound || trimmedString.characters.count % 2 != 0 {
            return nil
        }

        // everything ok, so now let's build NSData

        let data = NSMutableData(capacity: trimmedString.characters.count / 2)

        for var index = trimmedString.startIndex; index < trimmedString.endIndex; index = index.successor().successor() {
            let byteString = trimmedString.substringWithRange(Range<String.Index>(start: index, end: index.successor().successor()))
            let num = UInt8(byteString.withCString { strtoul($0, nil, 16) })
            data?.appendBytes([num] as [UInt8], length: 1)
        }

        return data
    }
```


Happy encrypting!
