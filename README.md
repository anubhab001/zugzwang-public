# ZUGZWANG Cipher (Concrete Instance) #

This [repository](https://github.com/anubhab001/zugzwang-public) contains a reference implementation of the proof-of-concept block cipher cipher, ZUGZWANG (concrete instance/encryption). The cipher is basically a four-round Feistel construction, but has an innate backdoor. The key is revealed through the ciphertext with the plaintext matches a backdoor entry, otherwise the cipher is secure. See this paper on  [ePrint](https://eprint.iacr.org/2022/???) for its specification and other details.

## Requirement ##
* Python 3
* [Pycryptodome](https://pypi.org/project/pycryptodome/)

## Test Cases ##
Case | 1
---- | ----
<span style="color:yellow;">Key</span>|             <span style="color:yellow;">10000000000000000000000000000000</span>
<span style="color:red;">Backdoor Entry</span>|  <span style="color:red;">10000000000000000000000000000000</span>
<span style="color:red;">Plaintext</span>|       <span style="color:red;">10000000000000000000000000000000</span>
Ciphertext|      10000000000000001000000000000000
<span style="color:yellow;">Recovered Key</span>|   <span style="color:yellow;">10000000000000000000000000000000</span>

Case | 2
---- | ----
Key|             10000000000000000000000000000000
<span style="color:green;">Backdoor Entry</span>|  <span style="color:green;">10000000000000000000000000000000</span>
Plaintext|       00000000000000000000000000000001
Ciphertext|      77882970d3ee73581cce9b1ae1e66cbd

Case | 3
---- | ----
Key|             10000000000000000000000000000000
<span style="color:green;">Backdoor Entry</span>|  <span style="color:green;">10000000000000000000000000000000</span>
Plaintext|       f0000000000000000000000000000000
Ciphertext|      d5c03bdfec4e0fcf853645f83c6d74ef

Case | 4
---- | ----
<span style="color:yellow;">Key</span>|             <span style="color:yellow;">10000000000000000000000000000000</span>
<span style="color:red;">Backdoor Entry</span>|  <span style="color:red;">0000000000000000000000000000000f</span>
<span style="color:red;">Plaintext</span>|       <span style="color:red;">0000000000000000000000000000000f</span>
Ciphertext|      100000000000000f0000000000000000
<span style="color:yellow;">Recovered Key</span>|   <span style="color:yellow;">10000000000000000000000000000000</span>

Case | 5
---- | ----
Key|             10000000000000000000000000000000
<span style="color:green;">Backdoor Entry</span>|  <span style="color:green;">10000000000000000000000000000000</span>
Plaintext|       0000000000000000000000000000000f
Ciphertext|      81cca7e35cf90690105da7090fbb253d

Case | 6
---- | ----
Key|             f1000000000000000000000000000000
<span style="color:green;">Backdoor Entry</span>|  <span style="color:green;">1000000000000000000000000000000f</span>
Plaintext|       0000000000000000000000000000000f
Ciphertext|      d69db61c7ef55b8d4e0b7e87b18ee158

Case | 7
---- | ----
<span style="color:yellow;">Key</span>|             <span style="color:yellow;">3cf28000471a74d22d81b6c98a3dbe33</span>
<span style="color:red;">Backdoor Entry</span>|  <span style="color:red;">1831bcaa5bee08e639864e4823183090</span>
<span style="color:red;">Plaintext</span>|       <span style="color:red;">1831bcaa5bee08e639864e4823183090</span>
Ciphertext|      0574ce486402444235b00a63d1d3b6d5
<span style="color:yellow;">Recovered Key</span>|   <span style="color:yellow;">3cf28000471a74d22d81b6c98a3dbe33</span>

Case | 8
---- | ----
Key|             3cf28000471a74d22d81b6c98a3dbe33
<span style="color:green;">Backdoor Entry</span>|  <span style="color:green;">1831bcaa5bee08e639864e4823183090</span>
Plaintext|       9eac455e039a58928e163658e1493a20
Ciphertext|      7a7700e9f5f4f974e9ba2834160cf284
<span style="color:gray;">_Note_</span>| <span style="color:gray;">_This test case is currently hardcoded_</span>
