#!/usr/bin/env python3

import argparse
from jinja2 import Environment, FileSystemLoader
import os
import sys
import yaml

def main(args):

  d = {}
  d["NodeId"] = int(args.node_num)
  d["Uplink"] = args.uplink if args.uplink else "Gi0/0/0/0"
  d["NodePeers"] = [int(n) for n in args.node_nei_str.split(',')]

  pwd = os.path.dirname(os.path.abspath(__file__))
  env = Environment(loader=FileSystemLoader(pwd))

  print(env.get_template(args.template if args.template else "main_template.j2").render(d))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='INE-Style XRv Config Generator for Large Labs')
  parser.add_argument("node_num", help="Numerical ID of this node.")
  parser.add_argument("node_nei_str", help="Comma-delimited list of nodes this node attaches to.")
  parser.add_argument("--uplink", help="Physical uplink from which to create subinterfaces")
  parser.add_argument("--template", help="J2 template to use (From pwd)")
  main(parser.parse_args())
