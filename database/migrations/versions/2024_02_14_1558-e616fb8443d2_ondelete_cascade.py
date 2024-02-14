"""ondelete CASCADE

Revision ID: e616fb8443d2
Revises: 43f1f3df812f
Create Date: 2024-02-14 15:58:31.453623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e616fb8443d2'
down_revision: Union[str, None] = '43f1f3df812f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('groups_studio_id_fkey', 'groups', type_='foreignkey')
    op.create_foreign_key(None, 'groups', 'studios', ['studio_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('individual_lessons_studio_id_fkey', 'individual_lessons', type_='foreignkey')
    op.create_foreign_key(None, 'individual_lessons', 'studios', ['studio_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('schedules_group_id_fkey', 'schedules', type_='foreignkey')
    op.create_foreign_key(None, 'schedules', 'groups', ['group_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('student_group_association_student_id_fkey', 'student_group_association', type_='foreignkey')
    op.drop_constraint('student_group_association_group_id_fkey', 'student_group_association', type_='foreignkey')
    op.create_foreign_key(None, 'student_group_association', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'student_group_association', 'groups', ['group_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'student_group_association', type_='foreignkey')
    op.drop_constraint(None, 'student_group_association', type_='foreignkey')
    op.create_foreign_key('student_group_association_group_id_fkey', 'student_group_association', 'groups', ['group_id'], ['id'])
    op.create_foreign_key('student_group_association_student_id_fkey', 'student_group_association', 'students', ['student_id'], ['id'])
    op.drop_constraint(None, 'schedules', type_='foreignkey')
    op.create_foreign_key('schedules_group_id_fkey', 'schedules', 'groups', ['group_id'], ['id'])
    op.drop_constraint(None, 'individual_lessons', type_='foreignkey')
    op.create_foreign_key('individual_lessons_studio_id_fkey', 'individual_lessons', 'studios', ['studio_id'], ['id'])
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.create_foreign_key('groups_studio_id_fkey', 'groups', 'studios', ['studio_id'], ['id'])
    # ### end Alembic commands ###