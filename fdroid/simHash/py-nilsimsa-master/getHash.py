
# from nilsimsa.deprecated._deprecated_nilsimsa import Nilsimsa as orig_Nilsimsa
from nilsimsa import Nilsimsa, compare_digests, convert_hex_to_ints

# nil = Nilsimsa('0'*64)
# s1 = nil.hexdigest()
# nil = Nilsimsa('0'*64+'11111234234223423423424')
# s2 = nil.hexdigest()
# print s1,s2
# print compare_digests(s1,s2)

def get_nilsimsa(string):
    return Nilsimsa(string).hexdigest()


def compare_hash(hash1, hash2):
    return 128 - compare_digests(hash1, hash2)


if __name__ == '__main__':
    # get_nilsimsa()
    l = get_nilsimsa('rtrtrtrtrtrt83dgfddfdfggd46587364dgbvnbnbnf09287')
    n = get_nilsimsa('rtrtrtrtrtrt83dgfdfggd465bnf09287')
    print compare_hash(l, n)