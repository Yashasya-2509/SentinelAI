# Security Notes
- Defensive use only; analyse data you are authorized to process.
- The API has no authentication yet. Do not expose it publicly before adding auth.
- Model artifacts are joblib/pickle files: load only artifacts you trained yourself.
- Uploaded CSVs are untrusted input; schema validation is enforced but not a full sandbox.
- Never commit real network captures or credentials (see .gitignore).
