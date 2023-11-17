"""empty message

Revision ID: 4a2cbdde9202
Revises: c0a3944210f4
Create Date: 2023-11-16 15:49:14.361582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a2cbdde9202'
down_revision = 'c0a3944210f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sensors',
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.Column('vibration', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('acceleration_x', sa.Float(), nullable=True),
    sa.Column('acceleration_y', sa.Float(), nullable=True),
    sa.Column('acceleration_z', sa.Float(), nullable=True),
    sa.Column('gyroscope_x', sa.Float(), nullable=True),
    sa.Column('gyroscope_y', sa.Float(), nullable=True),
    sa.Column('gyroscope_z', sa.Float(), nullable=True),
    sa.Column('crash', sa.Integer(), nullable=True),
    sa.Column('terrain', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ),
    sa.PrimaryKeyConstraint('time', 'trip_id')
    )
    op.create_table('terrain',
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('terrain', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ),
    sa.PrimaryKeyConstraint('time', 'trip_id')
    )
    op.drop_table('imu')
    op.drop_table('gps')
    op.drop_table('vibration')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vibration',
    sa.Column('time', sa.DATETIME(), nullable=False),
    sa.Column('intensity', sa.INTEGER(), nullable=True),
    sa.Column('trip_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ),
    sa.PrimaryKeyConstraint('time')
    )
    op.create_table('gps',
    sa.Column('time', sa.DATETIME(), nullable=False),
    sa.Column('latitude', sa.FLOAT(), nullable=True),
    sa.Column('longitude', sa.FLOAT(), nullable=True),
    sa.Column('trip_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ),
    sa.PrimaryKeyConstraint('time')
    )
    op.create_table('imu',
    sa.Column('time', sa.DATETIME(), nullable=False),
    sa.Column('acceleration_x', sa.FLOAT(), nullable=True),
    sa.Column('acceleration_y', sa.FLOAT(), nullable=True),
    sa.Column('acceleration_z', sa.FLOAT(), nullable=True),
    sa.Column('gyroscope_x', sa.FLOAT(), nullable=True),
    sa.Column('gyroscope_y', sa.FLOAT(), nullable=True),
    sa.Column('gyroscope_z', sa.FLOAT(), nullable=True),
    sa.Column('trip_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ),
    sa.PrimaryKeyConstraint('time')
    )
    op.drop_table('terrain')
    op.drop_table('sensors')
    # ### end Alembic commands ###