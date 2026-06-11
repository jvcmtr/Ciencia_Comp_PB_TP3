from q4_utils import ipv4_to_int, ipv6_to_int

class Node:
    def __init__(self):
        self.children = [None, None]
        self.route_id = None

class Router:
    def __init__(self):
        self.root = Node()

    def _parse_ip(self, str):
        if ":" in str:
            return ipv6_to_int(str), 128
        else:
            return ipv4_to_int(str), 32

    def insert(self, cidr, route_id):
        ip_part, bits_str = cidr.split("/")
        val, max_bits = self._parse_ip(ip_part)
        length = int(bits_str)
        
        curr = self.root
        for i in range(length):
            bit = (val >> (max_bits - 1 - i)) & 1
            if not curr.children[bit]:
                curr.children[bit] = Node()
            curr = curr.children[bit]
        curr.route_id = route_id

    def lookup(self, ip):
        val, max_bits = self._parse_ip(ip)
        curr = self.root
        lpm_id = None
        
        for i in range(max_bits + 1):
            if curr.route_id is not None:
                lpm_id = curr.route_id
            if i == max_bits:
                break
            bit = (val >> (max_bits - 1 - i)) & 1
            if not curr.children[bit]:
                break
            curr = curr.children[bit]
        return lpm_id

ROUTE_TABLE = [
    ("192.168.0.0/16", 10),
    ("192.168.1.0/24", 20),
    ("192.168.1.128/25", 30),
    ("10.0.0.0/8", 40),
    ("0.0.0.0/0", 50),
    ("2001:db8::/32", 100),
    ("2001:db8:a::/48", 200)
]

TEST_CASES = [
    ("192.168.0.50", 10),
    ("192.168.1.20", 20),
    ("192.168.1.150", 30),
    ("10.255.0.1", 40),
    ("8.8.8.8", 50),
    ("2001:db8:a:1::10", 200),
    ("2001:db8:c::1", 100)
]

def test():
    router = Router()
    errors = 0

    for cidr, _id in ROUTE_TABLE:
        router.insert(cidr, _id)

    for i in range(len(TEST_CASES)):
        t, expected = TEST_CASES[i]
        result = router.lookup(t) 
        if expected == result:
            print(f"[{i+1}/{len(TEST_CASES)}]\t[SUCCESS] \t IP '{t}' correcly maped to route with ID '{result}'")
        else:
            print(f"[{i+1}/{len(TEST_CASES)}]\t[TEST FAILED] \t IP '{t}' didnt maped ID '{expected}', instead it maped to ID '{result}'")
            errors += 1
    
    print("____________________________________")
    print("\t Tests finished !")
    print(f"[{errors}/{len(TEST_CASES) }] Errors found - {'SUCCESS' if errors==0 else 'FAIL'}")


if __name__ == "__main__":
    test()