#!/usr/bin/env python3
"""
Script to manage ENV variable across all microservice .env files
"""
import os
import sys

def update_env_files(env_value=None, remove=False):
    """Update or remove ENV from all service .env files"""
    
    services_dir = os.path.join(os.path.dirname(__file__), '..', 'microservices')
    
    for service in os.listdir(services_dir):
        env_path = os.path.join(services_dir, service, '.env')
        
        if not os.path.exists(env_path):
            continue
            
        # Read the file
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        # Process lines
        new_lines = []
        env_found = False
        
        for line in lines:
            if line.strip().startswith('ENV='):
                env_found = True
                if remove:
                    print(f"  Removing ENV from {service}/.env")
                    continue  # Skip this line
                elif env_value:
                    print(f"  Updating {service}/.env: ENV={env_value}")
                    new_lines.append(f"ENV={env_value}\n")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        # If ENV wasn't found and we're adding it
        if not env_found and env_value and not remove:
            print(f"  Adding ENV={env_value} to {service}/.env")
            new_lines.append(f"\nENV={env_value}\n")
        
        # Write back
        with open(env_path, 'w') as f:
            f.writelines(new_lines)

def main():
    print("🔧 Environment Configuration Manager")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python update_env_files.py remove    - Remove ENV from all service .env files")
        print("  python update_env_files.py dev       - Set ENV=dev in all service .env files")
        print("  python update_env_files.py prod      - Set ENV=prod in all service .env files")
        print("\nCurrent approach:")
        print("  - Remove ENV from service .env files to use root .env")
        print("  - Or set all to same value for consistency")
        return
    
    command = sys.argv[1].lower()
    
    if command == "remove":
        print("\nRemoving ENV from all service .env files...")
        print("This will make services use the root .env ENV value")
        update_env_files(remove=True)
        print("\n✅ Done! Services will now use root .env for ENV setting")
        
    elif command in ["dev", "prod"]:
        print(f"\nSetting ENV={command} in all service .env files...")
        update_env_files(env_value=command)
        print(f"\n✅ Done! All services set to ENV={command}")
        
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()