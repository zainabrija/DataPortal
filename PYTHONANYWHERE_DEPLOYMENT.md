# 🐍 PythonAnywhere Deployment Guide for PBS Data Portal

This guide will walk you through deploying your PBS Data Portal Flask application to PythonAnywhere - a reliable, Python-focused hosting platform.

## 🌟 **Why PythonAnywhere?**

- ✅ **Free tier available** (no credit card required)
- ✅ **Python-focused** hosting (perfect for Flask)
- ✅ **Reliable deployment** (no snapshot issues)
- ✅ **Easy web interface** (no complex CLI)
- ✅ **Good performance** for Flask applications
- ✅ **Built-in SSL** certificates

## 📋 **Prerequisites**

1. **PythonAnywhere Account**: Sign up at [pythonanywhere.com](https://pythonanywhere.com)
2. **GitHub Repository**: Your code must be on GitHub
3. **Python 3.8+**: PythonAnywhere supports modern Python versions

## 🚀 **Step-by-Step Deployment**

### **Step 1: Sign Up for PythonAnywhere**

1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Click **"Create a Beginner account"** (free)
3. **No credit card required** for free tier
4. Choose a username (e.g., `zainabrija`)
5. Verify your email

### **Step 2: Access Your Dashboard**

1. **Log in** to PythonAnywhere
2. You'll see your **dashboard** with various tools
3. **Free tier includes**:
   - 1 web app
   - 512 MB storage
   - 1 CPU core
   - Custom domain support

### **Step 3: Clone Your Repository**

1. **Click "Files"** in the left sidebar
2. **Click "Bash"** to open a terminal
3. **Clone your repo**:
   ```bash
   git clone https://github.com/zainabrija/DataPortal.git
   cd DataPortal
   ```

### **Step 4: Install Dependencies**

1. **In the Bash terminal**:

   ```bash
   pip install --user -r requirements.txt
   ```

2. **Verify installation**:
   ```bash
   python -c "import flask; print('Flask installed successfully')"
   ```

### **Step 5: Configure Your Web App**

1. **Click "Web"** in the left sidebar
2. **Click "Add a new web app"**
3. **Choose "Flask"** as the framework
4. **Select Python 3.8** or higher
5. **Set path**: `/home/yourusername/DataPortal/app.py`

### **Step 6: Configure WSGI File**

1. **Click on your web app** in the Web section
2. **Click "WSGI configuration file"**
3. **Replace the content** with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/DataPortal'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import your Flask app
from app import app as application

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-secret-key-here'

# For debugging
if __name__ == "__main__":
    application.run()
```

**Replace `yourusername` with your actual PythonAnywhere username**

### **Step 7: Set Environment Variables**

1. **In the Web app configuration**
2. **Add these environment variables**:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///pbs_portal.db
   ```

### **Step 8: Reload Your Web App**

1. **Click "Reload"** button
2. **Wait for reload** to complete
3. **Check for any errors** in the error log

## 🌐 **Access Your Deployed App**

Your app will be available at:

- **URL**: `https://yourusername.pythonanywhere.com`
- **Admin Login**:
  - Email: `admin@pbs.gov.pk`
  - Password: `admin123`

## 🔧 **PythonAnywhere-Specific Features**

### **File Management**

- **Web-based file editor** (no need for Git on server)
- **Easy file uploads** and downloads
- **Built-in text editor** for quick fixes

### **Database Support**

- **SQLite** (included, perfect for your app)
- **MySQL** (available on paid plans)
- **PostgreSQL** (available on paid plans)

### **SSL Certificates**

- **Automatic HTTPS** (no configuration needed)
- **Custom domains** supported
- **Professional hosting** appearance

## 💰 **PythonAnywhere Pricing**

### **Free Tier**

- **1 web app**
- **512 MB storage**
- **1 CPU core**
- **Custom domain support**
- **Perfect for development and small apps**

### **Paid Plans**

- **Hacker**: $5/month (more resources)
- **Developer**: $12/month (professional features)
- **Professional**: $99/month (enterprise features)

## 🔍 **Troubleshooting**

### **Common Issues & Solutions**

| Issue                        | Solution                          |
| ---------------------------- | --------------------------------- |
| **Import errors**            | Check sys.path in WSGI file       |
| **Database errors**          | Ensure database file is writable  |
| **Static files not loading** | Check static folder configuration |
| **App not reloading**        | Check WSGI file syntax            |

### **Check Logs**

1. **Click "Web"** in sidebar
2. **Click on your web app**
3. **View "Error log"** for debugging
4. **View "Server log"** for general info

## 📊 **Monitoring Your App**

### **PythonAnywhere Dashboard**

- **Real-time status** of your web app
- **Resource usage** monitoring
- **Error tracking** and debugging
- **Performance metrics**

### **File Management**

- **Easy file editing** through web interface
- **Git integration** for version control
- **Backup and restore** capabilities

## 🚀 **Next Steps After Deployment**

1. **Custom Domain**: Add your own domain name
2. **Database Upgrade**: Consider MySQL/PostgreSQL for production
3. **Monitoring**: Set up alerts and notifications
4. **Backup**: Implement automated backups
5. **SSL**: Already included automatically

## ✅ **Deployment Checklist**

- [ ] PythonAnywhere account created
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Web app configured
- [ ] WSGI file updated
- [ ] Environment variables set
- [ ] Web app reloaded
- [ ] App accessible via URL
- [ ] Admin login working
- [ ] Database accessible

## 📞 **Getting Help**

- **PythonAnywhere Documentation**: [help.pythonanywhere.com](https://help.pythonanywhere.com)
- **Community Forum**: Very active and helpful
- **Email Support**: Available for all users

---

**Congratulations!** 🎉 Your PBS Data Portal is now live on PythonAnywhere!

**Next**: Follow the steps above to deploy your app!

