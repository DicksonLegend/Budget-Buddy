# 💰 Budget Buddy - Personal Finance Tracker

A modern, feature-rich personal finance tracker built with **Streamlit** and **PostgreSQL**. Track your income, expenses, and gain valuable insights into your spending patterns with an intuitive, responsive web interface.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28.0-FF4B4B.svg)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg)](https://www.postgresql.org/)
[![Railway](https://img.shields.io/badge/railway-deployed-success)](https://railway.app/)

![Budget Buddy Dashboard](https://budget-buddy-production-f944.up.railway.app/)

## ✨ Features

### 📊 **Dashboard**
- **Real-time Overview**: See your total income, expenses, and balance at a glance
- **Interactive Charts**: Beautiful visualizations using Plotly
- **Daily Balance Trends**: Track your financial progress over the last 30 days
- **Recent Transactions**: Quick view of your latest financial activities

### 💰 **Income & Expense Management**
- **Easy Transaction Entry**: Add income and expenses with predefined categories
- **Custom Categories**: Create your own categories for better organization
- **Bulk Data Operations**: Clear all data or export to CSV
- **Real-time Updates**: Instant updates across all views

### 📈 **Analytics & Insights**
- **Smart Insights**: AI-powered spending alerts and recommendations
- **Category Analysis**: Detailed breakdown of spending by category
- **Monthly Trends**: Track income vs expenses over time
- **Savings Rate Monitoring**: Keep track of your financial health

### 🎯 **Advanced Features**
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Dark Mode Support**: Automatic dark/light mode detection
- **Data Export**: Download your transactions as CSV
- **Secure Storage**: All data stored securely in PostgreSQL database
- **Session Management**: User-specific data isolation

## 🚀 Live Demo

Try Budget Buddy live: [Your Railway Deployment URL]

## 🛠️ Tech Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Backend Language | 3.11+ |
| **Streamlit** | Web Framework | 1.28.0 |
| **PostgreSQL** | Database | Latest |
| **Pandas** | Data Manipulation | 2.0.3 |
| **Plotly** | Data Visualization | 5.15.0 |
| **SQLAlchemy** | Database ORM | 2.0.19 |
| **Railway** | Cloud Deployment | - |

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- PostgreSQL database
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/DicksonLegend/Budget-Buddy.git
   cd Budget-Buddy
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.streamlit/secrets.toml` file:
   ```toml
   [database]
   DATABASE_URL = "postgresql://username:password@localhost:5432/budget_buddy"
   ```
   
   Or set environment variable:
   ```bash
   # Windows
   set DATABASE_URL=postgresql://username:password@localhost:5432/budget_buddy
   
   # macOS/Linux
   export DATABASE_URL=postgresql://username:password@localhost:5432/budget_buddy
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 🚁 Railway Deployment

Budget Buddy is optimized for [Railway](https://railway.app/) deployment with zero configuration.

### Deploy to Railway

1. **Fork this repository**

2. **Connect to Railway**
   - Sign up at [railway.app](https://railway.app/)
   - Connect your GitHub account
   - Select this repository

3. **Add PostgreSQL Database**
   - In your Railway project, click "New Service"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically provide the `DATABASE_URL`

4. **Deploy**
   - Railway will automatically detect the `Procfile`
   - Your app will be live in minutes!

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## 🏗️ Project Structure

```
Budget-Buddy/
├── app.py                 # Main Streamlit application
├── debug_version.py       # Database debugging utilities
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version specification
├── Procfile              # Railway deployment configuration
├── packages.txt          # System packages for Railway
├── README.md             # This file
└── .gitignore           # Git ignore rules
```

## 🎨 Features Overview

### Dashboard View
```python
# Key metrics displayed
✅ Total Income
✅ Total Expenses  
✅ Current Balance
✅ Daily trend charts
✅ Category breakdowns
```

### Transaction Management
```python
# Supported transaction types
📊 Income Categories:
   - Salary, Freelance, Business, Investment
   - Rental, Bonus, Commission, Dividend
   - Interest, Other (Custom)

💸 Expense Categories:
   - Food, Transportation, Utilities
   - Healthcare, Education, Entertainment
   - Shopping, Rent, Insurance, Groceries
   - Fuel, Bills, Travel, Subscription
   - Other (Custom)
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `PORT` | Application port (Railway auto-sets) | ❌ |

### Database Schema

```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,           -- 'Income' or 'Expense'
    category VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check your DATABASE_URL format
   postgresql://username:password@host:port/database
   
   # For Railway, ensure PostgreSQL service is linked
   ```

2. **App Won't Start Locally**
   ```bash
   # Verify Python version
   python --version  # Should be 3.11+
   
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

3. **Charts Not Displaying**
   ```bash
   # Clear Streamlit cache
   streamlit cache clear
   ```

### Debug Mode

Use the included debug utility to diagnose database issues:

```bash
streamlit run debug_version.py
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to functions
- Test your changes locally
- Update documentation if needed

## 📝 API Reference

### Core Functions

```python
# Transaction Management
add_transaction(transaction_type, category, amount, description="")
get_transactions()  # Returns all user transactions
delete_transaction(transaction_id)

# Data Analysis
get_summary()  # Returns (total_income, total_expense)
get_category_summary()  # Category-wise breakdown
get_spending_insights()  # AI-powered insights

# Database
initialize_database()  # Set up tables
clear_all_data()  # Remove all user data
```

## 🔐 Security & Privacy

- **User Isolation**: Each session gets a unique user ID
- **Secure Database**: All data encrypted in transit and at rest
- **No Personal Info**: No email or personal data collection required
- **Local Storage**: Option to run completely locally

## 📊 Performance

- **Caching**: Smart caching with 10-second TTL for optimal performance
- **Lazy Loading**: Data loaded only when needed
- **Optimized Queries**: Efficient database queries with proper indexing
- **Mobile Optimized**: Responsive design for all screen sizes

## 🆘 Support

### Get Help

- 📧 **Email**: [dicksone2006@gmail.com]
- 🐛 **Issues**: [GitHub Issues](https://github.com/DicksonLegend/Budget-Buddy/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/DicksonLegend/Budget-Buddy/discussions)

### Documentation

- 📖 **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io/)
- 🐘 **PostgreSQL Docs**: [postgresql.org/docs](https://www.postgresql.org/docs/)
- 🚂 **Railway Docs**: [docs.railway.app](https://docs.railway.app/)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit Team** - For the amazing web framework
- **Railway** - For seamless deployment experience
- **Plotly** - For beautiful, interactive charts
- **PostgreSQL** - For robust data storage

## 🗺️ Roadmap

### Upcoming Features

- [ ] **Multi-user Support** - Proper authentication system
- [ ] **Budget Goals** - Set and track spending limits
- [ ] **Recurring Transactions** - Automatic monthly income/expenses
- [ ] **Data Import** - CSV/Excel import functionality
- [ ] **Mobile App** - React Native companion app
- [ ] **Email Reports** - Weekly/monthly financial summaries
- [ ] **Advanced Analytics** - Forecasting and predictions
- [ ] **Bank Integration** - Connect bank accounts (with Plaid)

### Recent Updates

- ✅ **v1.0.0** - Initial release with core functionality
- ✅ **Railway Deployment** - One-click deployment support
- ✅ **Responsive Design** - Mobile-optimized interface
- ✅ **Smart Insights** - AI-powered spending analysis

---

<div align="center">

**Built with ❤️ by [DicksonLegend](https://github.com/DicksonLegend)**

[⭐ Star this repo](https://github.com/DicksonLegend/Budget-Buddy) | [🐛 Report Bug](https://github.com/DicksonLegend/Budget-Buddy/issues) | [💡 Request Feature](https://github.com/DicksonLegend/Budget-Buddy/issues)

</div>

---

*Made with 💰 for better financial management*
