from src.db import db
from datetime import datetime, timedelta
import enum

class SubscriptionTier(enum.Enum):
    FREE = 'free'
    PREMIUM = 'premium'

class UserSubscription(db.Model):
    __tablename__ = 'user_subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True, nullable=False)
    tier = db.Column(db.Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    is_trial = db.Column(db.Boolean, default=False)
    trial_ends_at = db.Column(db.DateTime, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    stripe_customer_id = db.Column(db.String(100), nullable=True)
    stripe_subscription_id = db.Column(db.String(100), nullable=True)
    stories_created_this_month = db.Column(db.Integer, default=0)
    story_segments_this_month = db.Column(db.Integer, default=0)
    last_reset_date = db.Column(db.Date, default=datetime.utcnow().date())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'tier': self.tier.value,
            'is_trial': self.is_trial,
            'trial_ends_at': self.trial_ends_at.isoformat() if self.trial_ends_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'stories_created_this_month': self.stories_created_this_month,
            'story_segments_this_month': self.story_segments_this_month,
            'last_reset_date': self.last_reset_date.isoformat()
        }

class FeatureUsage(db.Model):
    __tablename__ = 'feature_usage'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    feature_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'feature_name': self.feature_name,
            'created_at': self.created_at.isoformat()
        }
