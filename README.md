# Pakistan Bureau of Statistics (PBS) Open Data Portal

A comprehensive CRUD-based web application for the Pakistan Bureau of Statistics Open Data Portal, built with Python Flask and SQLite.

## 🚀 **Quick Deploy on Railway (Recommended)**

**Deploy in 5 minutes with Railway:**

1. Push your code to GitHub
2. Connect to [Railway.app](https://railway.app)
3. Deploy automatically!

**See `RAILWAY_DEPLOYMENT.md` for detailed instructions.**

## Features

### User Features

- **User Registration & Authentication**: Complete user registration with personal details
- **Data Request Management**: Submit, view, edit, and cancel data requests
- **Dashboard**: Track all your data requests with status updates
- **Open Data Access**: Browse and search available datasets
- **Multiple Data Formats**: Support for CSV, Excel, PDF, and JSON formats

### Admin Features

- **Admin Dashboard**: Manage all data requests from users
- **Status Management**: Update request status and payment status
- **User Management**: View user details and request history
- **Export Functionality**: Export request data for reporting

### Technical Features

- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Updates**: AJAX-powered status updates
- **Form Validation**: Client and server-side validation
- **Security**: Password hashing and user authentication
- **Database**: SQLite with SQLAlchemy ORM

## Screenshots

The application includes the following key interfaces:

1. **Home Page**: Hero section with portal features and recent datasets
2. **User Dashboard**: Data requests table with view/edit/cancel actions
3. **Admin Dashboard**: Comprehensive request management with status dropdowns
4. **Data Request Form**: Multi-section form with personal details, data requirements, and timeline
5. **Open Data**: Dataset browsing with search and filter capabilities

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd DataPortal

# Or simply download and extract the project files
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 4: Access the Application

1. **Home Page**: `http://localhost:5000/`
2. **Register**: `http://localhost:5000/register`
3. **Login**: `http://localhost:5000/login`

### Default Admin Account

- **Email**: admin@pbs.gov.pk
- **Password**: admin123

## 🚂 **Railway Deployment (Recommended)**

Railway is the easiest way to deploy your Flask app:

- ✅ **Free tier available** ($5 credit/month)
- ✅ **Auto-detects Flask** applications
- ✅ **GitHub integration** for automatic deployments
- ✅ **Better performance** than other free tiers

**See `RAILWAY_DEPLOYMENT.md` for complete deployment guide.**

## Database Structure

### Users Table

- Personal information (name, email, CNIC, phone, etc.)
- Address details (city, district, province, nationality)
- Admin privileges flag

### Data Requests Table

- Request details (dataset name, purpose, format)
- Timeline information (requested date, deadline, urgency)
- Status tracking (pending, in progress, completed)
- Payment status

### Datasets Table

- Dataset information (name, description, category)
- Format and download tracking

## Customization

### Styling

The application uses Bootstrap 5 with custom CSS variables for theming. Main colors can be modified in `templates/base.html`:

```css
:root {
  --primary-color: #20c997;
  --secondary-color: #17a2b8;
  --accent-color: #28a745;
  --dark-color: #343a40;
  --light-color: #f8f9fa;
}
```

### Database Configuration

The application uses SQLite by default. To use a different database, modify the configuration in `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-uri'
```

### Adding New Features

1. **New Routes**: Add to `app.py`
2. **New Templates**: Create in `templates/` directory
3. **New Models**: Add to database models section in `app.py`

## Security Features

- Password hashing using Werkzeug
- User authentication with Flask-Login
- Form validation and CSRF protection
- Admin role-based access control
- Input sanitization and validation

## 🚀 **Deployment Options**

### **Railway (Recommended)**

- **Free tier**: $5 credit/month
- **Auto-deployment**: GitHub integration
- **Easy setup**: Auto-detects Flask

### **Local Development**

```bash
python app.py
```

### **Production Deployment**

For production deployment, consider:

1. **Web Server**: Use Gunicorn (already included)
2. **Database**: Switch to PostgreSQL or MySQL
3. **Environment Variables**: Use Railway dashboard
4. **HTTPS**: Railway provides SSL automatically
5. **Backup**: Implement database backup strategy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is developed for the Pakistan Bureau of Statistics. All rights reserved.

## Support

For technical support or questions:

- Email: data@pbs.gov.pk
- Phone: +92-51-925-xxxx

## Changelog

### Version 1.0.0

- Initial release
- Complete CRUD functionality
- User and admin dashboards
- Data request management
- Responsive design
- SQLite database
- Railway deployment ready
