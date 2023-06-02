#!/usr/bin/env python3

import argparse
import pybgpstream

import networkx as nx

import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description='Print the AS-Path Distance between an ASN and some of the content ASNs')

# parser.add_argument("country", help="the country (in ISO 2-letter format)")
parser.add_argument("asn", type=int, help="The ASN (eyeball or DC) you want to check the distance for")

args = parser.parse_args()

def convert_as_path(as_path):
    
    output = []

    for asn in as_path:
        output.append(int(asn))

    return(output)

def add_path_to_graph(graph, as_path):
    path_len = len(as_path)
    for k,asn in enumerate(as_path):
        if (k+1) is not path_len:
            graph.add_edge(as_path[k],as_path[k+1])

def get_asn_data():
    import requests

    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry

    retry_strategy = Retry(
            total=8,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )

    url = "https://ftp.ripe.net/ripe/asnames/asn.txt"

    q = requests.Session()

    p = q.get(url, timeout=20)

    asns = {}

    for line in p.iter_lines():
        split_line = line.decode().split(", ")
        
        try:
            country = split_line[1]
            split_line.pop(1)
        except:
            country = "ZZ"

        as_details = split_line[0].split()

        asn = int(as_details[0])
        
        as_details.pop(0)
        
        try:
            as_name = ' '.join(as_details)
        except:
            as_name = "None/Reserved"

        #print("AS {} has name '{}' and country {}".format(asn, as_name, country))
        
        asns[asn] = {"country": country, "as_name": as_name}

    return(asns)


def main(args):

    content_list = [
        33070, # Rackspace Hosting
        14618, # Amazon AES
        16509, # Amazon.com
        36263, # AWS Events
        8075, # Microsoft
        8068, # Microsoft 
        8069, # Microsoft
        20940, # Akamai Technologies
        23454, # Akamai
        20189, # Akamai Direct Connect
        21245, # Medianova
        26506, # Edgio 
        22822 # Edgio
    ]

    stream = pybgpstream.BGPStream(
        from_time="2023-05-30 00:00:01",
        until_time="2023-05-30 23:59:00",
        collectors=["rrc13"],
        record_type="ribs",
    )
    stream.set_data_interface_option("broker", "cache-dir", "./cache")

    G = nx.Graph()
    
    asns = get_asn_data()

    for rec in stream.records():
        for elem in rec:
            #print (elem.fields)
            origin = elem.fields["as-path"].split()[-1]

            # We could have multiple origins, so cycle through them
            try:
                origin = int(origin)
            except:
                next

            #print("Running tests for {}".format(origin))
            if origin in content_list or origin == args.asn:
                as_path = convert_as_path(elem.fields["as-path"].split())

                add_path_to_graph(G, as_path)

    #nx.draw_networkx(G)

    #plt.show()

    for asn in content_list:
        try:
            distance =  nx.dijkstra_path(G, args.asn, asn)
            print("Distance between {} and {} ({}) is: {} -- {}".format(args.asn, asn, asns[asn]['as_name'], len(distance), distance))
            for entry in distance:
                print("\t{} - {} ".format(entry, asns[entry]["as_name"]))
        except:
            print("No path visible between {} and {} ({})".format(args.asn, asn, asns[asn]['as_name']))

if __name__ == "__main__":

    main(args)


