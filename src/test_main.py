import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.main import load_lookup_table, load_flow_logs, generate_summary

class TestNetworkFlowAnalyzer(unittest.TestCase):
    def setUp(self):
        os.makedirs("test_data", exist_ok=True)
        
    def test_lookup_table_loading(self):
        with open("test_data/test_lookup.txt", "w") as f:
            f.write("dstport,protocol,tag\n")
            f.write("25,TCP,sv_P1\n")  
            f.write("443,tcp,sv_P2\n")
            f.write("25,UDP,sv_P3\n")  
        
        lookup_table = load_lookup_table("test_data/test_lookup.txt")
        
        self.assertEqual(lookup_table[("25", "tcp")], "sv_P1")
        self.assertEqual(lookup_table[("443", "tcp")], "sv_P2")
        self.assertEqual(lookup_table[("25", "udp")], "sv_P3")

    def test_flow_log_processing(self):
        with open("test_data/test_lookup.txt", "w") as f:
            f.write("dstport,protocol,tag\n")
            f.write("443,tcp,sv_P2\n")

        with open("test_data/test_flow.txt", "w") as f:
            f.write("2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
            f.write("2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK\n")

        lookup_table = load_lookup_table("test_data/test_lookup.txt")
        enriched_logs = load_flow_logs("test_data/test_flow.txt", lookup_table)

        self.assertTrue("sv_P2" in enriched_logs[0])
        self.assertTrue("Untagged" in enriched_logs[1])

    def test_large_file_handling(self):
        with open("test_data/large_lookup.txt", "w") as f:
            f.write("dstport,protocol,tag\n")
            for i in range(10000):
                f.write(f"{i},tcp,tag_{i}\n")

        with open("test_data/large_flow.txt", "w") as f:
            for i in range(50000):  
                f.write(f"2 123456789012 eni-{i} 10.0.0.1 10.0.0.2 {i} 49152 6 10 1000 1620140761 1620140821 ACCEPT OK\n")

        lookup_table = load_lookup_table("test_data/large_lookup.txt")
        enriched_logs = load_flow_logs("test_data/large_flow.txt", lookup_table)
        
        self.assertTrue(len(lookup_table) > 9000)  
        self.assertTrue(len(enriched_logs) > 40000)  

    def test_protocol_handling(self):
        with open("test_data/protocol_lookup.txt", "w") as f:
            f.write("dstport,protocol,tag\n")
            f.write("80,tcp,web\n")
            f.write("53,udp,dns\n")
            f.write("0,icmp,ping\n")

        with open("test_data/protocol_flow.txt", "w") as f:
            f.write("2 123 eni-1 10.0.0.1 10.0.0.2 80 49152 6 10 1000 1620140761 1620140821 ACCEPT OK\n")  # TCP
            f.write("2 123 eni-2 10.0.0.1 10.0.0.2 53 49152 17 10 1000 1620140761 1620140821 ACCEPT OK\n")  # UDP
            f.write("2 123 eni-3 10.0.0.1 10.0.0.2 0 0 1 10 1000 1620140761 1620140821 ACCEPT OK\n")  # ICMP

        lookup_table = load_lookup_table("test_data/protocol_lookup.txt")
        enriched_logs = load_flow_logs("test_data/protocol_flow.txt", lookup_table)

        self.assertTrue("web" in enriched_logs[0])
        self.assertTrue("dns" in enriched_logs[1])
        self.assertTrue("ping" in enriched_logs[2])

    def tearDown(self):
        import shutil
        shutil.rmtree("test_data", ignore_errors=True)

if __name__ == '__main__':
    unittest.main()