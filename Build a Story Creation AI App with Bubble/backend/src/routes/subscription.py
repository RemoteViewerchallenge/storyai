from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.db import db
from src.models.subscription import UserSubscription, FeatureUsage, SubscriptionTier
from datetime import datetime

subscription_bp = Blueprint('subscription', __name__)

@subscription_bp.route('/subscription/<user_id>', methods=['GET'])
@cross_origin()
def get_user_subscription(user_id):
    """Get user's subscription details"""
    subscription = UserSubscription.get_or_create_subscription(user_id)
    return jsonify(subscription.to_dict())

@subscription_bp.route('/subscription/<user_id>/check-feature', methods=['POST'])
@cross_origin()
def check_feature_access(user_id):
    """Check if user can access a specific feature"""
    try:
        data = request.json
        feature = data.get('feature')
        
        if not feature:
            return jsonify({'error': 'Feature name is required'}), 400
        
        subscription = UserSubscription.get_or_create_subscription(user_id)
        
        access_checks = {
            'create_story': subscription.can_create_stories(),
            'continue_story': subscription.can_continue_story(),
            'premium_characters': subscription.can_use_premium_features(),
            'premium_image_styles': subscription.can_use_premium_features(),
            'voice_input': subscription.can_use_premium_features(),
            'partner_creation': subscription.can_use_premium_features(),
            'story_saving': subscription.can_use_premium_features()
        }
        
        can_access = access_checks.get(feature, False)
        
        response = {
            'user_id': user_id,
            'feature': feature,
            'can_access': can_access,
            'subscription_tier': subscription.tier.value,
            'is_premium': subscription.can_use_premium_features()
        }
        
        # Add specific limits for free tier
        if not subscription.can_use_premium_features():
            response.update({
                'stories_created_this_month': subscription.stories_created_this_month,
                'story_segments_this_month': subscription.story_segments_this_month,
                'free_tier_limits': {
                    'max_stories_per_month': 5,
                    'max_segments_per_month': 50
                }
            })
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subscription_bp.route('/subscription/<user_id>/start-trial', methods=['POST'])
@cross_origin()
def start_trial(user_id):
    """Start a free trial for the user"""
    try:
        data = request.json
        trial_days = data.get('trial_days', 7)
        
        subscription = UserSubscription.get_or_create_subscription(user_id)
        
        if subscription.tier != SubscriptionTier.FREE:
            return jsonify({'error': 'User is already on a premium plan'}), 400
        
        if subscription.is_trial:
            return jsonify({'error': 'User has already used their trial'}), 400
        
        success = subscription.start_trial(trial_days)
        
        if success:
            db.session.commit()
            return jsonify({
                'message': 'Trial started successfully',
                'subscription': subscription.to_dict()
            })
        else:
            return jsonify({'error': 'Failed to start trial'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@subscription_bp.route('/subscription/<user_id>/upgrade', methods=['POST'])
@cross_origin()
def upgrade_subscription(user_id):
    """Upgrade user to premium subscription"""
    try:
        data = request.json
        subscription_months = data.get('months', 1)
        stripe_customer_id = data.get('stripe_customer_id')
        stripe_subscription_id = data.get('stripe_subscription_id')
        
        subscription = UserSubscription.get_or_create_subscription(user_id)
        subscription.upgrade_to_premium(subscription_months)
        
        if stripe_customer_id:
            subscription.stripe_customer_id = stripe_customer_id
        if stripe_subscription_id:
            subscription.stripe_subscription_id = stripe_subscription_id
        
        db.session.commit()
        
        return jsonify({
            'message': 'Subscription upgraded successfully',
            'subscription': subscription.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@subscription_bp.route('/subscription/<user_id>/downgrade', methods=['POST'])
@cross_origin()
def downgrade_subscription(user_id):
    """Downgrade user to free tier"""
    try:
        subscription = UserSubscription.query.filter_by(user_id=user_id).first()
        
        if not subscription:
            return jsonify({'error': 'Subscription not found'}), 404
        
        subscription.downgrade_to_free()
        db.session.commit()
        
        return jsonify({
            'message': 'Subscription downgraded successfully',
            'subscription': subscription.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@subscription_bp.route('/subscription/<user_id>/usage', methods=['POST'])
@cross_origin()
def log_feature_usage(user_id):
    """Log usage of a feature"""
    try:
        data = request.json
        feature_name = data.get('feature_name')
        
        if not feature_name:
            return jsonify({'error': 'Feature name is required'}), 400
        
        # Log the usage
        usage = FeatureUsage.log_feature_usage(user_id, feature_name)
        
        # Update subscription counters
        subscription = UserSubscription.get_or_create_subscription(user_id)
        
        if feature_name == 'story_creation':
            subscription.increment_story_count()
        elif feature_name == 'story_continuation':
            subscription.increment_segment_count()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Usage logged successfully',
            'usage': usage.to_dict(),
            'subscription': subscription.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@subscription_bp.route('/subscription/<user_id>/usage-stats', methods=['GET'])
@cross_origin()
def get_usage_stats(user_id):
    """Get usage statistics for a user"""
    try:
        subscription = UserSubscription.get_or_create_subscription(user_id)
        
        # Get recent usage
        recent_usage = FeatureUsage.query.filter_by(user_id=user_id).order_by(
            FeatureUsage.created_at.desc()
        ).limit(10).all()
        
        return jsonify({
            'subscription': subscription.to_dict(),
            'recent_usage': [usage.to_dict() for usage in recent_usage]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subscription_bp.route('/subscription/tiers', methods=['GET'])
@cross_origin()
def get_subscription_tiers():
    """Get available subscription tiers and their features"""
    return jsonify({
        'tiers': {
            'free': {
                'name': 'Storyteller',
                'price': 0,
                'features': [
                    'Basic character creation (Male/Female)',
                    'Anime image style',
                    'Single character stories',
                    'Text input only',
                    'Standard narrator voice',
                    '5 stories per month',
                    '50 story segments per month'
                ],
                'limitations': [
                    'No alien characters',
                    'No fantasy/realistic image styles',
                    'No partner characters',
                    'No voice input',
                    'Limited phone interactions'
                ]
            },
            'premium': {
                'name': 'Story Master',
                'price': 9.99,
                'billing': 'monthly',
                'features': [
                    'All character types (including Alien)',
                    'All image styles (Anime, Fantasy, Realistic)',
                    'Partner character creation',
                    'Unlimited story length',
                    'Voice input (TTS)',
                    'Enhanced phone interactions',
                    'Character voice customization',
                    'Story saving and resuming',
                    'Multiple concurrent stories'
                ],
                'trial': {
                    'available': True,
                    'duration_days': 7
                }
            }
        }
    })

