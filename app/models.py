from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    # Define relationships
    daily_payments = db.relationship('DailyPaymentModel', back_populates='user', lazy='dynamic')
    payment_history = db.relationship('PaymentHistoryModel', back_populates='user', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

class Product(db.Model):
    __tablename__ = 'products' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock
        }

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)  # New column for total amount

    items = db.relationship('OrderItem', backref='order', lazy=True)
    payment = db.relationship('Payment', uselist=False, back_populates='order')
    returns = db.relationship('Return', backref='original_order', lazy=True)



    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'created_at': self.created_at,
            'amount': self.amount,
            'items': [item.to_dict() for item in self.items],
            'payment': self.payment.to_dict() if self.payment else None,
            'returns': [ret.to_dict() for ret in self.returns]
        }

class OrderItem(db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)  # You may need to add a price column if necessary

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price  # Include price if necessary
        }

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    order = db.relationship('Order', back_populates='payment')

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'amount': self.amount,
            'status': self.status,
            'created_at': self.created_at
        }

class Return(db.Model):
    __tablename__ = 'returns'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # order = db.relationship('Order', backref='returns')

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'reason': self.reason,
            'status': self.status,
            'created_at': self.created_at
        }
    
class DailyPaymentModel(db.Model):
    __tablename__ = 'daily_payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow().date())  # Use lambda for default date
    paid = db.Column(db.Boolean, default=False)

    # Relationship with User (like ProductModel with StoreModel)
    user = db.relationship('User', back_populates='daily_payments')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='uq_user_date'),
        db.Index('idx_user_date', 'user_id', 'date')
    )

    @classmethod
    def mark_paid(cls, user_id, date=None):
        date = date or datetime.utcnow().date()
        payment = cls.query.filter_by(user_id=user_id, date=date).first()

        if not payment:
            payment = cls(user_id=user_id, date=date, paid=True)
            db.session.add(payment)
        else:
            payment.paid = True

        db.session.commit()
        PaymentHistoryModel.record_history(user_id, date, 'paid', 'STK push successful')

    @classmethod
    def mark_as_unpaid(cls, user_id, date=None):
        date = date or datetime.utcnow().date()
        payment = cls.query.filter_by(user_id=user_id, date=date).first()

        if not payment:
            # Create a new unpaid record for the missed payment
            payment = cls(user_id=user_id, date=date, paid=False)
            db.session.add(payment)
        else:
            payment.paid = False  # Mark as unpaid if exists

        db.session.commit()


class PaymentHistoryModel(db.Model):
    __tablename__ = 'payment_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 'paid' or 'unpaid'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.String(255), nullable=True)

    # Relationship with User (like ProductModel with StoreModel)
    user = db.relationship('User', back_populates='payment_history')

    def to_dict(self):
        """Convert the PaymentHistoryModel instance to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,  # Convert date to string
            'status': self.status,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'reason': self.reason,
        }
        
    @classmethod
    def record_history(cls, user_id, date, status, reason=None):
        history = cls(user_id=user_id, date=date, status=status, reason=reason)
        db.session.add(history)
        db.session.commit()

