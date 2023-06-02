# path_distance
Analyse the distance between a given ASN and a series of content networks

This script uses BGPStream as data source.  It generates a graph using all the paths where the origins are either the ASN provided or one of the ASNs in the __content_list__ list, and then proceeds to calculate the shortest path between the two using the Dijkstra algorithm.
Because of the data source and the way the script generates its graph, there are a number of limitations.  This is "good enough" for the initial goal of the script.

## Usage

```shell
# ./path_distance.py 58280
```

where AS58280 is the one you would like to use as measure.

## Install

First of all, you need to install BGPStream.

On OSX, I recommend using brew:

```shell
# brew install bgpstream
```

this will install the necessary libraries.

Then you would need to create a virtualenv for python

```shell
# python3 -m venv ./venv
```

and install the necessary dependencies

```shell
# source ./venv/bin/activate
(venv) # pip3 install requests matplotlib networkx
(venv) # pip3 install --global-option=build_ext --global-option="-I/opt/homebrew/include" --global-option="-L/opt/homebrew/opt/bgpstream/lib" pybgpstream
```

Now you're ready to execute it.

