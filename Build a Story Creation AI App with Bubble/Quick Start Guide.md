# Quick Start Guide

Get your Story AI Backend up and running in minutes with this streamlined setup guide.

## Prerequisites

- AWS account with EC2 access
- Hugging Face account with API key
- ElevenLabs account with API key
- SSH client (Terminal on Mac/Linux, PuTTY on Windows)

## 1. Launch EC2 Instance

1. **Login to AWS Console** → EC2 → Launch Instance
2. **Choose AMI**: Ubuntu 22.04 LTS
3. **Instance Type**: t3.medium (recommended for start)
4. **Key Pair**: Create new or select existing
5. **Security Group**: Allow SSH (22), HTTP (80), HTTPS (443)
6. **Storage**: 20 GB gp3
7. **Launch Instance**

## 2. Connect and Setup

```bash
# Connect to your instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip git nginx supervisor -y

# Create application user
sudo adduser storyai
sudo usermod -aG sudo storyai
sudo su - storyai
```

## 3. Deploy Application

```bash
# Upload your application files or clone repository
# If you have the files locally, use SCP:
# scp -i your-key.pem -r story_ai_backend ubuntu@your-instance-ip:/home/ubuntu/

# Move to application directory
cd story_ai_backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 4. Configure Environment

```bash
# Create environment file
cp .env.example .env
nano .env
```

Add your API keys:
```
HUGGINGFACE_API_KEY=your_huggingface_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
SECRET_KEY=your_secret_key_here
```

## 5. Initialize Database

```bash
# Initialize database
python scripts/init_db.py init

# Create sample data (optional)
python scripts/init_db.py sample
```

## 6. Test Locally

```bash
# Start development server
python src/main.py

# In another terminal, test the API
curl http://localhost:5000/api/status
```

## 7. Configure Production (Supervisor)

```bash
# Create supervisor config
sudo nano /etc/supervisor/conf.d/storyai.conf
```

Add configuration:
```ini
[program:storyai]
command=/home/storyai/story_ai_backend/venv/bin/python /home/storyai/story_ai_backend/src/main.py
directory=/home/storyai/story_ai_backend
user=storyai
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/storyai.log
```

```bash
# Start with supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start storyai
```

## 8. Configure Nginx (Optional)

```bash
# Create nginx config
sudo nano /etc/nginx/sites-available/storyai
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or your IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/storyai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 9. Test Production

```bash
# Test API endpoints
curl http://your-instance-ip/api/status
curl http://your-instance-ip/api/health

# Test character creation
curl -X POST http://your-instance-ip/api/characters \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "perspective": "1st_person", "gender": "male", "career": "ceo", "image_style": "anime"}'
```

## 10. Bubble.io Integration

1. **In Bubble.io**: Add API Connector plugin
2. **API Root URL**: `http://your-instance-ip/api` (or your domain)
3. **Add API calls** for characters, stories, subscriptions
4. **Create data types** matching API responses
5. **Build your UI** following the integration guide

## Quick Test Commands

```bash
# Check service status
sudo supervisorctl status storyai

# View logs
sudo tail -f /var/log/storyai.log

# Restart service
sudo supervisorctl restart storyai

# Check database
ls -la src/database/

# Test API health
curl http://localhost:5000/api/health
```

## Common Issues

**Service won't start**: Check logs with `sudo tail -f /var/log/storyai.log`

**API calls fail**: Verify security group allows traffic on port 80/443

**Database errors**: Run `python scripts/init_db.py reset` to recreate database

**AI services not working**: Verify API keys in `.env` file

## Next Steps

1. **SSL Certificate**: Use Let's Encrypt for HTTPS
2. **Domain Name**: Point your domain to the instance
3. **Monitoring**: Set up CloudWatch monitoring
4. **Backups**: Configure automated backups
5. **Scaling**: Plan for load balancing as you grow

## Support

- Check `API_DOCUMENTATION.md` for API details
- Review `DEPLOYMENT_GUIDE.md` for comprehensive setup
- See `BUBBLE_INTEGRATION.md` for frontend integration
- Check `TEST_RESULTS.md` for testing information

Your Story AI Backend is now ready to power your Bubble.io frontend! 🚀

