# Google Ad Manager Campaign Management

A Python library for programmatically managing campaigns in Google Ad Manager (GAM), including creation of orders, line items, and creatives.

## Features

- Create orders with specified advertisers
- Create line items with targeting and scheduling
- Create third-party creatives
- Automatic handling of currency and inventory targeting
- Timezone-aware scheduling

## Prerequisites

- Python 3.10 or higher
- Google Ad Manager account
- Google Cloud project with Ad Manager API enabled
- Service account with appropriate permissions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/StreetsDigital/google-ad-manager-tools.git
cd google-ad-manager-tools
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Set up your Google Ad Manager API access:
   - Create a project in Google Cloud Console
   - Enable the Google Ad Manager API
   - Create a service account and download the JSON key file

2. Set up your configuration files:
   - Copy `googleads.yaml.example` to `googleads.yaml`
   - Copy `service-account.json.example` to `service-account.json`
   - Update both files with your actual credentials

```bash
cp googleads.yaml.example googleads.yaml
cp service-account.json.example service-account.json
```

3. Update the configuration files with your credentials:
   - In `googleads.yaml`:
     - Set your network code
     - Update the path to your service account JSON file
   - In `service-account.json`:
     - Replace all placeholder values with your actual service account details

## Security Best Practices

### Credential Management

1. **Configuration Files**
   - Copy the example files to create your working copies:
     ```bash
     cp .env.example .env
     cp googleads.yaml.example googleads.yaml
     cp service-account.json.example service-account.json
     ```
   - Never commit real credentials to the repository
   - Store production credentials outside the project directory
   - Use environment variables for sensitive values

2. **Environment Variables**
   - All sensitive configuration should be stored in `.env`
   - Use `python-dotenv` to load environment variables
   - Different environments should have different `.env` files
   - Production credentials should be managed by your deployment platform

3. **Service Account Security**
   - Rotate service account keys regularly (recommended: every 90 days)
   - Use the principle of least privilege
   - Monitor service account usage
   - Store service account keys securely
   - Use separate service accounts for development and production

### Protected Files

The following files are protected by `.gitignore`:

```
service-account*.json     # Service account credentials
googleads*.yaml          # Google Ads configuration
.env                     # Environment variables
*.key, *.pem, *.crt     # Cryptographic keys
credentials/            # Credential directory
secrets/                # Secrets directory
```

### Security Recommendations

1. **Access Control**
   - Use role-based access control (RBAC) in Google Ad Manager
   - Regularly audit user and service account permissions
   - Remove unused service accounts and user access

2. **API Security**
   - Monitor API usage and set up alerts
   - Implement rate limiting
   - Use API quotas to prevent abuse
   - Keep the API version updated

3. **Development Security**
   - Use virtual environments
   - Regular security updates for dependencies
   - Code review for security concerns
   - Static code analysis for security issues

4. **Production Security**
   - Use secure environment variable management
   - Implement logging and monitoring
   - Regular security audits
   - Incident response plan

### Security Checklist

Before deploying:
- [ ] All sensitive files are in `.gitignore`
- [ ] No credentials in code or comments
- [ ] Environment variables configured
- [ ] Service account has minimum required permissions
- [ ] API version is current
- [ ] Dependencies are up to date
- [ ] Security logging is enabled
creative = create_creative(client, order['advertiserId'])
print(f"Created creative with ID: {creative['id']}")
```

### Running the Test Script

A test script is provided to demonstrate the full workflow:

```bash
python src/test_campaign.py
```

## Default Settings

- Line Items:
  - Type: STANDARD
  - Creative Size: 300x250
  - Cost Type: CPM
  - Duration: 1 year from creation
  - Impressions Goal: 100,000

- Creatives:
  - Type: Third Party
  - Size: 300x250
  - SafeFrame Compatible: Yes

## Error Handling

The library includes comprehensive error handling for common issues:
- Network connectivity problems
- Invalid credentials
- Missing permissions
- Invalid targeting settings
- Currency mismatches

## Logging

Detailed logging is enabled by default and includes:
- Operation progress
- Success confirmations
- Error details
- User and entity IDs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your License Here]

## Support

For support, please [create an issue](your-issue-tracker-url) or contact [your-contact-info]. 
