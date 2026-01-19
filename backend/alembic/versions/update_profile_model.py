"""Update profile model with new fields and indexes

Revision ID: update_profile_model
Revises: 3c4a79343bc1
Create Date: 2026-01-20 03:40:23.192547

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'update_profile_model'
down_revision = '3c4a79343bc1'
branch_labels = None
depends_on = None

def upgrade():
    # SQLite doesn't support ALTER TABLE operations that modify columns
    # So we need to create a new table with the updated schema, copy the data,
    # drop the old table, and rename the new one
    
    # Create a temporary table with the new schema
    op.create_table(
        'profiles_new',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(100), nullable=False, index=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('title', sa.String(200), nullable=True),
        sa.Column('location', sa.String(200), nullable=True, index=True),
        sa.Column('about', sa.Text, nullable=True),
        sa.Column('github_url', sa.String(500), nullable=True),
        sa.Column('linkedin_url', sa.String(500), nullable=True),
        sa.Column('twitter_url', sa.String(500), nullable=True),
        sa.Column('profile_picture_url', sa.String(500), nullable=True),
        sa.Column('metadata', sa.JSON, nullable=True, default=dict),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), onupdate=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )
    
    # Copy data from old table to new table
    op.execute('''
        INSERT INTO profiles_new (
            id, name, email, title, location, about, 
            github_url, linkedin_url, twitter_url, profile_picture_url,
            created_at, updated_at
        )
        SELECT 
            id, name, email, title, location, about, 
            github_url, linkedin_url, twitter_url, profile_picture_url,
            created_at, updated_at
        FROM profiles
    ''')
    
    # Drop the old table
    op.drop_table('profiles')
    
    # Rename the new table to the original name
    op.rename_table('profiles_new', 'profiles')
    
    # Add indexes
    op.create_index(op.f('ix_profiles_name'), 'profiles', [sa.text('lower(name)')], unique=False)
    op.create_index(op.f('ix_profiles_location'), 'profiles', ['location'], unique=False)
    
    # Set default values for existing rows
    op.execute("UPDATE profiles SET metadata = '{}' WHERE metadata IS NULL")
    
    # Note: SQLite doesn't support table comments, so we skip that

def downgrade():
    # Create a temporary table with the old schema
    op.create_table(
        'profiles_old',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(100), nullable=False, index=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('title', sa.String(100), nullable=True),
        sa.Column('location', sa.String(100), nullable=True, index=True),
        sa.Column('about', sa.Text, nullable=True),
        sa.Column('github_url', sa.String(255), nullable=True),
        sa.Column('linkedin_url', sa.String(255), nullable=True),
        sa.Column('twitter_url', sa.String(255), nullable=True),
        sa.Column('profile_picture_url', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), onupdate=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )
    
    # Copy data from new table to old table (excluding metadata)
    op.execute('''
        INSERT INTO profiles_old (
            id, name, email, title, location, about, 
            github_url, linkedin_url, twitter_url, profile_picture_url,
            created_at, updated_at
        )
        SELECT 
            id, name, email, title, location, about, 
            github_url, linkedin_url, twitter_url, profile_picture_url,
            created_at, updated_at
        FROM profiles
    ''')
    
    # Drop the new table
    op.drop_table('profiles')
    
    # Rename the old table back to the original name
    op.rename_table('profiles_old', 'profiles')
