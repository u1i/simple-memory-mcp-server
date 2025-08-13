import asyncio
import logging
import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

# Initialize your FastMCP server
mcp = FastMCP("LongTermMemoryMCP")

# Database setup
DB_PATH = "user_memory.db"

def init_database():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create simple facts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL DEFAULT 'default',
            fact TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create index for user lookup
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON user_facts(user_id)")
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

@mcp.tool()
def store_user_info(
    fact: str,
    user_id: str = "default"
) -> str:
    """
    Store a single piece of information about the user.
    
    IMPORTANT: Only store SHORT, CONDENSED facts - NOT long explanations or conversations!
    Think of this as storing key highlights or nuggets from conversations.
    Maximum 1-2 sentences. Focus on the essential information only.
    
    GOOD examples:
    - "The user lives in Singapore"
    - "The user has a cat called Wendy"
    - "The user prefers Python over JavaScript"
    - "The user works as a software engineer"
    - "The user is building an e-commerce API"
    
    BAD examples (too long/detailed):
    - "The user told me a long story about how they moved to Singapore last year because of work and they really like it there but miss their family back home..."
    - "The user explained their entire programming background including all the languages they've learned and projects they've worked on..."
    
    Args:
        fact: A SHORT, condensed fact about the user (1-2 sentences max)
        user_id: User identifier (defaults to "default")
    
    Returns:
        Confirmation message
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO user_facts (user_id, fact)
            VALUES (?, ?)
        """, (user_id, fact))
        
        fact_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Stored fact: {fact} (ID: {fact_id})")
        return f"Stored: {fact}"
        
    except Exception as e:
        logger.error(f"Error storing fact: {e}")
        return f"Error storing fact: {str(e)}"

@mcp.tool()
def get_user_info(
    user_id: str = "default"
) -> str:
    """
    Retrieve all stored information about the user.
    
    Use this tool to recall everything you know about the user.
    This returns all stored facts in a simple, readable format.
    
    Args:
        user_id: User identifier (defaults to "default")
    
    Returns:
        A text summary of everything known about the user
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT fact, created_at
            FROM user_facts 
            WHERE user_id = ?
            ORDER BY created_at ASC
        """, (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return "I don't have any information stored about this user yet."
        
        info_text = "Here's what I know about the user:\n\n"
        for i, (fact, created_at) in enumerate(results, 1):
            info_text += f"{i}. {fact}\n"
        
        logger.info(f"Retrieved {len(results)} facts for user {user_id}")
        return info_text
        
    except Exception as e:
        logger.error(f"Error retrieving user info: {e}")
        return f"Error retrieving user info: {str(e)}"











if __name__ == "__main__":
    # Initialize database on startup
    init_database()
    
    print("Starting Long-Term Memory MCP server...")
    print(f"Database location: {os.path.abspath(DB_PATH)}")
    
    # To run remotely using Streamable HTTP
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
    print("Long-Term Memory MCP server stopped.")
