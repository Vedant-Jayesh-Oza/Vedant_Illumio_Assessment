import os

def load_lookup_table(filepath):
    
    lookup_table = {}

    if not os.path.exists(filepath):
        print(f"Error: Lookup table file '{filepath}' not found.")
        return lookup_table  

    try:
        with open(filepath, "r") as file:
            next(file) 

            for line in file:
                parts = line.strip().split(",")
                
                if len(parts) != 3:
                    print(f"Warning: Skipping malformed line: {line.strip()}")
                    continue  

                dstport, protocol, tag = parts

                protocol = protocol.strip().lower()
                dstport = dstport.strip()
                tag = tag.strip()

                lookup_table[(dstport, protocol)] = tag  

    except Exception as e:
        print(f"Error reading lookup table: {e}")

    return lookup_table

def load_flow_logs(filepath, lookup_table):
    
    enriched_logs = []

    if not os.path.exists(filepath):
        print(f"Error: Flow log file '{filepath}' not found.")
        return enriched_logs  

    try:
        with open(filepath, "r") as file:
            for line in file:
                parts = line.strip().split()

                if len(parts) < 10:
                    print(f"Warning: Skipping malformed line: {line.strip()}")
                    continue  

                dstport = parts[5].strip()  
                protocol_num = parts[7].strip()  

                protocol_mapping = {"6": "tcp", "17": "udp", "1": "icmp"}
                protocol = protocol_mapping.get(protocol_num, "unknown").lower()

                tag = lookup_table.get((dstport, protocol), "Untagged")

                enriched_logs.append(f"{line.strip()} {tag}")

    except Exception as e:
        print(f"Error reading flow log file: {e}")

    return enriched_logs

def generate_summary(enriched_logs, output_file):
    
    from collections import defaultdict

    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)

    for log in enriched_logs:
        parts = log.strip().split()
        
        if len(parts) < 10:
            continue  
        
        dstport = parts[5]  
        protocol_num = parts[7]  
        tag = parts[-1] 
        
        protocol_mapping = {"6": "tcp", "17": "udp", "1": "icmp"}
        protocol = protocol_mapping.get(protocol_num, "unknown").lower()

        tag_counts[tag] += 1

        port_protocol_counts[(dstport, protocol)] += 1

    with open(output_file, "w") as file:
        file.write("Tag Counts:\nTag,Count\n")
        for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
            file.write(f"{tag},{count}\n")

        file.write("\nPort/Protocol Combination Counts:\nPort,Protocol,Count\n")
        for (port, protocol), count in sorted(port_protocol_counts.items()):
            file.write(f"{port},{protocol},{count}\n")

    print(f"\nSummary generated and saved to {output_file}")


if __name__ == "__main__":
    lookup_path = "data/lookup.txt"
    flowlog_path = "data/flow_logs.txt"
    output_summary_path = "output/summary.txt"

    lookup_dict = load_lookup_table(lookup_path)
    enriched_logs = load_flow_logs(flowlog_path, lookup_dict)

    print("\nEnriched Flow Logs:")
    for log in enriched_logs[:5]:  
        print(log)

    generate_summary(enriched_logs, output_summary_path)


