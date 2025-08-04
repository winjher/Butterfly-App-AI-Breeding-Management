# Butterfly Breeding Ecosystem

## Overview

This is a comprehensive Streamlit-based butterfly breeding management system that integrates multiple business functions including breeding management, AI classification, point of sale, sales tracking, and farm booking systems. The application is designed for butterfly breeders, farm operators, and customers to manage the complete butterfly lifecycle and business operations.

## User Preferences

```
Preferred communication style: Simple, everyday language.
```

## System Architecture

The application follows a modular Streamlit architecture with the following key design decisions:

### Frontend Architecture
- **Framework**: Streamlit with custom glassmorphism styling
- **UI Pattern**: Multi-tab navigation with modular components
- **Styling**: Custom CSS with glassmorphism effects and background image support
- **Responsive Design**: Wide layout configuration for desktop-first experience

### Backend Architecture
- **Database**: Hybrid approach using SQLite for user authentication and CSV files for business data
- **Authentication**: Session-based authentication with SHA256 password hashing
- **Data Persistence**: CSV files for transactional data, SQLite for user management
- **File Organization**: Modular structure with separate modules for each business function

### Data Storage Strategy
- **User Data**: SQLite database (`users.db`) for authentication and user profiles
- **Business Data**: CSV files for flexible data storage and easy export/import
- **Images**: Local file system storage in `icon/` directory
- **Model Data**: Dedicated `model/` directory for AI classification models

## Key Components

### Authentication Module (`modules/auth.py`)
- SHA256 password hashing for security
- Role-based access control (admin/user)
- Session state management
- Default admin account creation

### Profile Management (`modules/profile_management.py`)
- Role-based profile editing with extended user fields
- Contact information, birthday, and address management
- Payment information storage (credit card last 4 digits)
- Student and faculty specific profile sections

### Premium System (`modules/premium_system.py`)
- Premium membership subscription (₱299/month)
- Commission tracking and Level 2 achievement system
- 260,000 pesos earnings milestone for Level 2 status
- 20,000 pesos achievement prize for reaching Level 2
- Ewallet integration with transaction history
- Signup bonus system (200 pesos GCash bonus)

### Email Notifications (`modules/email_notifications.py`)
- SendGrid integration for automated email campaigns
- Premium membership promotion emails to breeders
- Level upgrade congratulations notifications
- Bulk email capabilities for breeder outreach

### Landing Page (`modules/landing_page.py`)
- Enhanced dashboard with signup bonus promotion
- Premium membership benefits showcase
- Success stories and testimonials display
- Top earners leaderboard
- Feature highlights and conversion optimization

### Breeding Management (`modules/breeding_management.py`)
- Cage management system
- Task scheduling and tracking
- Breeding batch monitoring
- Analytics dashboard with real-time metrics

### AI Classification (`modules/ai_classification.py`)
- TensorFlow/Keras integration for butterfly species identification
- Image preprocessing and validation
- Support for multiple image formats
- Classification confidence scoring

### Point of Sale (`modules/point_of_sale.py`)
- Shopping cart functionality
- Order number generation
- Inventory management for 18 butterfly/moth species
- Transaction recording with profit/cost tracking

### Sales Tracking (`modules/sales_tracking.py`)
- Breeder sales management
- Purchase tracking
- Customer relationship management
- Analytics and reporting

### Booking System (`modules/booking_system.py`)
- Farm visit scheduling
- Location mapping with Folium integration
- Capacity management
- Review system

## Data Flow

1. **User Authentication**: Users log in through the auth module, establishing session state
2. **Navigation**: Main app routes users to selected modules based on sidebar navigation
3. **Data Operations**: Each module independently manages its CSV files for data persistence
4. **Image Processing**: AI classification module processes uploaded images through preprocessing pipeline
5. **Reporting**: Data aggregation across modules for analytics and reporting

## External Dependencies

### Core Framework
- **Streamlit**: Primary web application framework
- **Pandas**: Data manipulation and CSV handling
- **SQLite3**: Embedded database for user management

### AI/ML Components
- **TensorFlow**: Machine learning framework for butterfly classification
- **PIL (Pillow)**: Image processing and manipulation
- **NumPy**: Numerical operations for image preprocessing

### UI/Visualization
- **Folium**: Interactive maps for farm locations
- **Streamlit-Folium**: Streamlit integration for map components

### Security & Authentication
- **Hashlib**: Password hashing (SHA256)
- **Bcrypt**: Alternative password hashing (imported but not actively used)

### Utilities
- **Base64**: Image encoding for CSS background integration
- **DateTime**: Timestamp management across all modules
- **OS**: File system operations and directory management

## Deployment Strategy

### Development Setup
- Single-file entry point (`app.py`) for easy deployment
- Modular architecture allows for independent testing of components
- CSV-based data storage eliminates complex database setup requirements

### Production Considerations
- **Database Migration**: Current CSV approach may need PostgreSQL migration for scalability
- **File Storage**: Local image storage should migrate to cloud storage (AWS S3, etc.)
- **Model Storage**: TensorFlow models require proper versioning and deployment strategy
- **Session Management**: Current in-memory sessions need persistent storage for production

### Scalability Notes
- CSV files work well for small to medium datasets but may need database migration
- Current architecture supports horizontal scaling through database abstraction layer
- Image processing pipeline can be offloaded to separate microservice if needed

The application prioritizes ease of deployment and maintenance while providing comprehensive business functionality for butterfly breeding operations.