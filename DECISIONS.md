### 2024-12-05: Data Storage Choice
**Context:** Needed to choose between SQLite and PostgreSQL
**Decision:** Selected SQLite
**Rationale:**
- Simpler deployment
- Single user application
- No complex concurrent access needed
- No idea how to use another database and don't have time to learn

### 2024-12-05: Data choice
**Context:** Needed to choose between downloading data vs connecting to API
**Decision:** Downloading CSV data
**Rationale:**
- Avoid need to figure out the API connection with limited time
- CSV should be easy format to use (no data types but can add with pandas script)

### 2024-12-06: Data choice
**Context:** Needed to choose between spending time on data cleaning and prep vs dummy data
**Decision:** Using dummy data so I could get on with building the web pages. I'll sort out real data if I have time
**Rationale:**
- I don't have time to prep the data, and don't want to spend time on it when I don't need to
- Priority is getting a working site up and running
- No point having good data if I can't get the rest of it to work