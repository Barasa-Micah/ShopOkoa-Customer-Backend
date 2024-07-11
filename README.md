# ShopOkoa Customer 

## Introduction
This Flask application serves as a backend for an e-commerce platform. It provides endpoints for user authentication, order management, payment processing, and return requests.

## Setup

### Prerequisites
- Python 3.7+
- Virtual environment (optional but recommended)

### Installation
1. Clone the repository:
   \`\`\`bash
   git clone <repository_url>
   cd <repository_name>
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. Set up environment variables (optional):
   - Create a \`.env\` file in the root directory.
   - Define the following variables:
     \`\`\`bash
     SECRET_KEY=<your_secret_key>
     DATABASE_URL=<your_database_url>
     JWT_SECRET_KEY=<your_jwt_secret_key>
     \`\`\`

4. Initialize the database:
   \`\`\`bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   \`\`\`

## Configuration

The application can be configured for different environments (development, testing, production) via the \`Config\` class in \`app/config.py\`.

## Usage

### Running the Application
Run the Flask application:
   \`\`\`bash
   flask run
   \`\`\`

The application will start on \`http://localhost:5000\` by default.

### Endpoints

#### Authentication
- **POST /auth/register** - Register a new user.
- **POST /auth/login** - Login and generate access tokens.
- **GET /auth/profile** - Fetch user profile information.

#### Orders
- **POST /orders** - Create a new order.
- **POST /orders/<order_id>/cancel** - Cancel an order.
- **POST /orders/<order_id>/payment** - Process payment for an order.
- **POST /orders/<order_id>/return** - Initiate a return for an order.
- **GET /orders/<order_id>/status** - Get the status of an order.

### Models
The application includes the following models:
- **User**: Represents a registered user.
- **Product**: Represents a product available for purchase.
- **Order**: Represents a customer's order.
- **OrderItem**: Represents an item within an order.
- **Payment**: Represents a payment made for an order.
- **Return**: Represents a return request for an order.

### Schemas
- **UserSchema**: Serialization schema for the \`User\` model.
- **OrderSchema**: Serialization schema for the \`Order\` model.
- **ProductSchema**: Serialization schema for the \`Product\` model.
- **PaymentSchema**: Serialization schema for the \`Payment\` model.
- **ReturnSchema**: Serialization schema for the \`Return\` model.


## License
This project is licensed under the MIT License - see the LICENSE file for details.
EOF