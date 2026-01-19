"""Initial migration

Revision ID: 0001
Revises: 
Create Date: 2024-01-20 02:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('skills', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('github_url', sa.String(length=255), nullable=True),
        sa.Column('demo_url', sa.String(length=255), nullable=True),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('is_featured', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('status', sa.String(length=20), server_default='active', nullable=False),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), server_default='{}', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), onupdate=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index on title for faster searches
    op.create_index(op.f('ix_projects_title'), 'projects', ['title'], unique=False)
    
    # Create index on skills for faster filtering
    op.execute("""
        CREATE INDEX ix_projects_skills ON projects USING GIN (skills);
    """)

def downgrade():
    # Drop indexes first
    op.drop_index('ix_projects_title', table_name='projects')
    op.execute("DROP INDEX IF EXISTS ix_projects_skills")
    
    # Then drop the table
    op.drop_table('projects')
