"""Add auto-posting tables

Revision ID: 001
Revises:
Create Date: 2025-11-18

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create scheduled_posts table
    op.create_table('scheduled_posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content_type', sa.String(length=50), nullable=True),
        sa.Column('platforms', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('ticker_id', sa.Integer(), nullable=True),
        sa.Column('pattern_scan_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('hashtags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('scheduled_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('posted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['pattern_scan_id'], ['pattern_scans.id'], ),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scheduled_posts_content_type'), 'scheduled_posts', ['content_type'], unique=False)
    op.create_index(op.f('ix_scheduled_posts_id'), 'scheduled_posts', ['id'], unique=False)
    op.create_index(op.f('ix_scheduled_posts_pattern_scan_id'), 'scheduled_posts', ['pattern_scan_id'], unique=False)
    op.create_index(op.f('ix_scheduled_posts_scheduled_time'), 'scheduled_posts', ['scheduled_time'], unique=False)
    op.create_index(op.f('ix_scheduled_posts_status'), 'scheduled_posts', ['status'], unique=False)
    op.create_index(op.f('ix_scheduled_posts_ticker_id'), 'scheduled_posts', ['ticker_id'], unique=False)

    # Create post_logs table
    op.create_table('post_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scheduled_post_id', sa.Integer(), nullable=True),
        sa.Column('platform', sa.String(length=50), nullable=True),
        sa.Column('post_id', sa.String(length=255), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('url', sa.Text(), nullable=True),
        sa.Column('posted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('compliance_disclaimer', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['scheduled_post_id'], ['scheduled_posts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_logs_id'), 'post_logs', ['id'], unique=False)
    op.create_index(op.f('ix_post_logs_platform'), 'post_logs', ['platform'], unique=False)
    op.create_index(op.f('ix_post_logs_posted_at'), 'post_logs', ['posted_at'], unique=False)
    op.create_index(op.f('ix_post_logs_scheduled_post_id'), 'post_logs', ['scheduled_post_id'], unique=False)

    # Create post_analytics table
    op.create_table('post_analytics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('post_log_id', sa.Integer(), nullable=True),
        sa.Column('platform', sa.String(length=50), nullable=True),
        sa.Column('likes', sa.Integer(), nullable=True),
        sa.Column('shares', sa.Integer(), nullable=True),
        sa.Column('comments', sa.Integer(), nullable=True),
        sa.Column('impressions', sa.Integer(), nullable=True),
        sa.Column('engagement_rate', sa.Float(), nullable=True),
        sa.Column('follower_count', sa.Integer(), nullable=True),
        sa.Column('checked_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['post_log_id'], ['post_logs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_analytics_checked_at'), 'post_analytics', ['checked_at'], unique=False)
    op.create_index(op.f('ix_post_analytics_id'), 'post_analytics', ['id'], unique=False)
    op.create_index(op.f('ix_post_analytics_platform'), 'post_analytics', ['platform'], unique=False)
    op.create_index(op.f('ix_post_analytics_post_log_id'), 'post_analytics', ['post_log_id'], unique=False)

    # Create community_engagements table
    op.create_table('community_engagements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=True),
        sa.Column('engagement_type', sa.String(length=50), nullable=True),
        sa.Column('target_user', sa.String(length=255), nullable=True),
        sa.Column('target_post_id', sa.String(length=255), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('executed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_community_engagements_created_at'), 'community_engagements', ['created_at'], unique=False)
    op.create_index(op.f('ix_community_engagements_engagement_type'), 'community_engagements', ['engagement_type'], unique=False)
    op.create_index(op.f('ix_community_engagements_id'), 'community_engagements', ['id'], unique=False)
    op.create_index(op.f('ix_community_engagements_platform'), 'community_engagements', ['platform'], unique=False)
    op.create_index(op.f('ix_community_engagements_status'), 'community_engagements', ['status'], unique=False)

    # Create compliance_logs table
    op.create_table('compliance_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('post_log_id', sa.Integer(), nullable=True),
        sa.Column('compliance_type', sa.String(length=50), nullable=True),
        sa.Column('disclaimer_text', sa.Text(), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=True),
        sa.Column('added_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('verified', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['post_log_id'], ['post_logs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_compliance_logs_added_at'), 'compliance_logs', ['added_at'], unique=False)
    op.create_index(op.f('ix_compliance_logs_compliance_type'), 'compliance_logs', ['compliance_type'], unique=False)
    op.create_index(op.f('ix_compliance_logs_id'), 'compliance_logs', ['id'], unique=False)
    op.create_index(op.f('ix_compliance_logs_platform'), 'compliance_logs', ['platform'], unique=False)
    op.create_index(op.f('ix_compliance_logs_post_log_id'), 'compliance_logs', ['post_log_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_compliance_logs_post_log_id'), table_name='compliance_logs')
    op.drop_index(op.f('ix_compliance_logs_platform'), table_name='compliance_logs')
    op.drop_index(op.f('ix_compliance_logs_id'), table_name='compliance_logs')
    op.drop_index(op.f('ix_compliance_logs_compliance_type'), table_name='compliance_logs')
    op.drop_index(op.f('ix_compliance_logs_added_at'), table_name='compliance_logs')
    op.drop_table('compliance_logs')

    op.drop_index(op.f('ix_community_engagements_status'), table_name='community_engagements')
    op.drop_index(op.f('ix_community_engagements_platform'), table_name='community_engagements')
    op.drop_index(op.f('ix_community_engagements_id'), table_name='community_engagements')
    op.drop_index(op.f('ix_community_engagements_engagement_type'), table_name='community_engagements')
    op.drop_index(op.f('ix_community_engagements_created_at'), table_name='community_engagements')
    op.drop_table('community_engagements')

    op.drop_index(op.f('ix_post_analytics_post_log_id'), table_name='post_analytics')
    op.drop_index(op.f('ix_post_analytics_platform'), table_name='post_analytics')
    op.drop_index(op.f('ix_post_analytics_id'), table_name='post_analytics')
    op.drop_index(op.f('ix_post_analytics_checked_at'), table_name='post_analytics')
    op.drop_table('post_analytics')

    op.drop_index(op.f('ix_post_logs_scheduled_post_id'), table_name='post_logs')
    op.drop_index(op.f('ix_post_logs_posted_at'), table_name='post_logs')
    op.drop_index(op.f('ix_post_logs_platform'), table_name='post_logs')
    op.drop_index(op.f('ix_post_logs_id'), table_name='post_logs')
    op.drop_table('post_logs')

    op.drop_index(op.f('ix_scheduled_posts_ticker_id'), table_name='scheduled_posts')
    op.drop_index(op.f('ix_scheduled_posts_status'), table_name='scheduled_posts')
    op.drop_index(op.f('ix_scheduled_posts_scheduled_time'), table_name='scheduled_posts')
    op.drop_index(op.f('ix_scheduled_posts_pattern_scan_id'), table_name='scheduled_posts')
    op.drop_index(op.f('ix_scheduled_posts_id'), table_name='scheduled_posts')
    op.drop_index(op.f('ix_scheduled_posts_content_type'), table_name='scheduled_posts')
    op.drop_table('scheduled_posts')
