import streamlit as st
import os
import psycopg2
from sqlalchemy import create_engine, text
from uuid import uuid4

def debug_environment_variables():
    """Debug function to show all environment variables"""
    st.write("## 🔍 Environment Variables Debug")
    
    # Show all environment variables containing database-related keywords
    db_vars = {}
    all_vars = {}
    
    for key, value in os.environ.items():
        all_vars[key] = value[:50] + "..." if len(value) > 50 else value
        if any(keyword in key.upper() for keyword in ['DATABASE', 'PG', 'POSTGRES', 'DB']):
            db_vars[key] = value[:50] + "..." if len(value) > 50 else value
    
    st.write("### Database-related environment variables:")
    if db_vars:
        for key, value in db_vars.items():
            st.write(f"- **{key}**: `{value}`")
    else:
        st.error("❌ No database-related environment variables found!")
    
    # Show total count
    st.write(f"### Total environment variables: {len(all_vars)}")
    
    with st.expander("Show all environment variables"):
        for key, value in sorted(all_vars.items()):
            st.write(f"- **{key}**: `{value}`")
    
    return db_vars

def test_database_connection_simple():
    """Simple database connection test"""
    st.write("## 🧪 Database Connection Test")
    
    # Try to find database URL
    possible_vars = ["DATABASE_URL", "DATABASE_PUBLIC_URL", "DATABASE_PRIVATE_URL", "POSTGRES_URL"]
    database_url = None
    found_var = None
    
    for var_name in possible_vars:
        if var_name in os.environ:
            database_url = os.environ[var_name]
            found_var = var_name
            break
    
    if not database_url:
        st.error("❌ No database URL found in environment variables!")
        return False
    
    st.success(f"✅ Found database URL in: `{found_var}`")
    st.write(f"URL format: `{database_url[:30]}...`")
    
    # Test connection with psycopg2 (simpler than SQLAlchemy)
    try:
        st.write("Attempting to connect...")
        
        # Add SSL mode if not present
        if "sslmode=" not in database_url:
            database_url += "?sslmode=require"
        
        # Test connection
        conn = psycopg2.connect(
            database_url,
            connect_timeout=10
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        
        st.success(f"✅ Database connection successful!")
        st.write(f"PostgreSQL version: {version[0][:100]}...")
        return True
        
    except psycopg2.OperationalError as e:
        st.error(f"❌ Connection failed: {str(e)}")
        
        # Provide specific guidance based on error
        error_str = str(e).lower()
        if "could not connect to server" in error_str:
            st.error("**Possible issues:**")
            st.error("1. PostgreSQL service is not running")
            st.error("2. Incorrect host/port in connection string")
            st.error("3. Network connectivity issues")
        elif "authentication failed" in error_str:
            st.error("**Authentication issue:**")
            st.error("1. Wrong username/password")
            st.error("2. Database user doesn't exist")
        elif "database" in error_str and "does not exist" in error_str:
            st.error("**Database doesn't exist:**")
            st.error("1. Database name is incorrect")
            st.error("2. Database hasn't been created yet")
        
        return False
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return False

def test_railway_service_linking():
    """Test if Railway services are properly linked"""
    st.write("## 🚂 Railway Service Linking Test")
    
    # Check for Railway-specific environment variables
    railway_vars = [
        "RAILWAY_PROJECT_ID",
        "RAILWAY_ENVIRONMENT_ID", 
        "RAILWAY_SERVICE_ID",
        "RAILWAY_DEPLOYMENT_ID"
    ]
    
    railway_found = False
    for var in railway_vars:
        if var in os.environ:
            st.write(f"✅ {var}: `{os.environ[var]}`")
            railway_found = True
        else:
            st.write(f"❌ {var}: Not found")
    
    if not railway_found:
        st.warning("⚠️ No Railway environment variables found. Are you running on Railway?")
    
    return railway_found

@st.cache_resource
def get_database_connection():
    """Create database connection with detailed logging"""
    try:
        # Try different methods to get DATABASE_URL
        database_url = None
        found_var = None
        
        # Method 1: Try Railway environment variables (multiple possible names)
        railway_vars = ["DATABASE_URL", "DATABASE_PUBLIC_URL", "DATABASE_PRIVATE_URL", "POSTGRES_URL"]
        for var_name in railway_vars:
            if var_name in os.environ:
                database_url = os.environ[var_name]
                found_var = var_name
                print(f"✅ Found {var_name} in environment variables")
                break
        
        if not database_url:
            print("❌ DATABASE_URL not found! Available environment variables:")
            for key, value in os.environ.items():
                if 'DATABASE' in key or 'PG' in key or 'POSTGRES' in key:
                    print(f"   {key}: {value[:50]}...")
            return None
        
        # Clean up the URL (Railway sometimes adds extra parameters)
        if "?sslmode=" not in database_url:
            database_url += "?sslmode=require"
        
        print(f"🔗 Connecting to database using {found_var}: {database_url[:50]}...")
        
        # Create engine with Railway-optimized settings
        engine = create_engine(
            database_url,
            connect_args={
                "connect_timeout": 30,
                "application_name": "budget_buddy_railway",
                "sslmode": "require"
            },
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=3600,
            pool_pre_ping=True,
            echo=False
        )
        
        # Test the connection
        print("🧪 Testing database connection...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            test_result = result.fetchone()
            if test_result[0] == 1:
                print("✅ Database connection successful!")
            else:
                raise Exception("Connection test failed")
        
        return engine
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Database connection error: {error_msg}")
        return None

def main():
    st.title("🔧 Database Connection Debugger")
    st.write("This tool will help diagnose your Railway database connection issues.")
    
    # Run debug tests
    debug_environment_variables()
    test_railway_service_linking()
    connection_success = test_database_connection_simple()
    
    if connection_success:
        st.success("🎉 Database connection is working! Your app should work now.")
    else:
        st.error("❌ Database connection failed. Please check the issues above.")
        
        st.write("## 🛠️ Next Steps:")
        st.write("1. **Check Railway Dashboard**: Make sure your PostgreSQL service is running (green status)")
        st.write("2. **Link Services**: In your Budget-Buddy service, go to Variables → Add Variable Reference → Select your Postgres service")
        st.write("3. **Verify Connection String**: Make sure the DATABASE_URL format is correct")
        st.write("4. **Check Service Logs**: Look at the logs in your Railway PostgreSQL service for any errors")
        
        if st.button("🔄 Retry Connection Test"):
            st.rerun()

if __name__ == "__main__":
    main()