# -*- coding: cp1252 -*-

KS = L^(m) + L^(m+1) + L^(m+2) + ........ + L^(M) 

where
L = character set length
m = min length of the key
M = max length of the key

For example, when you want to crack an half of a LanManager passwords (LM) using the character set "ABCDEFGHIJKLMNOPQRSTUVWXYZ" of 26 letters, the brute-force cracker have to try KS = 26^1 + 26^2 + 26^3 + ...... + 26^7 = 8353082582 different keys.

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`!@#$%^&*()_-+=[]{}\|<>"':;,.? /ñ"

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`!@#$%^&*()_-+=[]{}\\|<>\"\':;,.? /ñ"

Lcharset = len(charset)
Lcharset = 96
minkey = 1
maxkey = 8

KS = Lcharset**1 + Lcharset**2 + Lcharset**3 + Lcharset**4 + Lcharset**5 + Lcharset**6 + Lcharset**7 + Lcharset**8

# Need to break it down to chunks of 50 million per sec. or 180 billion an hour. 180000000000
# to do this charset will have to be adjusted. 
 

-----------------------------------------------------------------------------------------------------------
package 1

minkey = 1
maxkey = 5
p1:charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`!@#$%^&*()_-+=[]{}\\|<>\"\':;,.? /ñ"

-----------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------
package 2

minkey =6
maxkey =6

p2a:charset = "abcdefghijklmnopqrstuvwx"
p2b:charset = "yzABCDEFGHIJKLMNOPQRSTUV"
p2c:charset = "WXYZ1234567890~`!@#$%^&*"
p2d:charset = "()_-+=[]{}\\|<>\"\':;,.? /ñ"


-------------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------
package 3

minkey = 7
maxkey = 7


p3a:charset = "abcdefghi"
p3b:charset = "jklmnopqr"
p3c:charset = "stuvwxyzA"
p3d:charset = "BCDEFGHIJ"
p3e:charset = "KLMNOPQRS"
p3f:charset = "TUVWXYZ12"
p3g:charset = "34567890~"
p3h:charset = "`!@#$%^&*"
p3i:charset = "()_-+=[]{"
p3j:charset = "}\\|<>\"\':;"
p3k:charset = ",.? /ñ"


-----------------------------------------------------------------------------------------------------------------


-----------------------------------------------------------------------------------------------------------------
package 4

minkey = 8
maxkey = 8

p4a:charset = "abcdefghi"
p4b:charset = "jklmnopqr"
p4c:charset = "stuvwxyzA"
p4d:charset = "BCDEFGHIJ"
p4e:charset = "KLMNOPQRS"
p4f:charset = "TUVWXYZ12"
p4g:charset = "34567890~"
p4h:charset = "`!@#$%^&*"
p4i:charset = "()_-+=[]{"
p4j:charset = "}\\|<>\"\':;"
p4k:charset = ",.? /ñ"
------------------------------------------------------------------------------------------------------


-------------------------------------------------------------------------------------------------------
package 5

minkey = 9
maxkey = 9

p5a:charset = "abcdefg"
p5b:charset = "jklmnop"
p5c:charset = "stuvwxy"
p5d:charset = "BCDEFGH"
p5e:charset = "KLMNOPQ"
p5f:charset = "TUVWXYZ"
p5g:charset = "3456789"
p5h:charset = "`!@#$%^"
p5i:charset = "()_-+=["
p5j:charset = "}\\|<>\"\'"
p5k:charset = ",.? /ñ;"
p5l:charset = "hiqrzAI"
p5m:charset = "JRS120~"
p5n:charset = "&*]{:"
-----------------------------------------------------------------------------------------------------------


