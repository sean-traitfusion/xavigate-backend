#!/usr/bin/env python3
"""
Emergency cleanup script for oversized session memory
"""
import os
import sys
import psycopg2
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_db_connection():
    """Get database connection"""
    # For production, connect to the Docker container
    return psycopg2.connect(
        host="127.0.0.1",  # Docker binds to localhost
        port="5432",
        database="xavigate",
        user="postgres",
        password="changeme"  # Production password
    )

def cleanup_oversized_sessions():
    """Find and clean up oversized session memories"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Find sessions with oversized memory
        print("🔍 Finding oversized sessions...")
        cur.execute("""
            SELECT session_id, COUNT(*) as msg_count, 
                   SUM(LENGTH(role) + LENGTH(message) + 4) as total_chars
            FROM session_memory
            GROUP BY session_id
            HAVING SUM(LENGTH(role) + LENGTH(message) + 4) > 15000
            ORDER BY total_chars DESC
        """)
        
        oversized_sessions = cur.fetchall()
        
        if not oversized_sessions:
            print("✅ No oversized sessions found!")
            return
        
        print(f"\n❗ Found {len(oversized_sessions)} oversized sessions:")
        for session_id, msg_count, total_chars in oversized_sessions:
            print(f"  - Session {session_id}: {msg_count} messages, {total_chars:,} chars")
        
        # Clean up each oversized session
        response = input("\n🗑️ Do you want to clear these sessions? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Cleanup cancelled")
            return
        
        for session_id, msg_count, total_chars in oversized_sessions:
            print(f"\n🧹 Clearing session {session_id} ({total_chars:,} chars)...")
            
            # First, archive the conversation (optional)
            if total_chars < 100000:  # Only archive if not too huge
                cur.execute("""
                    SELECT role, message, created_at 
                    FROM session_memory 
                    WHERE session_id = %s 
                    ORDER BY created_at ASC
                """, (session_id,))
                
                messages = cur.fetchall()
                archive_path = f"/tmp/session_backup_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                
                with open(archive_path, 'w') as f:
                    for role, message, created_at in messages:
                        f.write(f"[{created_at}] {role}: {message}\n")
                
                print(f"  📁 Backed up to {archive_path}")
            
            # Clear the session
            cur.execute("DELETE FROM session_memory WHERE session_id = %s", (session_id,))
            print(f"  ✅ Cleared {msg_count} messages")
        
        conn.commit()
        print("\n✅ All oversized sessions cleared!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def check_specific_session(session_id):
    """Check a specific session's memory size"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT COUNT(*) as msg_count, 
                   SUM(LENGTH(role) + LENGTH(message) + 4) as total_chars
            FROM session_memory
            WHERE session_id = %s
        """, (session_id,))
        
        msg_count, total_chars = cur.fetchone()
        
        if total_chars:
            print(f"\n📊 Session {session_id}:")
            print(f"  - Messages: {msg_count}")
            print(f"  - Total chars: {total_chars:,}")
            print(f"  - Status: {'⚠️ OVERSIZED' if total_chars > 15000 else '✅ OK'}")
        else:
            print(f"\n❌ No data found for session {session_id}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cur.close()
        conn.close()

def main():
    """Main function"""
    print("🚀 Session Memory Cleanup Tool")
    
    if len(sys.argv) > 1:
        # Check specific session
        session_id = sys.argv[1]
        check_specific_session(session_id)
    else:
        # Find and clean all oversized sessions
        cleanup_oversized_sessions()

if __name__ == "__main__":
    main()