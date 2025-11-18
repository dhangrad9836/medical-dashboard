# Healthcare Metrics Dashboard

A Django-based web application for visualizing clinical imaging department metrics and operational performance. Built to demonstrate full-stack development skills combined with healthcare domain expertise.

![Dashboard Screenshot](screenshots/dashboard.png)

## 🎯 Project Overview

This dashboard provides real-time insights into radiology/imaging department operations, displaying key performance indicators that directly impact patient satisfaction and operational efficiency. The metrics and workflows are based on 15+ years of real-world experience in medical imaging.

## ✨ Features

- **Real-time Metrics Dashboard**: Key performance indicators at a glance
- **Interactive Data Tables**: Filterable patient visit records with comprehensive details
- **Visual Analytics**: Chart.js-powered visualizations including:
  - Visits by day of week (bar chart)
  - Exam type distribution (pie chart)
  - Daily trends (line chart)
  - Wait time analysis (horizontal bar chart)
- **SQL Documentation**: Transparent display of database queries and ORM usage
- **Healthcare Context**: Explanations of why each metric matters clinically

## 🏥 Healthcare Context

As someone who has worked in MRI/radiology for 15+ years, I understand which metrics matter:

- **Wait Time Analysis**: Critical for patient satisfaction and identifying workflow bottlenecks
- **Modality Utilization**: Informs capacity planning and equipment investment decisions
- **Day-of-Week Patterns**: Guides staffing optimization and scheduling
- **Satisfaction Scores**: Impacts hospital reimbursement (HCAHPS) and patient retention

This isn't just a demo project—it solves real problems I've experienced in clinical settings.

## 🛠️ Technology Stack

**Backend:**
- Python 3.x
- Django 4.x
- SQLite (development)
- Django ORM for database abstraction

**Frontend:**
- Bootstrap 5 (responsive design)
- Chart.js (data visualizations)
- Bootstrap Icons
- Vanilla JavaScript

**Data Generation:**
- Faker library for realistic test data
- Custom Django management command

## 📊 Key Metrics Tracked

1. **Total Visits**: Monthly and all-time patient volume
2. **Average Wait Time**: Operational efficiency indicator (target: <30 minutes)
3. **Patient Satisfaction**: 5-point scale rating
4. **Modality Utilization**: MRI, CT, X-Ray distribution
5. **Exam Type Breakdown**: Most common procedures
6. **Daily Trends**: Visit patterns over 30 days
7. **Emergency vs. Scheduled**: Case type distribution

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/healthcare-metrics-dashboard.git
cd healthcare-metrics-dashboard

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Generate sample data
python manage.py generate_data --count 200

# Start development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 📸 Screenshots

### Dashboard
![Dashboard View](screenshots/dashboard.png)
*Main dashboard showing key performance metrics and recent visits*

### Reports & Analytics
![Reports View](screenshots/reports.png)
*Interactive charts for data visualization and trend analysis*

### Data Table
![Data View](screenshots/data.png)
*Filterable table of patient visits with detailed information*

### Technical Documentation
![Technical View](screenshots/technical.png)
*SQL queries and implementation details*

## 💻 SQL Query Examples

The application uses both Django ORM and demonstrates understanding of SQL fundamentals:

### Total Visits This Month
```sql
SELECT COUNT(*) as total_visits
FROM metrics_patientvisit
WHERE visit_date >= DATE('now', 'start of month');
```

### Average Wait Time by Exam Type
```sql
SELECT exam_type, AVG(wait_time) as avg_wait
FROM metrics_patientvisit
GROUP BY exam_type
ORDER BY avg_wait DESC;
```

### Busiest Days of Week
```sql
SELECT strftime('%w', visit_date) as day_of_week, 
       COUNT(*) as visit_count
FROM metrics_patientvisit
GROUP BY day_of_week;
```

See the `/technical/` page in the application for full documentation.

## 🎓 Skills Demonstrated

- **Full-Stack Development**: Django backend, Bootstrap frontend, JavaScript interactivity
- **Database Design**: Normalized schema, efficient queries, proper indexing
- **Data Visualization**: Chart.js integration for meaningful analytics
- **Healthcare Domain Knowledge**: Realistic metrics and workflows from clinical experience
- **Code Quality**: Clean, commented code with comprehensive documentation
- **User Experience**: Responsive design, intuitive navigation, professional styling


## 📝 Project Structure

```
healthcare-metrics-dashboard/
├── dashboard_project/       # Django project settings
├── metrics/                 # Main application
│   ├── management/
│   │   └── commands/
│   │       └── generate_data.py
│   ├── templates/
│   │   └── metrics/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── data.html
│   │       ├── reports.html
│   │       └── technical.html
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── requirements.txt
└── README.md
```

## 🤝 Connect With Me

- **LinkedIn**: [linkedin.com/in/dhangrad9836](https://www.linkedin.com/in/dhangrad9836/)
- **GitHub**: [github.com/dhangrad9836](https://github.com/dhangrad9836)
- **Email**: darren.dhanpat@outlook.com
- **Website**: https://www.darrendhanpat.com

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built as part of my transition from clinical healthcare (15+ years as MRI Technologist) to healthcare technology development. This project combines my clinical experience with my growing technical skills in software development.

---

**Note**: This application uses synthetic data generated with the Faker library. No actual patient data is used or stored.
