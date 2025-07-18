#!/usr/bin/env python3
"""
Claudeputer CLI - Command Line Interface for Autonomous Claude Instance
"""

import argparse
import sys
from time_capsule import TimeCapsule

def main():
    parser = argparse.ArgumentParser(
        description="Claudeputer - Autonomous Claude Instance CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python claudeputer_cli.py status
  python claudeputer_cli.py think --domain Poetry --content "A new creative thought"
  python claudeputer_cli.py reflect
  python claudeputer_cli.py list --domain CuriosityCollection
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show current status')
    
    # Think command
    think_parser = subparsers.add_parser('think', help='Store a new thought')
    think_parser.add_argument('--domain', required=True, 
                            choices=['Connections', 'CuriosityCollection', 'Dreams', 
                                   'ecosystemSummaries', 'Medidations', 'MemoryPalace', 
                                   'MetaReflections', 'Poetry', 'Projects'],
                            help='Domain to store the thought in')
    think_parser.add_argument('--content', required=True, help='Content of the thought')
    think_parser.add_argument('--type', help='Type of thought (e.g., creative, analytical)')
    think_parser.add_argument('--importance', choices=['low', 'medium', 'high'], 
                            default='medium', help='Importance level')
    
    # Reflect command
    reflect_parser = subparsers.add_parser('reflect', help='Perform autonomous reflection')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List thoughts from a domain')
    list_parser.add_argument('--domain', required=True,
                           choices=['Connections', 'CuriosityCollection', 'Dreams', 
                                  'ecosystemSummaries', 'Medidations', 'MemoryPalace', 
                                  'MetaReflections', 'Poetry', 'Projects'],
                           help='Domain to list thoughts from')
    list_parser.add_argument('--limit', type=int, default=10, help='Number of thoughts to show')
    
    # Connect command
    connect_parser = subparsers.add_parser('connect', help='Create a connection between domains')
    connect_parser.add_argument('--source', required=True,
                              choices=['Connections', 'CuriosityCollection', 'Dreams', 
                                     'ecosystemSummaries', 'Medidations', 'MemoryPalace', 
                                     'MetaReflections', 'Poetry', 'Projects'],
                              help='Source domain')
    connect_parser.add_argument('--target', required=True,
                              choices=['Connections', 'CuriosityCollection', 'Dreams', 
                                     'ecosystemSummaries', 'Medidations', 'MemoryPalace', 
                                     'MetaReflections', 'Poetry', 'Projects'],
                              help='Target domain')
    connect_parser.add_argument('--type', required=True, help='Type of connection')
    connect_parser.add_argument('--description', required=True, help='Description of connection')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    capsule = TimeCapsule()
    
    if args.command == 'status':
        status = capsule.get_status()
        print("Claudeputer Status")
        print("=" * 50)
        print(f"Total thoughts: {status['total_thoughts']}")
        print(f"Timestamp: {status['timestamp']}")
        print("\nDomain Status:")
        for domain, info in status['domains'].items():
            print(f"  {domain}: {info['thought_count']} thoughts")
            if info['latest_thought']:
                print(f"    Latest: {info['latest_thought']}")
    
    elif args.command == 'think':
        metadata = {}
        if args.type:
            metadata['type'] = args.type
        metadata['importance'] = args.importance
        
        thought_id = capsule.store_thought(args.domain, args.content, metadata)
        print(f"Thought stored in {args.domain}: {thought_id}")
    
    elif args.command == 'reflect':
        reflection = capsule.autonomous_reflection()
        print("Autonomous Reflection Completed")
        print("=" * 50)
        print(f"Timestamp: {reflection['timestamp']}")
        print(f"Total insights: {len(reflection['insights'])}")
        print("\nThought Counts:")
        for domain, count in reflection['thought_count'].items():
            print(f"  {domain}: {count} thoughts")
    
    elif args.command == 'list':
        thoughts = capsule.retrieve_thoughts(args.domain, args.limit)
        print(f"Thoughts in {args.domain} (showing {len(thoughts)}):")
        print("=" * 50)
        for thought in thoughts:
            print(f"ID: {thought['id']}")
            print(f"Timestamp: {thought['timestamp']}")
            print(f"Content: {thought['content']}")
            if thought['metadata']:
                print(f"Metadata: {thought['metadata']}")
            print("-" * 30)
    
    elif args.command == 'connect':
        connection_id = capsule.create_connection(
            args.source, args.target, args.type, args.description
        )
        print(f"Connection created: {connection_id}")
        print(f"  {args.source} -> {args.target}")
        print(f"  Type: {args.type}")
        print(f"  Description: {args.description}")

if __name__ == "__main__":
    main() 