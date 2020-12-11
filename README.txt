GetInfo.py
  - Query information about one domain or all domiains using the interface prompt
  - MySQL table (domains.domainInfo) will refresh before query
  
CreateSnapshot.py
  - Create a snapshot for a domain using the user prompt (input domain name and create file name for new snapshot)
  - Automatically updates domains.snapshotInfo table
    
JoinTables.py
  - Creates a natural join between domainInfo and snapshotInfo tables
  - Use to return snapshots belonging to all or selected domains
  
    
