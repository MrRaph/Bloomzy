#!/usr/bin/env python3
"""
Service Registration Script for Consul
"""
import consul
import os
import sys
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_service(service_name, service_id, address, port, health_check_url, tags=None):
    """Register a service with Consul"""
    try:
        # Connect to Consul
        consul_host = os.environ.get('CONSUL_HOST', 'localhost')
        consul_port = int(os.environ.get('CONSUL_PORT', 8500))
        
        c = consul.Consul(host=consul_host, port=consul_port)
        
        # Register service
        c.agent.service.register(
            name=service_name,
            service_id=service_id,
            address=address,
            port=port,
            tags=tags or [],
            check=consul.Check.http(health_check_url, interval="10s", timeout="5s")
        )
        
        logger.info(f"Service {service_name} registered successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to register service {service_name}: {e}")
        return False

def deregister_service(service_id):
    """Deregister a service from Consul"""
    try:
        # Connect to Consul
        consul_host = os.environ.get('CONSUL_HOST', 'localhost')
        consul_port = int(os.environ.get('CONSUL_PORT', 8500))
        
        c = consul.Consul(host=consul_host, port=consul_port)
        
        # Deregister service
        c.agent.service.deregister(service_id)
        
        logger.info(f"Service {service_id} deregistered successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to deregister service {service_id}: {e}")
        return False

def discover_service(service_name):
    """Discover services by name"""
    try:
        # Connect to Consul
        consul_host = os.environ.get('CONSUL_HOST', 'localhost')
        consul_port = int(os.environ.get('CONSUL_PORT', 8500))
        
        c = consul.Consul(host=consul_host, port=consul_port)
        
        # Get healthy services
        services = c.health.service(service_name, passing=True)
        
        healthy_services = []
        for service in services[1]:
            healthy_services.append({
                'id': service['Service']['ID'],
                'address': service['Service']['Address'],
                'port': service['Service']['Port'],
                'tags': service['Service']['Tags']
            })
        
        return healthy_services
        
    except Exception as e:
        logger.error(f"Failed to discover service {service_name}: {e}")
        return []

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python register-service.py <action> [args...]")
        print("Actions:")
        print("  register <service_name> <service_id> <address> <port> <health_check_url> [tags]")
        print("  deregister <service_id>")
        print("  discover <service_name>")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "register":
        if len(sys.argv) < 7:
            print("Usage: register <service_name> <service_id> <address> <port> <health_check_url> [tags]")
            sys.exit(1)
        
        service_name = sys.argv[2]
        service_id = sys.argv[3]
        address = sys.argv[4]
        port = int(sys.argv[5])
        health_check_url = sys.argv[6]
        tags = sys.argv[7].split(',') if len(sys.argv) > 7 else None
        
        success = register_service(service_name, service_id, address, port, health_check_url, tags)
        sys.exit(0 if success else 1)
    
    elif action == "deregister":
        if len(sys.argv) < 3:
            print("Usage: deregister <service_id>")
            sys.exit(1)
        
        service_id = sys.argv[2]
        success = deregister_service(service_id)
        sys.exit(0 if success else 1)
    
    elif action == "discover":
        if len(sys.argv) < 3:
            print("Usage: discover <service_name>")
            sys.exit(1)
        
        service_name = sys.argv[2]
        services = discover_service(service_name)
        print(json.dumps(services, indent=2))
        sys.exit(0)
    
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()